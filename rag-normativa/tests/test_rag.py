import pytest

from rag_normativa.answer import NO_ENCONTRADO, validate_answer
from rag_normativa.chunking import Chunk, chunk_pages, normalize_text
from rag_normativa.extract import is_noise, page_from_text
from rag_normativa.retrieve import Hit, detect_curso, rrf, tokenize


def _hit(section="Artículo 1", page=3):
    chunk = Chunk("x-1", "decreto-65-eso", page, page, None, section, "", "", "", "Texto de prueba.")
    return Hit(chunk, 1.0)


def test_limpia_cabeceras_y_guarda_pagina_impresa():
    page = page_from_text(7, "BOLETÍN OFICIAL DEL ESTADO\nNúm. 340\nSec. I.   Pág. 122911\nTexto real")
    assert page.lines == ("Texto real",)
    assert page.printed == 122911
    assert is_noise("BOCM-20220726-2")
    assert not is_noise("Artículo 1. Objeto")


def test_quita_pie_de_decreto_con_numero_en_otra_linea():
    assert page_from_text(15, "Texto\nDecreto 65/2022, de 20 de julio\n15").lines == ("Texto",)
    assert page_from_text(15, "15\nDecreto 65/2022, de 20 de julio\nTexto").lines == ("Texto",)
    cita = "Según el\nDecreto 65/2022, de 20 de julio\nque regula"
    assert len(page_from_text(15, cita).lines) == 3


def test_detecta_articulos_y_conserva_paginas():
    pages = [
        page_from_text(3, "Artículo 1. Objeto\nEste decreto establece el currículo de la etapa completa."),
        page_from_text(4, "Artículo 2. Finalidad\nLa finalidad de la etapa consiste en lograr la formación."),
    ]
    chunks = chunk_pages("decreto-65-eso", pages)
    assert [(c.section, c.page_start) for c in chunks] == [("Artículo 1", 3), ("Artículo 2", 4)]


def test_detecta_materia_curso_y_bloque():
    text = (
        "ANEXO II\nMATEMÁTICAS\nIntroducción de la materia con texto suficiente para indexar.\n"
        "Competencias específicas.\n1. Interpretar problemas matemáticos de la vida cotidiana.\n"
        "1º ESO.\nCriterios de evaluación.\n1.1. Interpretar problemas organizando los datos dados.\n"
    )
    chunks = chunk_pages("decreto-65-eso", [page_from_text(30, text)])
    last = chunks[-1]
    assert (last.section, last.materia, last.curso, last.bloque) == (
        "Anexo II", "MATEMÁTICAS", "1º ESO", "Criterios de evaluación",
    )


def test_une_lineas_y_guiones_sin_romper_listas():
    assert normalize_text(["La profe-", "sión docente", "continúa"]) == "La profesión docente continúa"
    assert normalize_text(["Requisitos:", "a) Primero"]) == "Requisitos:\na) Primero"


def test_rrf_premia_coincidencias():
    scores = rrf([[1, 2], [2, 3]], k=60)
    assert max(scores, key=scores.get) == 2


@pytest.mark.parametrize("pregunta, esperado", [
    ("Criterios de Matemáticas de 2º de ESO", "2º ESO"),
    ("Contenidos de 2.º de la ESO", "2º ESO"),
    ("Contenidos de 4 ESO", "4º ESO"),
    ("Matemáticas en primero de la ESO", "1º ESO"),
    ("tercer curso de ESO", "3º ESO"),
    ("Contenidos de segundo de Bachillerato", "2º Bachillerato"),
    ("1º Bachillerato", "1º Bachillerato"),
    ("tercero de Bachillerato", None),
    ("¿Qué dice el artículo 2 de la ESO?", None),
    ("¿Cómo se organiza el horario lectivo?", None),
])
def test_detecta_curso_en_la_pregunta(pregunta, esperado):
    assert detect_curso(pregunta) == esperado


def test_tokenize_ignora_acentos_y_conserva_numeros():
    assert tokenize("El Artículo 28 de la Evaluación") == ["articulo", "28", "evaluacion"]


def test_expande_citas_validas():
    answer = validate_answer("La etapa dura cuatro cursos [F1].", [_hit()])
    assert "[decreto-65-eso, Artículo 1, p. 3]" in answer.text
    assert not answer.invalid_citations and not answer.uncited_paragraphs


def test_detecta_citas_inventadas_y_parrafos_sin_cita():
    answer = validate_answer("Dato [F9].\n\nOtro párrafo sin fuente.", [_hit()])
    assert answer.invalid_citations == ("F9",)
    assert len(answer.uncited_paragraphs) == 1


def test_reconoce_rechazo():
    answer = validate_answer(NO_ENCONTRADO, [_hit()])
    assert answer.refused and answer.text == NO_ENCONTRADO
