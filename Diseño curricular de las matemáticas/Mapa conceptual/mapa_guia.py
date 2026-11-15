"""Mapa conceptual de la SA adaptado a la guía de la profesora (Guia_AF_MapaConceptual_SA_MasterProf_2026_27_01).

Versión para entregar: selección de los elementos más representativos. Genera, con mapa_motor.py:
  - Gomez_MapaSA_masterprof_2026_2027.cxl: se importa en CmapTools y desde allí se guarda como .cmap y se exporta a PDF.
  - Gomez_MapaSA_anotado.tex: el mismo mapa en TikZ, con glosas breves junto a los enlaces cruzados.
"""
from pathlib import Path

from mapa_motor import Mapa

HERE = Path(__file__).parent
PREGUNTA = "¿Cómo se articula mi situación de aprendizaje para que el alumnado aprenda de forma competencial?"
TITULO = "Medir lo que no se puede alcanzar: ¿dónde caben más paneles solares en nuestro instituto?"

# id: (etiqueta, familia, genérico)
C = {
    "sa":    ("Situación de\naprendizaje", "marco", True),
    "ctx":   ("Contexto", "marco", True),
    "ctx1":  ("Ampliación solar\ndel instituto", "marco", False),
    "sab":   ("Saberes básicos", "curr", True),
    "vec":   ("Vectores (A)", "curr", False),
    "tri":   ("Trigonometría (B)", "curr", False),
    "rec":   ("Rectas (C)", "curr", False),
    "act":   ("Actividades", "acc", True),
    "f14":   ("Talleres GeoGebra\nF1–F4", "acc", False),
    "med":   ("Medimos el\ninstituto (S14)", "acc", False),
    "mod":   ("Modelo de\nsombras (S15)", "acc", False),
    "reto":  ("Reto", "marco", True),
    "preg":  ("¿Dónde caben\nmás paneles?", "marco", False),
    "ods":   ("ODS", "marco", True),
    "ods711":("ODS 7 y 11", "marco", False),
    "prod":  ("Producto final", "marco", True),
    "libro": ("Libro de\nGeoGebra", "marco", False),
    "prop":  ("Propuesta de\nampliación", "marco", False),
    "eval":  ("Evaluación", "eval", True),
    "evid":  ("Evidencias", "eval", True),
    "hoja":  ("Hoja de datos", "eval", False),
    "inst":  ("Instrumentos", "eval", True),
    "r1":    ("Rúbrica R1\n(libro)", "eval", False),
    "r2":    ("Rúbrica R2\n(defensa)", "eval", False),
    "l1":    ("Lista L1\n(observación)", "eval", False),
    "ce":    ("Competencias\nespecíficas", "curr", True),
    "crit":  ("Criterios de\nevaluación", "curr", True),
    "c11":   ("Criterio 1.1", "curr", False),
    "c61":   ("Criterio 6.1", "curr", False),
    "c93":   ("Criterio 9.3", "curr", False),
    "ce1":   ("CE1 Modelizar", "curr", False),
    "ce6":   ("CE6 Conexiones\nextramatemáticas", "curr", False),
    "ce9":   ("CE9 Trabajo\nen equipo", "curr", False),
    "desc":  ("Descriptores\noperativos", "curr", True),
    "stem3": ("STEM3", "curr", False),
    "cc4":   ("CC4", "curr", False),
    "cps":   ("CPSAA3.2", "curr", False),
    "met":   ("Metodología", "acc", True),
    "abr":   ("Aprendizaje\nbasado en retos", "acc", False),
    "mag":   ("Sesiones\nmagistrales", "acc", False),
    "coop":  ("Trabajo\ncooperativo", "acc", False),
    "roles": ("Roles\nrotatorios", "acc", False),
    "recu":  ("Recursos", "acc", True),
    "clin":  ("Clinómetro\ny GeoGebra", "acc", False),
    "div":   ("Atención a la\ndiversidad", "acc", True),
    "ref":   ("Refuerzo por\ncriterio (S13)", "acc", False),
}

m = Mapa(C, TITULO, PREGUNTA, "Gomez_MapaSA_masterprof_2026_2027")

# ---------------- Disposición ----------------
Y1, Y2 = 2.2, 4.4


m.pon("ctx", 1.6, Y1 - 0.9); m.pon("ctx1", 1.6, Y2)
m.pon("sab", 5.0, Y1); m.columna(["vec", "tri", "rec"], 5.45, "R", 4.1, 1.4)
m.pon("act", 15.6, Y1); m.columna(["f14", "med", "mod"], 15.15, "L", 4.1, 1.4)
m.pon("reto", 20.6, Y1); m.pon("preg", 18.0, Y2); m.pon("ods", 23.0, Y2); m.pon("ods711", 23.0, 6.0)
m.pon("prod", 20.6, 7.2); m.pon("libro", 20.6, 9.4); m.pon("prop", 20.6, 11.6)
m.pon("eval", 27.8, Y1); m.pon("evid", 25.6, Y2); m.pon("hoja", 26.4, 6.0)
m.pon("inst", 29.6, Y2); m.columna(["r1", "r2", "l1"], 30.05, "R", 6.3, 1.4)
m.pon("crit", 38.75, Y2); m.columna(["c11", "c61", "c93"], 38.3, "L", 6.3, 1.4)
m.pon("ce", 42.2, Y1); m.columna(["ce1", "ce6", "ce9"], 42.65, "R", 4.1, 1.4)
m.pon("desc", 49.2, Y2); m.columna(["stem3", "cc4", "cps"], 49.65, "R", 6.2, 1.4)
m.pon("met", 57.0, Y1); m.columna(["abr", "mag", "coop"], 56.55, "L", 4.1, 1.4)
m.pon("roles", m.POS["coop"][0], 9.0)
m.pon("recu", 60.2, Y2); m.pon("clin", 60.2, 6.1)
m.pon("div", 63.6, Y2); m.pon("ref", 63.6, 6.1)
m.XC = (m.POS["ctx"][0] + m.POS["div"][0]) / 2
m.pon("sa", m.XC, 0)
m.YL = 13.4

# ---------------- Proposiciones ----------------
LISTA = ("lista",)
P = [
    ("sa", "parte del", ["ctx"], False, ("t", 0.5)),
    ("sa", "moviliza", ["sab"], False, ("t", 0.45)),
    ("sa", "se desarrolla mediante", ["act"], False, ("t", 0.5)),
    ("sa", "se articula en torno al", ["reto"], False, ("t", 0.32)),
    ("sa", "se comprueba mediante", ["eval"], False, ("t", 0.72)),
    ("sa", "desarrolla", ["ce"], False, ("t", 0.5)),
    ("sa", "se apoya en", ["met"], False, ("t", 0.5)),
    ("ctx", "se concreta en", ["ctx1"], False, None),
    ("sab", "incluyen, entre otros,", ["vec", "tri", "rec"], False, LISTA),
    ("act", "incluyen, entre otras,", ["f14", "med", "mod"], False, LISTA),
    ("reto", "se formula como", ["preg"], False, ("t", 0.6)),
    ("reto", "contribuye a los", ["ods"], False, ("t", 0.6)),
    ("reto", "da lugar al", ["prod"], False, ("t", 0.5)),
    ("ods", "se concretan en", ["ods711"], False, None),
    ("prod", "se concreta en", ["libro"], False, None),
    ("libro", "recoge la", ["prop"], False, None),
    ("eval", "se apoya en", ["evid"], False, ("t", 0.6)),
    ("eval", "se realiza con", ["inst"], False, ("t", 0.6)),
    ("evid", "incluyen", ["hoja"], False, ("t", 0.45)),
    ("inst", "incluyen, entre otros,", ["r1", "r2", "l1"], False, LISTA),
    ("ce", "se evalúan con", ["crit"], False, ("t", 0.63)),
    ("ce", "incluyen, entre otras,", ["ce1", "ce6", "ce9"], False, ("lista", 0.86)),
    ("ce", "contribuyen a los", ["desc"], False, ("p", 46.6, 3.2)),
    ("crit", "incluyen, entre otros,", ["c11", "c61", "c93"], False, LISTA),
    ("desc", "incluyen, entre otros,", ["stem3", "cc4", "cps"], False, LISTA),
    ("met", "combina", ["abr", "mag", "coop"], False, LISTA),
    ("met", "utiliza", ["recu"], False, None),
    ("met", "incluye", ["div"], False, None),
    ("coop", "se organiza en", ["roles"], False, None),
    ("recu", "incluyen", ["clin"], False, None),
    ("div", "se concreta en", ["ref"], False, None),
    # Enlaces cruzados entre ramas (discontinuos)
    ("vec", "se construyen en", ["f14"], True, ("cruce", "right", "left")),
    ("tri", "se aplica en", ["med"], True, ("cruce", "right", "left")),
    ("rec", "se aplican en", ["mod"], True, ("cruce", "right", "left")),
    ("mod", "se recoge en el", ["libro"], True, ("cruce", "bottom", "left")),
    ("libro", "aporta la evidencia de", ["evid"], True, ("cruce", "right", "bottom", 0.6)),
    ("c11", "se evalúa mediante", ["r1"], True, ("cruce", "left", "right")),
    ("c61", "se evalúa mediante", ["r2"], True, ("cruce", "left", "right")),
    ("c93", "se evalúa mediante", ["l1"], True, ("cruce", "left", "right")),
    ("roles", "movilizan el", ["cps"], True, ("cruce", "left", "right")),
]

m.P = P

# Glosas de la versión LaTeX: explican, junto a los enlaces cruzados, por qué el diseño está alineado
GLOSAS = [
    ("cada saber se aplica\nen una actividad", 10.3, 8.1),
    ("el producto es\nla evidencia", 24.6, 8.6),
    ("cada criterio,\nsu instrumento", 34.9, 10.6),
    ("el cooperativo moviliza\nun descriptor", 53.6, 10.3),
]

m.GLOSAS = GLOSAS
m.notas_leyenda = r" \quad \emph{entre otros}: se muestra una selección; la relación completa está en las matrices de la situación de aprendizaje"
m.escribir(HERE, "Gomez_MapaSA_masterprof_2026_2027.cxl", "Gomez_MapaSA_anotado.tex")
