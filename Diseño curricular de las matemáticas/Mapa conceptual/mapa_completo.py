"""Versión completa del mapa conceptual de la SA: todas las competencias, criterios, descriptores priorizados,
instrumentos, saberes, actividades, partes del producto, roles, recursos y medidas de atención a la diversidad.

Competencias, descriptores, criterios e instrumentos se leen de ../Situación de aprendizaje/matrices.py, de modo que
el mapa no puede contradecir las matrices. Cada criterio lleva en su caja los códigos de los instrumentos que lo
evalúan, para no llenar el mapa de enlaces cruzados. Genera, con mapa_motor.py:
  - Gomez_MapaSA_completo.cxl (CmapTools) y Gomez_MapaSA_completo.tex (TikZ, con glosas).
"""
import contextlib
import io
import runpy
from pathlib import Path

from mapa_motor import Mapa

HERE = Path(__file__).parent
PREGUNTA = "¿Cómo se articula mi situación de aprendizaje para que el alumnado aprenda de forma competencial?"
TITULO = "Medir lo que no se puede alcanzar: ¿dónde caben más paneles solares en nuestro instituto? (versión completa)"

# ---------------- Datos de las matrices ----------------
with contextlib.redirect_stdout(io.StringIO()):
    MAT = runpy.run_path(str(HERE.parent / "Situación de aprendizaje" / "matrices.py"))
COD = MAT["CODIGOS"]
INSTR_DE = {}
for _bloque, _cont, filas in MAT["GRUPOS"]:
    for crit, _bloom, _op, ins in filas:
        lista = INSTR_DE.setdefault(crit, [])
        lista += [COD[i] for i in ins if COD[i] not in lista]
DESC_DE = {n: sorted(pri) for n, (_t, _l, pri, _m) in MAT["CE"].items()}
NOMBRE_CE = {"1": "CE1 Modelizar", "2": "CE2 Verificar", "3": "CE3 Conjeturar", "5": "CE5 Conectar ideas",
             "6": "CE6 Conexiones\nextramatemáticas", "7": "CE7 Representar", "8": "CE8 Comunicar",
             "9": "CE9 Destrezas\nsocioafectivas"}
assert set(NOMBRE_CE) == set(MAT["CE"]), "faltan competencias"
clave = lambda c: [int(t) for t in c.split(".")]
CRITS_DE = {n: sorted([c for c in INSTR_DE if c.split(".")[0] == n], key=clave) for n in NOMBRE_CE}
assert sum(len(v) for v in CRITS_DE.values()) == len(INSTR_DE) == 16

# ---------------- Conceptos ----------------
C = {
    "sa": ("Situación de\naprendizaje", "marco", True),
    "ctx": ("Contexto", "marco", True),
    "ctx1": ("Ampliación solar\ndel instituto", "marco", False),
    # Saberes básicos: los bloques de la matriz
    "sab": ("Saberes básicos", "curr", True),
    "vec": ("Vectores", "curr", False),
    "tri": ("Trigonometría", "curr", False),
    "modz": ("Modelización", "curr", False),
    "triang": ("Resolución de\ntriángulos", "curr", False),
    "rec": ("Rectas", "curr", False),
    "energ": ("Energía solar", "curr", False),
    "actit": ("Actitudes y\naprendizaje", "curr", False),
    # Actividades: las 20 sesiones
    "act": ("Actividades", "acc", True),
    "s1": ("Presentación del\nreto (S1)", "acc", False),
    "f14": ("Talleres GeoGebra\nF1–F4", "acc", False),
    "expo": ("Exposiciones y\nejercicios (S3–S11)", "acc", False),
    "piezas": ("Piezas del reto", "acc", False),
    "s13": ("Mapa y\nmétodo (S13)", "acc", False),
    "med": ("Medimos el\ninstituto (S14)", "acc", False),
    "mod": ("Modelo de\nsombras (S15)", "acc", False),
    "s16": ("Propuesta y\ncoevaluación (S16)", "acc", False),
    "s17": ("Mejora y\nensayo (S17)", "acc", False),
    "s18": ("Prueba individual\n(S18)", "acc", False),
    "s19": ("Defensa final\n(S19–S20)", "acc", False),
    # Reto y producto
    "reto": ("Reto", "marco", True),
    "preg": ("¿Dónde caben\nmás paneles?", "marco", False),
    "ods": ("ODS", "marco", True),
    "ods711": ("ODS 7 y 11", "marco", False),
    "prod": ("Producto final", "marco", True),
    "libro": ("Libro de\nGeoGebra", "marco", False),
    "p1": ("Método y datos", "marco", False),
    "p2": ("Modelo dinámico", "marco", False),
    "p3": ("Análisis del error", "marco", False),
    "p5": ("Reflexión ODS\ny límites", "marco", False),
    "p6": ("Registro de\ncambios", "marco", False),
    "p7": ("Fuentes y autoría", "marco", False),
    "p4": ("Propuesta de\nampliación", "marco", False),
    # Evaluación
    "eval": ("Evaluación", "eval", True),
    "evid": ("Evidencias", "eval", True),
    "hoja": ("Hoja de datos", "eval", False),
    "kanban": ("Tablero Kanban", "eval", False),
    "relevo": ("Hojas de relevo", "eval", False),
    "agentes": ("Hetero, co y\nautoevaluación", "eval", False),
    "inst": ("Instrumentos", "eval", True),
    "EX": ("Examen escrito\n(EX)", "eval", False),
    "CU": ("Cuestionarios\nQ1–Q4 (CU)", "eval", False),
    "FI": ("Fichas GeoGebra\nR4 (FI)", "eval", False),
    "LI": ("Rúbrica R1\nlibro (LI)", "eval", False),
    "EP": ("Rúbrica R2\ndefensa (EP)", "eval", False),
    "MC": ("Lista L2\nmapa (MC)", "eval", False),
    "OB": ("Lista L1\nobservación (OB)", "eval", False),
    "CO": ("Rúbrica R3\nco/auto (CO)", "eval", False),
    # Competencias, con sus descriptores priorizados y sus criterios
    "ce": ("Competencias\nespecíficas", "curr", True),
    # Metodología
    "met": ("Metodología", "acc", True),
    "abr": ("Aprendizaje\nbasado en retos", "acc", False),
    "mag": ("Sesiones\nmagistrales", "acc", False),
    "coop": ("Trabajo\ncooperativo", "acc", False),
    "etw": ("Proyecto\neTwinning", "acc", False),
    "roles": ("Cuatro roles\nrotatorios", "acc", False),
    "r_coord": ("Coordinación", "acc", False),
    "r_med": ("Medición", "acc", False),
    "r_mod": ("Modelo", "acc", False),
    "r_com": ("Comunicación", "acc", False),
    "lat": ("Sombras en\notra latitud", "acc", False),
    "recu": ("Recursos", "acc", True),
    "clin": ("Clinómetro", "acc", False),
    "cinta": ("Cinta métrica", "acc", False),
    "ggb": ("GeoGebra", "acc", False),
    "pvgis": ("PVGIS", "acc", False),
    "noaa": ("Calculadora NOAA", "acc", False),
    "twin": ("TwinSpace", "acc", False),
    "div": ("Atención a la\ndiversidad", "acc", True),
    "dua": ("Pautas DUA", "acc", False),
    "refz": ("Refuerzo por\ncriterio (S13)", "acc", False),
    "ampl": ("Ampliación:\nradio terrestre", "acc", False),
}
for n in NOMBRE_CE:
    C[f"ce{n}"] = (f"{NOMBRE_CE[n]}\n({' · '.join(DESC_DE[n])})", "curr", False)
    C[f"cr{n}"] = ("\n".join(f"{c}: {' · '.join(INSTR_DE[c])}" for c in CRITS_DE[n]), "curr", False)

m = Mapa(C, TITULO, PREGUNTA, "Gomez_MapaSA_completo", max_palabras=30)

# ---------------- Disposición ----------------
Y1, Y2 = 2.2, 4.4
FILAS = [4.1 + 1.4 * k for k in range(11)]  # filas de las actividades
ACT = ["s1", "f14", "expo", "piezas", "s13", "med", "mod", "s16", "s17", "s18", "s19"]
SAB = [("vec", 1), ("tri", 2), ("modz", 3), ("triang", 5), ("rec", 6), ("energ", 7), ("actit", 8)]

m.pon("ctx", 1.6, Y1 - 0.9); m.pon("ctx1", 1.6, Y2)
m.pon("sab", 5.0, Y1)
m.pila([s for s, _ in SAB], 5.45, "R", 0, ys=[FILAS[k] for _, k in SAB])
m.pon("act", 16.25, Y1)
m.pila(ACT, 15.8, "L", 0, ys=FILAS)
m.pon("reto", 21.4, Y1); m.pon("ods", 18.8, Y2); m.pon("ods711", 18.8, 6.0); m.pon("preg", 24.2, Y2)
m.pon("prod", 21.4, 6.6); m.pon("libro", 21.4, 8.8)
m.pila(["p1", "p2", "p3", "p5", "p6", "p7", "p4"], 21.85, "R", 0, ys=[10.7 + 1.4 * k for k in range(7)])
m.pon("eval", 30.4, Y1); m.pon("evid", 27.6, Y2); m.pon("agentes", 31.0, Y2); m.pon("inst", 34.6, Y2)
m.columna(["hoja", "kanban", "relevo"], 28.05, "R", 6.3, 1.15)
m.columna(["EX", "CU", "FI", "LI", "EP", "MC", "OB", "CO"], 35.05, "R", 6.3, 1.4)
# Competencias: cada fila, la competencia (con sus descriptores) y la caja de sus criterios
m.pon("ce", 39.6, Y1)
y = 3.8
for n in NOMBRE_CE:
    h = max(len(C[f"ce{n}"][0].split("\n")), len(C[f"cr{n}"][0].split("\n"))) * 0.4 + 0.3
    m.columna([f"ce{n}"], 40.05, "R", y + h / 2, 0)
    m.columna([f"cr{n}"], 48.9, "R", y + h / 2, 0)
    y += h + 0.4
m.pon("met", 62.5, Y1)
for cid, x in (("abr", 55.7), ("mag", 58.6), ("coop", 61.3), ("etw", 63.95), ("recu", 66.7), ("div", 71.7)):
    m.pon(cid, x, Y2)
m.pon("roles", 61.3, 6.6); m.columna(["r_coord", "r_med", "r_mod", "r_com"], 61.75, "R", 8.3, 1.1)
m.pon("lat", 63.95, 6.6)
m.columna(["clin", "cinta", "ggb", "pvgis", "noaa", "twin"], 67.15, "R", 6.3, 1.15)
m.columna(["dua", "refz", "ampl"], 72.15, "R", 6.3, 1.4)
m.XC = (m.POS["ctx"][0] + m.POS["div"][0]) / 2
m.pon("sa", m.XC, 0)
m.YL = 21.4

# ---------------- Proposiciones ----------------
LISTA = ("lista",)
P = [
    ("sa", "parte del", ["ctx"], False, ("t", 0.5)),
    ("sa", "moviliza", ["sab"], False, ("t", 0.45)),
    ("sa", "se desarrolla mediante", ["act"], False, ("t", 0.55)),
    ("sa", "se articula en torno al", ["reto"], False, ("t", 0.35)),
    ("sa", "se comprueba mediante", ["eval"], False, ("t", 0.6)),
    ("sa", "desarrolla", ["ce"], False, ("t", 0.6)),
    ("sa", "se apoya en", ["met"], False, ("t", 0.5)),
    ("ctx", "se concreta en", ["ctx1"], False, None),
    ("sab", "incluyen", [s for s, _ in SAB], False, LISTA),
    ("act", "se concretan en", ACT, False, LISTA),
    ("reto", "contribuye a los", ["ods"], False, ("t", 0.6)),
    ("reto", "se formula como", ["preg"], False, ("t", 0.6)),
    ("reto", "da lugar al", ["prod"], False, ("t", 0.5)),
    ("ods", "se concretan en", ["ods711"], False, None),
    ("prod", "se concreta en", ["libro"], False, None),
    ("libro", "incluye", ["p1", "p2", "p3", "p5", "p6", "p7", "p4"], False, LISTA),
    ("eval", "se apoya en", ["evid"], False, ("t", 0.6)),
    ("eval", "combina", ["agentes"], False, ("t", 0.55)),
    ("eval", "se realiza con", ["inst"], False, ("t", 0.6)),
    ("evid", "incluyen", ["hoja", "kanban", "relevo"], False, LISTA),
    ("inst", "incluyen", ["EX", "CU", "FI", "LI", "EP", "MC", "OB", "CO"], False, LISTA),
    ("ce", "incluyen", [f"ce{n}" for n in NOMBRE_CE], False, LISTA),
    ("met", "combina", ["abr", "mag", "coop"], False, ("p", 59.4, 3.25)),
    ("met", "desarrolla un", ["etw"], False, ("t", 0.4)),
    ("met", "utiliza", ["recu"], False, ("t", 0.6)),
    ("met", "incluye", ["div"], False, ("t", 0.35)),
    ("coop", "se organiza en", ["roles"], False, None),
    ("roles", "rotan entre", ["r_coord", "r_med", "r_mod", "r_com"], False, ("lista", 0.95)),
    ("etw", "compara", ["lat"], False, None),
    ("recu", "incluyen", ["clin", "cinta", "ggb", "pvgis", "noaa", "twin"], False, LISTA),
    ("div", "se concreta en", ["dua", "refz", "ampl"], False, LISTA),
]
for n in NOMBRE_CE:
    P.append((f"ce{n}", "se evalúa con los criterios", [f"cr{n}"], False, ("cruce", "right", "left")))
P += [
    # Enlaces cruzados entre ramas (discontinuos)
    ("vec", "se construyen en", ["f14"], True, ("cruce", "right", "left")),
    ("tri", "se trabaja en", ["expo"], True, ("cruce", "right", "left")),
    ("modz", "se desarrolla en", ["piezas"], True, ("cruce", "right", "left")),
    ("triang", "se aplica en", ["med"], True, ("cruce", "right", "left")),
    ("rec", "se aplican en", ["mod"], True, ("cruce", "right", "left")),
    ("energ", "se aplica en la", ["s16"], True, ("cruce", "right", "left")),
    ("actit", "se trabajan en", ["s17"], True, ("cruce", "right", "left")),
    ("mod", "se recoge en el", ["libro"], True, ("cruce", "right", "left")),
    ("libro", "aporta la evidencia de", ["evid"], True, ("cruce", "right", "bottom", 0.6)),
    ("p4", "se defiende en la", ["s19"], True, ("cruce", "left", "right")),
    ("roles", "se evalúan con los", ["cr9"], True, ("cruce", "left", "right", 0.5)),
]
m.P = P

m.GLOSAS = [
    ("cada saber se aplica\nen una actividad", 8.6, 17.6),
    ("el producto es\nla evidencia", 25.9, 9.0),
    ("cada criterio lleva los códigos\nde sus instrumentos", 50.6, 19.4),
    ("el trabajo cooperativo\nse evalúa con el criterio 9.3", 57.4, 15.6),
]
m.leyenda_extra = ("Instrumentos: EX examen · CU cuestionarios · FI fichas · LI libro y propuesta · EP exposición · "
                   "MC mapa conceptual · OB observación · CO co/autoevaluación. Entre paréntesis, en cada competencia, "
                   "sus descriptores operativos priorizados.")
m.escribir(HERE, "Gomez_MapaSA_completo.cxl", "Gomez_MapaSA_completo.tex")
