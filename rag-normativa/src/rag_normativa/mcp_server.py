"""Servidor MCP: expone la búsqueda en las normas a Claude y otros clientes."""

from __future__ import annotations

from mcp.server.fastmcp import FastMCP

from .config import DEFAULT_TOP_K, NORMAS, NORMAS_POR_ID
from .extract import read_page
from .retrieve import Retriever

mcp = FastMCP(
    "rag-normativa",
    instructions=(
        "Busca en la LOMLOE y en los decretos 64/2022 (Bachillerato) y 65/2022 (ESO) de Madrid. "
        "Responde solo con lo que devuelvan las herramientas, cita cada afirmación con el campo "
        "'cita' y di que no lo encuentras si los resultados no lo respaldan."
    ),
)

_retriever: Retriever | None = None


def _get_retriever() -> Retriever:
    global _retriever
    if _retriever is None:
        _retriever = Retriever()
    return _retriever


@mcp.tool()
def listar_normas() -> list[dict]:
    """Lista las normas disponibles y el identificador de cada una."""
    return [{"id": n.id, "nombre": n.nombre} for n in NORMAS]


@mcp.tool()
def buscar_normativa(
    consulta: str,
    norma: str | None = None,
    materia: str | None = None,
    curso: str | None = None,
    k: int = DEFAULT_TOP_K,
) -> list[dict]:
    """Busca fragmentos relevantes. Cita cada afirmación con el campo 'cita' del resultado.

    Args:
        consulta: Pregunta o términos de búsqueda, incluidas referencias como "artículo 28".
        norma: Identificador opcional: lomloe, decreto-64-bach o decreto-65-eso.
        materia: Filtro opcional de materia, por ejemplo "matemáticas".
        curso: Filtro opcional de curso, por ejemplo "3º ESO" o "1º Bachillerato".
        k: Número de fragmentos (entre 1 y 30).
    """
    if norma and norma not in NORMAS_POR_ID:
        raise ValueError(f"Norma desconocida. Opciones: {', '.join(NORMAS_POR_ID)}")
    hits = _get_retriever().search(consulta, norma, materia, curso, max(1, min(k, 30)))
    return [
        {
            "cita": h.chunk.cita,
            "norma": h.chunk.norma,
            "pagina_pdf": h.chunk.page_start,
            "pagina_boletin": h.chunk.printed_start,
            "texto": h.chunk.text,
        }
        for h in hits
    ]


@mcp.tool()
def leer_pagina(norma: str, pagina: int) -> dict:
    """Devuelve el texto completo de una página del PDF para verificar una cita.

    Args:
        norma: Identificador: lomloe, decreto-64-bach o decreto-65-eso.
        pagina: Número de página física del PDF, empezando en 1.
    """
    if norma not in NORMAS_POR_ID:
        raise ValueError(f"Norma desconocida. Opciones: {', '.join(NORMAS_POR_ID)}")
    page = read_page(NORMAS_POR_ID[norma].path, pagina)
    return {
        "cita": f"{norma}, p. {page.number}",
        "pagina_boletin": page.printed,
        "texto": "\n".join(page.lines),
    }


def main() -> None:
    mcp.run()


if __name__ == "__main__":
    main()
