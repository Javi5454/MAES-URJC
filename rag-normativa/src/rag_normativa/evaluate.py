"""Evaluación de la recuperación con preguntas de referencia."""

from __future__ import annotations

from pathlib import Path

import yaml

from .answer import generate
from .config import PROJECT_DIR
from .retrieve import Retriever

EVAL_FILE = PROJECT_DIR / "eval" / "preguntas.yaml"


def evaluate(path: Path = EVAL_FILE, k: int = 5, model: str | None = None) -> bool:
    items = yaml.safe_load(path.read_text(encoding="utf-8"))
    retriever = Retriever()
    answerable = [i for i in items if not i.get("sin_respuesta")]
    unanswerable = [i for i in items if i.get("sin_respuesta")]

    hits_ok = 0
    for item in answerable:
        hits = retriever.search(item["pregunta"], k=k)
        expected = set(item["paginas"])
        found = any(
            h.chunk.norma == item["norma"]
            and expected & set(range(h.chunk.page_start, h.chunk.page_end + 1))
            for h in hits
        )
        hits_ok += found
        print(f"{'OK ' if found else 'FALLO'} {item['pregunta']}")
        if not found:
            print("      obtenido:", "; ".join(h.chunk.cita for h in hits[:3]))
    print(f"\nhit@{k}: {hits_ok}/{len(answerable)} = {hits_ok / len(answerable):.0%}")

    if model:
        refused = 0
        for item in unanswerable:
            answer = generate(item["pregunta"], retriever.search(item["pregunta"]), model)
            refused += answer.refused
            print(f"{'OK ' if answer.refused else 'FALLO'} (sin respuesta) {item['pregunta']}")
        print(f"rechazos correctos: {refused}/{len(unanswerable)}")
    return hits_ok == len(answerable)
