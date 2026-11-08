"""Extracción de texto de los PDF, página a página y sin cabeceras ni pies."""

from __future__ import annotations

import re
from dataclasses import dataclass
from pathlib import Path

import pymupdf

_DIAS = r"(LUNES|MARTES|MI[EÉ]RCOLES|JUEVES|VIERNES|S[AÁ]BADO|DOMINGO)"

# Líneas que el boletín repite en cada página y que no son contenido.
_RUIDO = [
    re.compile(p, re.IGNORECASE)
    for p in (
        r"BOLET[IÍ]N OFICIAL DEL ESTADO",
        r"BOLET[IÍ]N OFICIAL DE LA COMUNIDAD DE MADRID",
        r"BOCM",
        r"BOCM-\d+(-\d+)?",
        r"B\.O\.C\.M\. N[uú]m\. \d+",
        r"N[uú]m\. \d+",
        r"P[aá]g\. \d+",
        r"Sec\. [IVX]+\.?\s+P[aá]g\. \d+",
        _DIAS + r" \d+ DE \w+ DE \d{4}",
        r"cve: BOE-[A-Z0-9-]+",
        r"Verificable en https?://\S+",
        r"ISSN: \S+",
        r"D\. ?L\.: \S+",
        r"https?://www\.bocm\.es.*",
        r"Decreto \d+/\d{4}, de \d+ de \w+ \d+",
    )
]
_PAGINA_IMPRESA = re.compile(r"P[aá]g\. (\d+)", re.IGNORECASE)
_PIE_DECRETO = re.compile(r"Decreto \d+/\d{4}, de \d+ de \w+")


@dataclass(frozen=True)
class Page:
    number: int  # Página física del PDF, empezando en 1.
    printed: int | None  # Número impreso en el boletín.
    lines: tuple[str, ...]


def clean_line(line: str) -> str:
    line = re.sub(r"[   \xa0\t]", " ", line)
    return re.sub(r" {2,}", " ", line).strip()


def is_noise(line: str) -> bool:
    return any(p.fullmatch(line) for p in _RUIDO)


def _drop_split_footer(lines: list[str]) -> list[str]:
    """Quita el pie «Decreto N/AAAA, de D de M» cuando su número va en otra línea."""
    drop: set[int] = set()
    for i, line in enumerate(lines):
        if _PIE_DECRETO.fullmatch(line):
            for j in (i - 1, i + 1):
                if 0 <= j < len(lines) and lines[j].isdigit():
                    drop.update((i, j))
    return [l for i, l in enumerate(lines) if i not in drop]


def page_from_text(number: int, text: str) -> Page:
    lines = [clean_line(l) for l in text.splitlines()]
    lines = [l for l in lines if l]
    printed = None
    for line in lines:
        match = _PAGINA_IMPRESA.search(line)
        if match and is_noise(line):
            printed = int(match.group(1))
            break
    return Page(number, printed, tuple(_drop_split_footer([l for l in lines if not is_noise(l)])))


def extract_pages(path: Path) -> list[Page]:
    with pymupdf.open(path) as doc:
        return [
            page_from_text(i, page.get_text("text", sort=False))
            for i, page in enumerate(doc, 1)
        ]


def read_page(path: Path, number: int) -> Page:
    with pymupdf.open(path) as doc:
        if not 1 <= number <= doc.page_count:
            raise ValueError(f"La página debe estar entre 1 y {doc.page_count}.")
        return page_from_text(number, doc[number - 1].get_text("text", sort=False))
