"""Construcción y carga del índice en disco."""

from __future__ import annotations

import json
import sys
from pathlib import Path

import numpy as np

from .chunking import Chunk, chunk_pages
from .config import DATA_DIR, EMBEDDING_MODEL, NORMAS
from .embeddings import embed
from .extract import extract_pages


class IndexNotBuilt(RuntimeError):
    pass


def build_index(data_dir: Path = DATA_DIR) -> list[Chunk]:
    chunks: list[Chunk] = []
    for norma in NORMAS:
        if not norma.path.exists():
            raise FileNotFoundError(f"No encuentro el PDF de {norma.id}: {norma.path}")
        nuevos = chunk_pages(norma.id, extract_pages(norma.path))
        print(f"{norma.id}: {len(nuevos)} fragmentos", file=sys.stderr)
        chunks.extend(nuevos)

    vectors = embed([c.embedding_text for c in chunks], progress=True)

    data_dir.mkdir(parents=True, exist_ok=True)
    with (data_dir / "chunks.jsonl").open("w", encoding="utf-8") as f:
        for chunk in chunks:
            f.write(json.dumps(chunk.to_dict(), ensure_ascii=False) + "\n")
    np.save(data_dir / "embeddings.npy", vectors)
    (data_dir / "meta.json").write_text(
        json.dumps({"embedding_model": EMBEDDING_MODEL, "chunks": len(chunks)}, indent=2),
        encoding="utf-8",
    )
    return chunks


def load_index(data_dir: Path = DATA_DIR) -> tuple[list[Chunk], np.ndarray]:
    meta_path = data_dir / "meta.json"
    if not meta_path.exists():
        raise IndexNotBuilt("No hay índice. Ejecuta primero: rag-normativa index")
    meta = json.loads(meta_path.read_text(encoding="utf-8"))
    if meta["embedding_model"] != EMBEDDING_MODEL:
        raise IndexNotBuilt(
            f"El índice usa {meta['embedding_model']} y la configuración {EMBEDDING_MODEL}. "
            "Reconstruye con: rag-normativa index"
        )
    with (data_dir / "chunks.jsonl").open(encoding="utf-8") as f:
        chunks = [Chunk(**json.loads(line)) for line in f]
    return chunks, np.load(data_dir / "embeddings.npy")
