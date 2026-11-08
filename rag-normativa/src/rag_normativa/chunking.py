"""Troceado guiado por la estructura legal y curricular de las normas."""

from __future__ import annotations

import re
from dataclasses import asdict, dataclass

from .config import MAX_CHUNK_CHARS, OVERLAP_CHARS
from .extract import Page

_NUMERALES = (
    r"(?:Uno|Dos|Tres|Cuatro|Cinco|Seis|Siete|Ocho|Nueve|Diez|Once|Doce|Trece|Catorce|Quince"
    r"|Dieciséis|Diecisiete|Dieciocho|Diecinueve|Veinte|Veintiuno|Veintidós|Veintitrés"
    r"|Veinticuatro|Veinticinco|Veintiséis|Veintisiete|Veintiocho|Veintinueve"
    r"|Treinta|Cuarenta|Cincuenta|Sesenta|Setenta|Ochenta|Noventa|Cien|Ciento)"
    r"(?: y \w+| \w+)?(?: bis)?"
)
_ARTICULO_TITULADO = re.compile(r"(Art[ií]culo (?:\d+(?: bis)?|único))\. ?([A-ZÁÉÍÓÚÑ].*)?$")
_ARTICULO_SOLO = re.compile(r"(Art[ií]culo \d+(?: bis)?)$")
_DISPOSICION = re.compile(
    r"(Disposici[oó]n (?:adicional|transitoria|derogatoria|final)(?: [\wáéíóúñ]+)?(?: bis)?)"
    r"(?:\.(?: .*)?)?$",
    re.IGNORECASE,
)
_PREAMBULO = re.compile(r"PREÁMBULO$")
_ANEXO = re.compile(r"ANEXO(?: [IVX]+)?\.?$")
_APARTADO_LEY = re.compile(rf"({_NUMERALES})\. ([A-ZÁÉÍÓÚÑ«“\"].*)$")
_BLOQUE = re.compile(r"(Competencias espec[ií]ficas|Criterios de evaluaci[oó]n|Contenidos|Saberes b[aá]sicos)\.?$", re.IGNORECASE)
_CURSO = re.compile(r"([1-4])\.?\s?[ºo°]\.? ?(ESO|E\.S\.O\.|Bachillerato|de Bachillerato|curso)\.?$", re.IGNORECASE)
_MAYUSCULAS = re.compile(r"[A-ZÁÉÍÓÚÑÜ][A-ZÁÉÍÓÚÑÜ ,:()\-Y]{3,}[A-ZÁÉÍÓÚÑÜ)I]$")
_COMPETENCIAS = re.compile(r"Competencias espec[ií]ficas\.?$", re.IGNORECASE)
_NO_MATERIA = re.compile(r"(ANEXO|MATERIAS|MODALIDAD)", re.IGNORECASE)


@dataclass(frozen=True)
class Chunk:
    id: str
    norma: str
    page_start: int
    page_end: int
    printed_start: int | None
    section: str
    materia: str
    curso: str
    bloque: str
    text: str

    def to_dict(self) -> dict:
        return asdict(self)

    @property
    def cita(self) -> str:
        paginas = (
            f"p. {self.page_start}"
            if self.page_start == self.page_end
            else f"pp. {self.page_start}-{self.page_end}"
        )
        materia = self.materia.capitalize()
        partes = (self.norma, self.section, materia, self.curso, self.bloque, paginas)
        return ", ".join(p for p in partes if p)

    @property
    def embedding_text(self) -> str:
        cabecera = " | ".join(x for x in (self.norma, self.section, self.materia, self.curso, self.bloque) if x)
        return f"{cabecera}\n{self.text}"


def _flatten(pages: list[Page]) -> list[tuple[str, Page]]:
    return [(line, page) for page in pages for line in page.lines]


def find_materias(lines: list[str], start: int = 0) -> dict[int, str]:
    """Localiza títulos de materia: líneas en mayúsculas seguidas de sus competencias."""
    runs: list[tuple[int, str]] = []
    i = start
    while i < len(lines):
        if _ANEXO.fullmatch(lines[i]):
            i += 1
        elif _MAYUSCULAS.fullmatch(lines[i]):
            first, parts = i, []
            while i < len(lines) and _MAYUSCULAS.fullmatch(lines[i]) and not _ANEXO.fullmatch(lines[i]):
                parts.append(lines[i])
                i += 1
            runs.append((first, " ".join(parts)))
        else:
            i += 1

    materias: dict[int, str] = {}
    for pos, (first, title) in enumerate(runs):
        end = runs[pos + 1][0] if pos + 1 < len(runs) else len(lines)
        if _NO_MATERIA.search(title):
            continue
        if any(_COMPETENCIAS.fullmatch(lines[j]) for j in range(first, end)):
            materias[first] = title
    return materias


def normalize_text(lines: list[str]) -> str:
    """Une líneas partidas por el maquetado, respetando listas y apartados."""
    text = "\n".join(lines)
    text = re.sub(r"(\w)-\n([a-záéíóúñ])", r"\1\2", text)
    text = re.sub(r"\n(?!(?:\d+\.|[a-zñ]\)|[A-Z]\.|[–—•-]) ?)", " ", text)
    return re.sub(r" {2,}", " ", text).strip()


def _windows(items: list[tuple[str, Page]]) -> list[list[tuple[str, Page]]]:
    windows, current, size = [], [], 0
    for item in items:
        if current and size + len(item[0]) > MAX_CHUNK_CHARS:
            windows.append(current)
            overlap, kept = [], 0
            for previous in reversed(current):
                if kept + len(previous[0]) > OVERLAP_CHARS:
                    break
                overlap.insert(0, previous)
                kept += len(previous[0])
            current, size = overlap, kept
        current.append(item)
        size += len(item[0])
    if current:
        windows.append(current)
    return windows


def chunk_pages(norma: str, pages: list[Page]) -> list[Chunk]:
    flat = _flatten(pages)
    lines = [line for line, _ in flat]
    annex_at = next((i for i, l in enumerate(lines) if _ANEXO.fullmatch(l)), len(lines))
    materias = find_materias(lines, annex_at) if annex_at < len(lines) else {}
    materia_lines = {
        j for start, title in materias.items()
        for j in range(start, start + 8)
        if j < len(lines) and _MAYUSCULAS.fullmatch(lines[j]) and lines[j] in title
    }

    chunks: list[Chunk] = []
    buffer: list[tuple[str, Page]] = []
    state = {"section": "Inicio", "materia": "", "curso": "", "bloque": ""}

    def flush() -> None:
        nonlocal buffer
        for window in _windows(buffer):
            text = normalize_text([line for line, _ in window])
            if len(text) < 30:
                continue
            first, last = window[0][1], window[-1][1]
            chunks.append(Chunk(
                id=f"{norma}-{len(chunks):05d}",
                norma=norma,
                page_start=first.number,
                page_end=last.number,
                printed_start=first.printed,
                text=text,
                **state,
            ))
        buffer = []

    for i, (line, page) in enumerate(flat):
        if i in materias:
            flush()
            state.update(section=state["section"] if i >= annex_at else "", materia=materias[i], curso="", bloque="")
            continue
        if i in materia_lines:
            continue

        if i >= annex_at:
            if _ANEXO.fullmatch(line):
                flush()
                state.update(section="Anexo" + line.rstrip(".")[5:], materia="", curso="", bloque="")
                continue
            if m := _BLOQUE.fullmatch(line):
                flush()
                state.update(bloque=m.group(1).capitalize(), curso=state["curso"] if not _COMPETENCIAS.fullmatch(line) else "")
                continue
            if m := _CURSO.fullmatch(line):
                flush()
                etapa = "ESO" if "E" in m.group(2).upper() and "BACH" not in m.group(2).upper() else "Bachillerato"
                state["curso"] = f"{m.group(1)}º {etapa}"
                continue
        else:
            heading = None
            for pattern in (_PREAMBULO, _ARTICULO_TITULADO, _ARTICULO_SOLO, _DISPOSICION):
                if m := pattern.fullmatch(line):
                    heading = m.group(1) if pattern is not _PREAMBULO else "Preámbulo"
                    break
            if heading is None and norma == "lomloe" and state["section"].startswith("Artículo único") and (m := _APARTADO_LEY.fullmatch(line)):
                heading = f"Artículo único, apartado {m.group(1).lower()}"
            if heading:
                flush()
                state.update(section=heading, materia="", curso="", bloque="")

        buffer.append((line, page))

    flush()
    return chunks
