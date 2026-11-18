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

from mapa_motor import Mapa, W

HERE = Path(__file__).parent
PREGUNTA = "¿Cómo se articula mi situación de aprendizaje para que el alumnado aprenda de forma competencial?"
TITULO = "Medir lo que no se puede alcanzar: ¿dónde caben más paneles solares en nuestro instituto?"

# ---------------- Datos de las matrices ----------------
with contextlib.redirect_stdout(io.StringIO()):
    MAT = runpy.run_path(str(HERE.parent / "Situación de aprendizaje" / "matrices.py"))
COD = MAT["CODIGOS"]
INSTR_DE = {}
for _bloque, _cont, filas in MAT["GRUPOS"]:
    for crit, _bloom, _op, ins in filas:
        lista = INSTR_DE.setdefault(crit, [])
        lista += [COD[i] for i in ins if COD[i] not in lista]
# FI (fichas) se sustituye por la ficha concreta que evalúa cada criterio, según la tabla de andamiaje (§6.4)
import re
_and = (HERE.parent / "Situación de aprendizaje" / "secciones" / "06_reto_producto.tex").read_text(encoding="utf-8")
_fila = re.search(r"^\s*Criterios & (.+?) \\\\\s*$", _and, re.M).group(1).split(" & ")
assert len(_fila) == 4, _fila
FICHAS_DE = {}
for k, crits in enumerate(_fila, 1):
    for c in crits.split(", "):
        FICHAS_DE.setdefault(c.strip(), []).append(f"F{k}")
assert set(FICHAS_DE) == {c for c, ins in INSTR_DE.items() if "FI" in ins}, "fichas y matrices no coinciden"
for c, ins in INSTR_DE.items():
    if "FI" in ins:
        i = ins.index("FI")
        INSTR_DE[c] = ins[:i] + FICHAS_DE[c] + ins[i + 1:]
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
    "ctx_cur": ("1.º de Bachillerato\n(Ciencias y Tecnología)", "marco", False),
    "ctx_cam": ("Comunidad de Madrid", "marco", False),
    "ctx_mat": ("Matemáticas I", "marco", False),
    # Saberes básicos: los bloques de la matriz
    "sab": ("Saberes básicos", "curr", True),
    "vec": ("Vectores", "curr", False),
    "tri": ("Trigonometría", "curr", False),
    "modz": ("Modelización", "curr", False),
    "triang": ("Resolución de\ntriángulos", "curr", False),
    "rec": ("Rectas", "curr", False),
    "energ": ("Energía solar", "curr", False),
    "actit": ("Error y trabajo\nen equipo", "curr", False),
    # Actividades: las 20 sesiones
    "act": ("Actividades", "acc", True),
    "f_ini": ("Inicio", "acc", True),
    "f_des": ("Desarrollo", "acc", True),
    "f_cie": ("Cierre", "acc", True),
    "s1": ("Presentación del\nreto (S1)", "acc", False),
    "s2": ("Taller F1 y equipos\n(S2)", "acc", False),
    "s34": ("Magistral de vectores\n(S3 y S4)", "acc", False),
    "s5": ("Taller F2:\ngoniometría (S5)", "acc", False),
    "s67": ("Magistral de\ntrigonometría (S6 y S7)", "acc", False),
    "s89": ("Magistral de triángulos\n(S8 y S9, con F3)", "acc", False),
    "s1011": ("Magistral de rectas\n(S10 y S11)", "acc", False),
    "s12": ("Taller F4: rayo\ny sombra (S12)", "acc", False),
    "s13": ("Refuerzo, mapa\ny método (S13)", "acc", False),
    "med": ("Medimos el\ninstituto (S14)", "acc", False),
    "mod": ("Modelo de\nsombras (S15)", "acc", False),
    "s16": ("Propuesta y\ncoevaluación (S16)", "acc", False),
    "s17": ("Mejora y\nensayo (S17)", "acc", False),
    "s18": ("Examen individual\n(S18)", "acc", False),
    "s19": ("Defensa final\n(S19 y S20)", "acc", False),
    # Sentidos matemáticos (RD 243/2022) y, entre paréntesis, el bloque del Decreto 64/2022
    "sent": ("Sentidos matemáticos\n(RD 243/2022)", "curr", True),
    "sA": ("A. Sentido numérico\n(Números y\noperaciones)", "curr", False),
    "sB": ("B. Sentido de la\nmedida (Medida\ny geometría)", "curr", False),
    "sC": ("C. Sentido espacial\n(Geometría en el\nplano y el espacio)", "curr", False),
    "sD": ("D. Sentido\nalgebraico\n(Álgebra)", "curr", False),
    "sE": ("E. Sentido\nestocástico\n(Estadística)", "curr", False),
    "sF": ("F. Sentido\nsocioafectivo (Actitudes\ny aprendizaje)", "curr", False),
    # Reto y producto
    "reto": ("Reto", "marco", True),
    "preg": ("¿Dónde caben\nmás paneles?", "marco", False),
    # Lo que hace cada equipo, en orden (S13 a S20)
    "tarea": ("Tarea de cada equipo", "acc", True),
    "t1": ("1. Elige un edificio;\nel profesor aprueba\nsu método (S13)", "acc", False),
    "t2": ("2. Lo mide desde\nuno y dos puntos (S14)", "acc", False),
    "t3": ("3. Mide el bloque de\nviviendas desde dos\npuntos (S14)", "acc", False),
    "t4": ("4. Modela su sombra\nen GeoGebra (S15)", "acc", False),
    "t5": ("5. Calcula filas y paneles\ncon el criterio IDAE (S16)", "acc", False),
    "t6": ("6. Defiende la propuesta\nante la dirección (S19–S20)", "acc", False),
    "ods": ("ODS", "marco", True),
    "ods7": ("ODS 7: energía\nasequible y no\ncontaminante", "marco", False),
    "ods11": ("ODS 11: ciudades\ny comunidades\nsostenibles", "marco", False),
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
    "FI": ("Fichas GeoGebra\nF1–F4 (R4)", "eval", False),
    "LI": ("Rúbrica R1\nlibro (LI)", "eval", False),
    "EP": ("Rúbrica R2\ndefensa (EP)", "eval", False),
    "MC": ("Lista L2\nmapa (MC)", "eval", False),
    "OB": ("Lista L1\nobservación (OB)", "eval", False),
    "CO": ("Rúbrica R3\nco/auto (CO)", "eval", False),
    # Competencias, con sus descriptores priorizados y sus criterios
    "ce": ("Competencias\nespecíficas", "curr", True),
    "matr": ("Matrices de relación\ncurricular", "curr", True),
    # Metodología
    "met": ("Metodología", "acc", True),
    "abr": ("Aprendizaje\nbasado en retos", "acc", False),
    "mag": ("Sesiones\nmagistrales", "acc", False),
    "coop": ("Trabajo\ncooperativo", "acc", False),
    "etw": ("Proyecto\neTwinning", "acc", True),
    "roles": ("Cuatro roles\nrotatorios\n(formación en S2)", "acc", False),
    "r_coord": ("Coordinador", "acc", False),
    "r_med": ("Medidor", "acc", False),
    "r_mod": ("Modelador", "acc", False),
    "r_com": ("Comunicador", "acc", False),
    "lat": ("Sombras en\notra latitud", "acc", False),
    "recu": ("Recursos", "acc", True),
    "clin": ("Clinómetro", "acc", False),
    "cinta": ("Cinta métrica", "acc", False),
    "ggb": ("GeoGebra", "acc", False),
    "pvgis": ("PVGIS", "acc", False),
    "noaa": ("Calculadora NOAA", "acc", False),
    "twin": ("TwinSpace", "acc", False),
    "div": ("Atención a la\ndiversidad", "acc", True),
    # Diseño Universal para el Aprendizaje: los tres principios, cada uno con su medida (SA, §8)
    "imp": ("Principio de\nimplicación", "acc", False),
    "rep": ("Principio de\nrepresentación", "acc", False),
    "accx": ("Principio de acción\ny expresión", "acc", False),
    "imp1": ("Elección del objeto\na medir (paso 1)", "acc", False),
    "rep1": ("Explicación, construcción\ndinámica y material escrito", "acc", False),
    "acc1": ("Productos variados: libro,\nexposición, escrito, mapa", "acc", False),
    "refz": ("Refuerzo por\ncriterio (S13)", "acc", False),
    "ampl": ("Ampliación:\nradio terrestre", "acc", False),
    # Criterio 1.1, el de mayor peso en la calificación, desglosado en proposiciones (Decreto 64/2022)
    "k_est": ("Estrategias y\nherramientas", "curr", False),
    "k_mod": ("Modelización y\nresolución de problemas", "curr", False),
    "k_efi": ("Eficiencia en\ncada caso", "curr", False),
    "k_dig": ("Herramientas\ndigitales", "curr", False),
    "k_cie": ("Ciencia y\ntecnología", "curr", False),
    "k_vid": ("Vida cotidiana", "curr", False),
}
# Descriptores operativos priorizados: un concepto por descriptor, aunque lo compartan varias competencias
ORDEN_DESC = []
etiqueta_desc = lambda d: "CE3 emprendedora" if d == "CE3" else d
for n in NOMBRE_CE:  # dentro de cada competencia, de más estrecho a más ancho, para que las flechas no se crucen
    ORDEN_DESC += sorted([d for d in DESC_DE[n] if d not in ORDEN_DESC], key=lambda d: len(etiqueta_desc(d)))
did = lambda d: "d_" + d.replace(".", "_")
for d in ORDEN_DESC:
    C[did(d)] = (etiqueta_desc(d), "curr", False)
for n in NOMBRE_CE:
    C[f"ce{n}"] = (NOMBRE_CE[n], "curr", False)
    C[f"cr{n}"] = ("\n".join(f"{c}: {' · '.join(INSTR_DE[c])}" for c in CRITS_DE[n]), "curr", False)

m = Mapa(C, TITULO, PREGUNTA, "Gomez_MapaSA_completo", max_palabras=30)
m.MX = 4.6  # margen izquierdo del CXL: el contexto ocupa x negativas

# ---------------- Disposición ----------------
Y1, Y2 = 2.2, 4.4
FILAS = [4.1 + 1.4 * k for k in range(len(["s1", "s2", "s34", "s5", "s67", "s89", "s1011", "s12", "s13", "med", "mod", "s16", "s17", "s18", "s19"]))]  # filas de las actividades
ACT = ["s1", "s2", "s34", "s5", "s67", "s89", "s1011", "s12", "s13", "med", "mod", "s16", "s17", "s18", "s19"]
SAB = [("vec", 2), ("tri", 4), ("triang", 5), ("rec", 6), ("modz", 7), ("energ", 11), ("actit", 12)]

m.pon("ctx", 1.6, Y1 - 0.9)
m.pila(["ctx_mat", "ctx_cur", "ctx_cam", "ctx1"], 1.15, "L", 2.6, sep=0.3)
m.pon("sab", 5.0, Y1)
m.pila([s for s, _ in SAB], 5.45, "R", 0, ys=[FILAS[k] for _, k in SAB])
m.pon("act", 16.25, Y1)
m.pila(ACT, 15.8, "L", 0, ys=FILAS)
m.pon("reto", 21.4, Y1); m.pon("ods", 20.05, Y2); m.columna(["ods7", "ods11"], 19.6, "L", 6.5, 1.85); m.pon("preg", 24.8, Y2)
m.pon("prod", 22.0, 6.6); m.pon("libro", 22.0, 8.8)
m.pon("tarea", 28.0, 11.0)
m.pila(["t1", "t2", "t3", "t4", "t5", "t6"], 28.45, "R", 12.5, sep=0.35)
m.pila(["p1", "p2", "p3", "p5", "p6", "p7", "p4"], 22.45, "R", 0, ys=[10.7 + 1.4 * k for k in range(7)])
m.pon("eval", 30.4, Y1); m.pon("evid", 27.6, Y2); m.pon("agentes", 31.0, Y2); m.pon("inst", 34.6, Y2)
m.columna(["hoja", "kanban", "relevo"], 28.05, "R", 6.3, 1.15)
m.columna(["EX", "CU", "FI", "LI", "EP", "MC", "OB", "CO"], 35.05, "R", 6.3, 1.4)
# Competencias: cada fila, la competencia y la caja de sus criterios; sus descriptores, en una columna a la izquierda
m.pon("ce", 39.6, Y1)
y = 3.8
for n in NOMBRE_CE:
    h = max(len(C[f"ce{n}"][0].split("\n")), len(C[f"cr{n}"][0].split("\n"))) * 0.4 + 0.3
    m.columna([f"ce{n}"], 40.05, "R", y + h / 2, 0)
    m.columna([f"cr{n}"], 48.9, "R", y + h / 2, 0)
    y += h + 0.4
m.pon("met", 62.5, Y1)
for cid, x in (("abr", 55.7), ("mag", 58.6), ("coop", 61.3), ("etw", 64.4), ("recu", 66.7), ("div", 71.7)):
    m.pon(cid, x, Y2)
m.pon("roles", 61.3, 6.6); m.columna(["r_coord", "r_med", "r_mod", "r_com"], 61.75, "R", 8.6, 1.1)
m.pon("lat", 64.4, 6.6)
m.columna(["clin", "cinta", "ggb", "pvgis", "noaa", "twin"], 67.15, "R", 6.3, 1.15)
m.columna(["imp", "rep", "accx", "refz", "ampl"], 72.15, "R", 6.3, 1.45)
for pr, hijo in (("imp", "imp1"), ("rep", "rep1"), ("accx", "acc1")):
    m.columna([hijo], 78.35, "R", m.POS[pr][1], 0)
# Hueco para la columna de descriptores: todo lo que está a la derecha de los instrumentos se desplaza
DX = 6.0
for cid, (x, yy) in list(m.POS.items()):
    if x >= 39.0:
        m.pon(cid, x + DX, yy)
X_DESC = 39.4  # borde izquierdo de la columna de descriptores
m.pila([did(d) for d in ORDEN_DESC], X_DESC, "R", 0, ys=[4.0 + 1.05 * k for k in range(len(ORDEN_DESC))])
X_FRASE_DESC = 43.9
m.XC = (m.POS["ctx"][0] + m.POS["div"][0]) / 2
m.pon("sa", m.XC, 0)
# Criterio 1.1 desglosado, abajo a la derecha
m.pon("k_est", 61.0 + DX, 14.0)
m.pon("k_mod", 57.0 + DX, 16.2); m.pon("k_efi", 61.6 + DX, 16.2); m.pon("k_dig", 65.8 + DX, 16.2)
m.pon("k_cie", 55.0 + DX, 18.4); m.pon("k_vid", 58.9 + DX, 18.4)
m.YL = 26.4
# Autoría: concepto suelto, sin enlaces, arriba a la derecha
AUTORIA = "Autoría: Javier Gómez López"
x_der = max(x + W(C[c][0]) / 2 for c, (x, _) in m.POS.items())
m.libres = [("autoria", AUTORIA, x_der - W(AUTORIA) / 2, -1.6)]

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
    ("ctx", "se concreta en", ["ctx_mat", "ctx_cur", "ctx_cam", "ctx1"], False, LISTA),
    ("reto", "contribuye a los", ["ods"], False, ("t", 0.6)),
    ("reto", "se formula como", ["preg"], False, ("t", 0.6)),
    ("reto", "da lugar al", ["prod"], False, ("t", 0.5)),
    ("preg", "se responde con la", ["tarea"], False, ("t", 0.45)),
    ("tarea", "consiste en", ["t1", "t2", "t3", "t4", "t5", "t6"], False, ("lista", 0.95)),
    ("ods", "se concretan en", ["ods7", "ods11"], False, LISTA),
    ("prod", "se concreta en", ["libro"], False, None),
    ("libro", "incluye", ["p1", "p2", "p3", "p5", "p6", "p7", "p4"], False, LISTA),
    ("eval", "se apoya en", ["evid"], False, ("t", 0.6)),
    ("eval", "combina", ["agentes"], False, ("t", 0.55)),
    ("eval", "se realiza con", ["inst"], False, ("t", 0.6)),
    ("evid", "incluyen", ["hoja", "kanban", "relevo"], False, LISTA),
    ("inst", "incluyen", ["EX", "CU", "FI", "LI", "EP", "MC", "OB", "CO"], False, LISTA),
    ("ce", "incluyen", [f"ce{n}" for n in NOMBRE_CE], False, LISTA),
    ("met", "combina", ["abr", "mag", "coop"], False, ("p", 59.4 + DX, 3.25)),
    ("met", "desarrolla un", ["etw"], False, ("t", 0.35)),
    ("met", "utiliza", ["recu"], False, ("t", 0.62)),
    ("met", "incluye", ["div"], False, ("t", 0.35)),
    ("coop", "se organiza en", ["roles"], False, None),
    ("roles", "rotan entre", ["r_coord", "r_med", "r_mod", "r_com"], False, ("lista", 1.15)),
    ("etw", "compara", ["lat"], False, None),
    ("recu", "incluyen", ["clin", "cinta", "ggb", "pvgis", "noaa", "twin"], False, LISTA),
    ("div", "se concreta en", ["imp", "rep", "accx", "refz", "ampl"], False, LISTA),
    ("imp", "se concreta en la", ["imp1"], False, ("cruce", "right", "left")),
    ("rep", "se concreta en la", ["rep1"], False, ("cruce", "right", "left")),
    ("accx", "se concreta en", ["acc1"], False, ("cruce", "right", "left")),
]
for n in NOMBRE_CE:
    P.append((f"ce{n}", "se evalúa con los criterios", [f"cr{n}"], False, ("cruce", "right", "left")))
    P.append((f"ce{n}", "contribuye a", [did(d) for d in DESC_DE[n]], False,
              ("p", X_FRASE_DESC, m.POS[f"ce{n}"][1], "left", "right")))
P += [
    ("cr1", "el 1.1 pide manejar", ["k_est"], False, ("cruce", "right", "top", 0.35)),
    ("k_est", "se aplican en la", ["k_mod"], False, ("t", 0.6)),
    ("k_est", "evaluando su", ["k_efi"], False, ("t", 0.5)),
    ("k_est", "incluidas las", ["k_dig"], False, ("t", 0.55)),
    ("k_mod", "en contextos de la", ["k_cie", "k_vid"], False, ("p", 57.0 + DX, 17.3)),
]
P += [
    # Enlaces cruzados entre ramas (discontinuos)
    ("vec", "se trabajan en la", ["s34"], True, ("cruce", "right", "left")),
    ("tri", "se trabaja en la", ["s67"], True, ("cruce", "right", "left")),
    ("triang", "se trabaja en la", ["s89"], True, ("cruce", "right", "left")),
    ("rec", "se trabajan en la", ["s1011"], True, ("cruce", "right", "left")),
    ("modz", "se aplica en el", ["s12"], True, ("cruce", "right", "left")),
    ("energ", "se aplica en la", ["s16"], True, ("cruce", "right", "left")),
    ("actit", "se trabajan en", ["s17"], True, ("cruce", "right", "left")),
    ("mod", "se recoge en el", ["libro"], True, ("cruce", "right", "left", 0.7)),
    ("evid", "incluyen también el", ["libro"], True, ("cruce", "bottom", "right", 0.4)),
    ("p4", "se defiende en la", ["s19"], True, ("cruce", "left", "right")),
    ("roles", "se evalúan con los", ["cr9"], True, ("cruce", "left", "right", 0.5)),
    ("k_mod", "la dirige el rol", ["r_mod"], True, ("cruce", "top", "left", 0.6)),
]
m.P = P

m.GLOSAS = [
    ("cada saber se trabaja\nen una actividad", 9.9, 22.8),
    ("el producto es\nla evidencia", 25.9, 9.0),
    ("cada criterio lleva los códigos\nde sus instrumentos", 50.6 + DX, 19.4),
    ("el cooperativo se evalúa\ncon el criterio 9.3", 46.8 + DX, 17.2),
]
m.leyenda_extra = ("Instrumentos: EX examen · CU cuestionarios · F1–F4 fichas de GeoGebra (rúbrica R4) · LI libro y propuesta · "
                   "EP exposición · MC mapa conceptual · OB observación · CO co/autoevaluación. Descriptores operativos del perfil "
                   "de salida: STEM, matemática y en ciencia, tecnología e ingeniería · CD, digital · CE, emprendedora · "
                   "CC, ciudadana · CCL, comunicación lingüística · CPSAA, personal, social y de aprender a aprender.\n"
                   "Temporalización: 20 sesiones de 55 minutos en 5 semanas, 4 por semana; S1–S20 indica la sesión.")
# ---------------- Fases de las actividades (temporalización, §3.4) ----------------
H = 4.2  # el reto y lo que queda a su derecha se desplazan para dejar sitio a la columna de fases
for cid, (x, yy) in list(m.POS.items()):
    if x >= 16.4:
        m.pon(cid, x + H, yy)
m.P = [(o, lab, ds, cz, ("p", aj[1] + H) + tuple(aj[2:]) if aj and aj[0] == "p" and aj[1] >= 16.4 else aj)
       for o, lab, ds, cz, aj in m.P]
m.GLOSAS = [(t, x + H if x >= 16.4 else x, yy) for t, x, yy in m.GLOSAS]
FASES = {"f_ini": ["s1"], "f_des": ACT[1:13], "f_cie": ["s18", "s19"]}
assert sum(len(v) for v in FASES.values()) == len(ACT)
fila = dict(zip(ACT, FILAS))
m.pon("f_ini", 18.9, fila["s1"])
m.pon("f_des", 18.9, (fila["s2"] + fila["s17"]) / 2)
m.pon("f_cie", 18.9, fila["s19"] + 1.0)
m.P += [
    ("act", "comienzan con el", ["f_ini"], False, None),
    ("f_ini", "sigue el", ["f_des"], False, None),
    ("f_des", "termina con el", ["f_cie"], False, None),
]
for f, ses in FASES.items():
    m.P.append((f, "incluye", ses, False, ("p", 16.9, m.POS[f][1], "left", "right")))

# ---------------- Sentidos matemáticos: hueco a la izquierda ----------------
G = 4.3  # todo lo que hay a la derecha del contexto se desplaza para dejar sitio a los sentidos
for cid, (x, yy) in list(m.POS.items()):
    if x >= 4.5 and not cid.startswith("ctx"):
        m.pon(cid, x + G, yy)
m.P = [(o, lab, ds, cz, ("p", aj[1] + G) + tuple(aj[2:]) if aj and aj[0] == "p" and aj[1] >= 4.5 else aj)
       for o, lab, ds, cz, aj in m.P]
m.GLOSAS = [(t, x + G if x >= 4.5 else x, yy) for t, x, yy in m.GLOSAS]
SENT = ["sA", "sB", "sD", "sC", "sF", "sE"]  # orden que reduce los cruces con los saberes
INCLUYE = {"sA": ["vec"], "sB": ["tri", "triang"], "sD": ["tri", "modz"], "sC": ["rec", "modz", "energ"],
           "sF": ["energ", "actit"]}  # según las letras de los bloques en las matrices; el E no se trabaja
m.pon("sent", 4.6, 5.6)
m.columna(SENT, 6.0, "L", 7.6, 1.85)
m.P.append(("sab", "se organizan en los", ["sent"], False, None))
m.P.append(("sent", "comprenden", SENT, False, ("p", 6.6, 6.45, "center", "right")))
for sid, saberes in INCLUYE.items():
    m.P.append((sid, "incluye", saberes, False, ("p", 7.3, m.POS[sid][1], "right", "left")))
# Matrices de relación curricular (SA, §5): enlazan saberes, competencias e instrumentos
m.pon("matr", 48.5, 2.2)
m.P.append(("sa", "se planifica con las", ["matr"], False, None))
m.P.append(("matr", "relacionan", ["ce", "inst"], False, ("p", 50.9, 3.1, "bottom", "center")))
m.P.append(("matr", "relacionan los", ["sab"], False, ("p", 45.0, 2.95, "left", "bottom")))
# Herramientas digitales del criterio 1.1: todos los recursos digitales de la SA
DIGITALES = ["ggb", "pvgis", "noaa", "twin"]
x_borde = min(m.ancla(d, "left")[0] for d in DIGITALES)
y_med = sum(m.POS[d][1] for d in DIGITALES) / len(DIGITALES)
m.P.append(("k_dig", "como", DIGITALES, True, ("p", x_borde - 1.3, y_med, "top", "left")))
m.XC = (m.POS["ctx"][0] + m.POS["div"][0]) / 2
m.pon("sa", m.XC, 0)
x_der = max(x + W(C[c][0]) / 2 for c, (x, _) in m.POS.items())
m.libres = [("autoria", AUTORIA, x_der - W(AUTORIA) / 2, -1.6)]
m.leyenda_extra += " Sentidos matemáticos: entre paréntesis, el bloque de contenidos del Decreto 64/2022."
m.escribir(HERE, "Gomez_MapaSA_completo.cxl", "Gomez_MapaSA_completo.tex")
