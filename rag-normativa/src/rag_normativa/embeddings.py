"""Cliente de embeddings de Ollama."""

from __future__ import annotations

import sys

import numpy as np
import requests

from .config import EMBEDDING_MODEL, OLLAMA_URL

BATCH_SIZE = 32


def embed(texts: list[str], model: str = EMBEDDING_MODEL, progress: bool = False) -> np.ndarray:
    """Devuelve una matriz de vectores normalizados (norma L2 = 1)."""
    vectors: list[list[float]] = []
    for start in range(0, len(texts), BATCH_SIZE):
        response = requests.post(
            f"{OLLAMA_URL}/api/embed",
            json={"model": model, "input": texts[start : start + BATCH_SIZE]},
            timeout=600,
        )
        response.raise_for_status()
        vectors.extend(response.json()["embeddings"])
        if progress:
            print(f"  embeddings: {len(vectors)}/{len(texts)}", file=sys.stderr, flush=True)
    matrix = np.asarray(vectors, dtype=np.float32)
    norms = np.linalg.norm(matrix, axis=1, keepdims=True)
    return matrix / np.clip(norms, 1e-12, None)
