"""Generación con modelos de Ollama y validación de las citas."""

from __future__ import annotations

import re
from dataclasses import dataclass

import requests

from .config import DEFAULT_CHAT_MODEL, OLLAMA_URL
from .retrieve import Hit

NO_ENCONTRADO = "No lo encuentro en estas normas."

SYSTEM_PROMPT = f"""Eres un asistente que responde preguntas sobre normativa educativa española.

Reglas obligatorias:
1. Usa únicamente los fragmentos proporcionados. No uses conocimiento externo.
2. Cada afirmación debe terminar con la cita de su fragmento, con el formato [F1] o [F1, F3].
3. No cites fragmentos que no respalden la afirmación.
4. Si los fragmentos no contienen la respuesta, contesta exactamente: "{NO_ENCONTRADO}"
5. Responde en español, con precisión y sin rodeos. Respeta la redacción normativa."""

_CITA = re.compile(r"\[(F\d+(?:\s*,\s*F\d+)*)\]")
_THINK = re.compile(r"<think>.*?</think>", re.DOTALL)


@dataclass(frozen=True)
class Answer:
    text: str
    cited: tuple[Hit, ...]
    invalid_citations: tuple[str, ...]
    uncited_paragraphs: tuple[str, ...]
    refused: bool


def build_context(hits: list[Hit]) -> str:
    return "\n\n".join(f"[F{i}] ({h.chunk.cita})\n{h.chunk.text}" for i, h in enumerate(hits, 1))


def validate_answer(raw: str, hits: list[Hit]) -> Answer:
    """Comprueba las citas y sustituye [F1] por la referencia legible."""
    raw = _THINK.sub("", raw).strip()
    if NO_ENCONTRADO.lower() in raw.lower():
        return Answer(NO_ENCONTRADO, (), (), (), True)

    used: dict[int, Hit] = {}
    invalid: list[str] = []

    def replace(match: re.Match[str]) -> str:
        labels = []
        for item in match.group(1).split(","):
            ref = item.strip()
            number = int(ref[1:])
            if 1 <= number <= len(hits):
                used[number] = hits[number - 1]
                labels.append(hits[number - 1].chunk.cita)
            else:
                invalid.append(ref)
                labels.append(f"{ref}: CITA NO VÁLIDA")
        return "[" + "; ".join(labels) + "]"

    paragraphs = [p for p in re.split(r"\n\s*\n", raw) if p.strip()]
    uncited = tuple(
        p for p in paragraphs
        if not _CITA.search(p) and not p.rstrip().endswith(":") and not p.lstrip().startswith("#")
    )
    return Answer(_CITA.sub(replace, raw), tuple(used[i] for i in sorted(used)), tuple(invalid), uncited, False)


def _chat(payload: dict) -> requests.Response:
    return requests.post(f"{OLLAMA_URL}/api/chat", json=payload, timeout=900)


def generate(question: str, hits: list[Hit], model: str = DEFAULT_CHAT_MODEL) -> Answer:
    if not hits:
        return Answer(NO_ENCONTRADO, (), (), (), True)
    payload = {
        "model": model,
        "stream": False,
        "think": False,
        "options": {"temperature": 0.1, "num_ctx": 16384},
        "messages": [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": f"Fragmentos:\n\n{build_context(hits)}\n\nPregunta: {question}"},
        ],
    }
    response = _chat(payload)
    if response.status_code == 400:  # Algunos modelos no admiten la opción "think".
        payload.pop("think")
        response = _chat(payload)
    response.raise_for_status()
    return validate_answer(response.json()["message"]["content"], hits)
