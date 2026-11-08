"""Catálogo de normas, rutas y parámetros del sistema."""

from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path

PROJECT_DIR = Path(__file__).resolve().parents[2]
REPO_DIR = PROJECT_DIR.parent
DATA_DIR = PROJECT_DIR / "data"

OLLAMA_URL = os.environ.get("OLLAMA_URL", "http://localhost:11434")
EMBEDDING_MODEL = os.environ.get("RAG_EMBEDDING_MODEL", "bge-m3")
DEFAULT_CHAT_MODEL = os.environ.get("RAG_CHAT_MODEL", "qwen3.5:35b-a3b")

MAX_CHUNK_CHARS = 1500
OVERLAP_CHARS = 200
DEFAULT_TOP_K = 8


@dataclass(frozen=True)
class Norma:
    id: str
    nombre: str
    archivo: str

    @property
    def path(self) -> Path:
        return REPO_DIR / self.archivo


NORMAS: tuple[Norma, ...] = (
    Norma(
        "lomloe",
        "Ley Orgánica 3/2020 (LOMLOE), BOE núm. 340, de 30 de diciembre de 2020",
        "BOE-A-2020-17264.pdf",
    ),
    Norma(
        "decreto-64-bach",
        "Decreto 64/2022 de la Comunidad de Madrid (Bachillerato), BOCM núm. 176",
        "Decreto-64-2022-Curriculum-de-Bachillerato_Madrid.pdf",
    ),
    Norma(
        "decreto-65-eso",
        "Decreto 65/2022 de la Comunidad de Madrid (ESO), BOCM núm. 176",
        "Decreto-65-2022_ordenacion-y-el-curriculo-ESO-en-CAM.pdf",
    ),
)

NORMAS_POR_ID = {n.id: n for n in NORMAS}
