"""Interfaz de línea de comandos."""

from __future__ import annotations

import argparse
import sys

import requests

from .config import DEFAULT_CHAT_MODEL, DEFAULT_TOP_K, NORMAS, NORMAS_POR_ID
from .index import IndexNotBuilt


def _filters(parser: argparse.ArgumentParser) -> None:
    parser.add_argument("consulta")
    parser.add_argument("--norma", choices=sorted(NORMAS_POR_ID))
    parser.add_argument("--materia", help='Por ejemplo: "matemáticas"')
    parser.add_argument("--curso", help='Por ejemplo: "1º ESO" o "2º Bachillerato"')
    parser.add_argument("-k", type=int, default=DEFAULT_TOP_K)


def _search(args: argparse.Namespace):
    from .retrieve import Retriever

    return Retriever().search(args.consulta, args.norma, args.materia, args.curso, args.k)


def cmd_index(_: argparse.Namespace) -> int:
    from .index import build_index

    print(f"Índice creado con {len(build_index())} fragmentos.")
    return 0


def cmd_search(args: argparse.Namespace) -> int:
    hits = _search(args)
    if not hits:
        print("Sin resultados.")
    for i, hit in enumerate(hits, 1):
        print(f"\n[{i}] {hit.chunk.cita}  (score {hit.score:.4f})\n{hit.chunk.text}")
    return 0


def cmd_ask(args: argparse.Namespace) -> int:
    from .answer import generate

    answer = generate(args.consulta, _search(args), args.model)
    print(answer.text)
    if answer.cited:
        print("\nFuentes:")
        for hit in answer.cited:
            print(f"- {hit.chunk.cita}")
    if answer.invalid_citations:
        print(f"\nAVISO: citas inexistentes: {', '.join(answer.invalid_citations)}", file=sys.stderr)
    if answer.uncited_paragraphs:
        print(f"\nAVISO: {len(answer.uncited_paragraphs)} párrafo(s) sin cita; revísalos.", file=sys.stderr)
    return 1 if answer.invalid_citations else 0


def cmd_evaluate(args: argparse.Namespace) -> int:
    from .evaluate import evaluate

    return 0 if evaluate(k=args.k, model=args.model) else 1


def cmd_normas(_: argparse.Namespace) -> int:
    for norma in NORMAS:
        print(f"{norma.id}: {norma.nombre}")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(prog="rag-normativa", description=__doc__)
    sub = parser.add_subparsers(required=True)

    sub.add_parser("index", help="Construye el índice").set_defaults(func=cmd_index)
    sub.add_parser("normas", help="Lista las normas").set_defaults(func=cmd_normas)

    search = sub.add_parser("search", help="Busca fragmentos sin usar un modelo de chat")
    _filters(search)
    search.set_defaults(func=cmd_search)

    ask = sub.add_parser("ask", help="Responde con citas usando un modelo de Ollama")
    _filters(ask)
    ask.add_argument("--model", default=DEFAULT_CHAT_MODEL)
    ask.set_defaults(func=cmd_ask)

    evaluation = sub.add_parser("evaluate", help="Mide la calidad con eval/preguntas.yaml")
    evaluation.add_argument("-k", type=int, default=5)
    evaluation.add_argument("--model", help="Evalúa también los rechazos con este modelo")
    evaluation.set_defaults(func=cmd_evaluate)

    args = parser.parse_args()
    try:
        return args.func(args)
    except IndexNotBuilt as error:
        print(error, file=sys.stderr)
    except requests.ConnectionError:
        print("No puedo conectar con Ollama. ¿Está en marcha?", file=sys.stderr)
    except requests.HTTPError as error:
        print(f"Error de Ollama: {error}. ¿Has descargado el modelo?", file=sys.stderr)
    return 2


if __name__ == "__main__":
    sys.exit(main())
