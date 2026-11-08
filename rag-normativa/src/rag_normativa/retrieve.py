"""Búsqueda híbrida: semántica (embeddings) + léxica (BM25), fusionadas con RRF."""

from __future__ import annotations

import re
import unicodedata
from dataclasses import dataclass

import numpy as np
from rank_bm25 import BM25Okapi

from .chunking import Chunk
from .config import DEFAULT_TOP_K
from .embeddings import embed
from .index import load_index

RRF_K = 60
POOL_SIZE = 50

_STOPWORDS = set(
    "a al algo como con de del el en es la las lo los o para por que se si su sus un una y".split()
)


def strip_accents(text: str) -> str:
    decomposed = unicodedata.normalize("NFD", text)
    return "".join(c for c in decomposed if not unicodedata.combining(c))


def tokenize(text: str) -> list[str]:
    tokens = re.findall(r"[a-z0-9]+", strip_accents(text.lower()))
    return [t for t in tokens if t not in _STOPWORDS]


def _key(text: str) -> str:
    return re.sub(r"[^a-z0-9]", "", strip_accents(text.lower().replace("º", "")))


_ORDINALES = {
    "1": 1, "primero": 1, "primer": 1,
    "2": 2, "segundo": 2,
    "3": 3, "tercero": 3, "tercer": 3,
    "4": 4, "cuarto": 4,
}
_ENLACE = r"(?:curso\s+)?(?:de\s+)?(?:la\s+)?"
# Un número suelto solo cuenta pegado a la etapa («4 ESO»), no en «artículo 2 de la ESO».
_CURSO_EN_PREGUNTA = re.compile(
    rf"\b(?:(primero|primer|segundo|tercero|tercer|cuarto)\s+{_ENLACE}"
    rf"|([1-4])\s*\.?\s*[ºª°o]\s*{_ENLACE}"
    r"|([1-4])\s+)(eso|bachillerato)\b"
)


def detect_curso(query: str) -> str | None:
    """Reconoce un curso escrito en la pregunta, como «2º de ESO» o «segundo de Bachillerato»."""
    match = _CURSO_EN_PREGUNTA.search(strip_accents(query.lower()))
    if not match:
        return None
    ordinal = match.group(1) or match.group(2) or match.group(3)
    etapa = match.group(4)
    numero = _ORDINALES[ordinal]
    if etapa == "bachillerato" and numero > 2:
        return None
    return f"{numero}º {'ESO' if etapa == 'eso' else 'Bachillerato'}"


def rrf(rankings: list[list[int]], k: int = RRF_K) -> dict[int, float]:
    """Reciprocal Rank Fusion: premia lo que aparece alto en varias listas."""
    scores: dict[int, float] = {}
    for ranking in rankings:
        for rank, item in enumerate(ranking, 1):
            scores[item] = scores.get(item, 0.0) + 1.0 / (k + rank)
    return scores


@dataclass(frozen=True)
class Hit:
    chunk: Chunk
    score: float


class Retriever:
    def __init__(self) -> None:
        self.chunks, self.vectors = load_index()
        self.bm25 = BM25Okapi([tokenize(c.embedding_text) for c in self.chunks])

    def _mask(self, norma: str | None, materia: str | None, curso: str | None) -> np.ndarray:
        wanted_materia = _key(materia) if materia else ""
        wanted_curso = _key(curso) if curso else ""
        return np.fromiter(
            (
                (not norma or c.norma == norma)
                and (not wanted_materia or wanted_materia in _key(c.materia))
                and (not wanted_curso or wanted_curso in _key(c.curso))
                for c in self.chunks
            ),
            dtype=bool,
            count=len(self.chunks),
        )

    def search(
        self,
        query: str,
        norma: str | None = None,
        materia: str | None = None,
        curso: str | None = None,
        k: int = DEFAULT_TOP_K,
    ) -> list[Hit]:
        mask = self._mask(norma, materia, curso)
        if not mask.any():
            return []

        def top(scores: np.ndarray, allowed: np.ndarray = mask) -> list[int]:
            order = np.argsort(-scores)
            return [int(i) for i in order if allowed[i]][:POOL_SIZE]

        query_vector = embed([query])[0]
        semantic_scores = self.vectors @ query_vector
        lexical_scores = np.asarray(self.bm25.get_scores(tokenize(query)))
        rankings = [
            top(semantic_scores),
            [i for i in top(lexical_scores) if lexical_scores[i] > 0],
        ]

        # Un curso mencionado en la pregunta añade una lista que lo favorece. No es un
        # filtro: las preguntas generales sobre promoción deben seguir hallando artículos.
        detected = detect_curso(query) if not curso else None
        if detected:
            same_course = mask & np.fromiter(
                (c.curso == detected for c in self.chunks), dtype=bool, count=len(self.chunks)
            )
            rankings.append(top(semantic_scores, same_course))

        fused = rrf(rankings)
        best = sorted(fused.items(), key=lambda item: -item[1])[:k]
        return [Hit(self.chunks[i], score) for i, score in best]
