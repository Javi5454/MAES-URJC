"""Genera matrices_tabla.tex: amplía la matriz de la Actividad 1 con descriptores, sesiones y evidencias.

Lee INSTR, CRIT, BLOOM y GRUPOS de ../Actividad 1/matriz.py sin ejecutarlo (ese script regenera sus
propios archivos al importarlo) y añade aquí solo lo nuevo de la situación de aprendizaje.
"""
import ast
from pathlib import Path

HERE = Path(__file__).parent
NOMBRES = {"INSTR", "CORTO", "CRIT", "BLOOM", "GRUPOS", "EX", "CU", "FI", "LI", "EP", "MC", "OB", "CO"}
arbol = ast.parse((HERE.parent / "Actividad 1" / "matriz.py").read_text(encoding="utf-8"))
datos = {}
for nodo in arbol.body:
    if isinstance(nodo, ast.Assign):
        destinos = {t.id for d in nodo.targets for t in ([d] if isinstance(d, ast.Name) else getattr(d, "elts", []))}
        if destinos & NOMBRES:
            exec(compile(ast.Module([nodo], []), "matriz.py", "exec"), {"range": range}, datos)
CRIT, GRUPOS, EX, CU, FI, LI, EP, MC, OB, CO = (datos[k] for k in "CRIT GRUPOS EX CU FI LI EP MC OB CO".split())
CODIGOS = ["EX", "CU", "FI", "LI", "EP", "MC", "OB", "CO"]

# Ampliación respecto a la Actividad 1: competencia específica 6 (Decreto 64/2022, BOCM p. 324)
CRIT = dict(CRIT)
CRIT["6.1"] = ("Resolver problemas en situaciones diversas, utilizando procesos matemáticos, estableciendo y aplicando "
               "conexiones entre el mundo real, otras áreas de conocimiento y las matemáticas.")
CRIT["6.2"] = ("Analizar la aportación de las matemáticas al progreso de la humanidad reflexionando sobre su contribución "
               "en la propuesta de soluciones a situaciones complejas y a los retos científicos y tecnológicos que se "
               "plantean en la sociedad.")
GRUPOS = list(GRUPOS) + [("C y F. Conexión con la energía solar", [
    "Modelos matemáticos (geométricos, algebraicos, grafos...) en la resolución de problemas en el plano. Conexiones con otras disciplinas y áreas de interés.",
    "Valoración de la contribución de las matemáticas y el papel de matemáticos a lo largo de la historia en el avance de la ciencia y la tecnología.",
], [
    ("6.1", "Aplicar", "El alumno ha resuelto la ubicación de los nuevos paneles conectando las medidas reales, el modelo geométrico y el criterio técnico de separación entre filas.", [LI, EP]),
    ("6.2", "Analizar", "El alumno ha analizado cómo contribuye su propuesta a los retos de energía sostenible (ODS 7 y 11), señalando el papel del modelo matemático y sus límites.", [LI, EP]),
])]

# El examen escrito no recoge la representación con tecnología: 7.1 se evidencia con F1 y Q1.
bloque_7_1, cont_7_1, fs_7_1 = GRUPOS[0]
assert fs_7_1[0][0] == "7.1"
GRUPOS[0] = (bloque_7_1, cont_7_1, [(*fs_7_1[0][:3], [k for k in fs_7_1[0][3] if k != EX]), *fs_7_1[1:]])

# Competencias específicas: enunciado literal, descriptores que fija el decreto (BOCM pp. 321-324),
# descriptores priorizados y motivo por el que no se priorizan los demás.
CE = {
    "1": ("Modelizar y resolver problemas de la vida cotidiana y de la ciencia y la tecnología aplicando diferentes estrategias y formas de razonamiento para obtener posibles soluciones.",
          "STEM1, STEM2, STEM3, CD2, CD5, CPSAA4, CPSAA5, CE3", {"STEM3", "CD5", "CE3"},
          "STEM1, STEM2 y CD2 se concretan en CE2, CE3 y CE7. CPSAA4 y CPSAA5 no tienen aquí una actividad específica."),
    "2": ("Verificar la validez de las posibles soluciones de un problema empleando el razonamiento y la argumentación para contrastar su idoneidad.",
          "STEM1, STEM2, CD3, CPSAA4, CC3, CE3", {"STEM1", "STEM2"},
          "CPSAA4 se refiere a analizar información de medios de comunicación, y cotejar un cálculo no lo es. CD3, CC3 y CE3 no intervienen en la verificación."),
    "3": ("Formular o investigar conjeturas o problemas, utilizando el razonamiento, la argumentación, la creatividad y el uso de herramientas tecnológicas, para generar nuevo conocimiento matemático.",
          "CCL1, STEM1, STEM2, CD1, CD2, CD3, CD5, CE3", {"STEM1", "STEM2"},
          "CD5 no se moviliza: al conjeturar, GeoGebra es un instrumento de investigación y no se crea ninguna herramienta. CD1, CD2, CD3, CE3 y CCL1 no definen lo que se aprende en esta tarea."),
    "5": ("Establecer, investigar y utilizar conexiones entre las diferentes ideas matemáticas estableciendo vínculos entre conceptos, procedimientos, argumentos y modelos para dar significado y estructurar el aprendizaje matemático.",
          "STEM1, STEM3, CD2, CD3, CCEC1", {"STEM1"},
          "Compartir una construcción (CD3) o crear contenido digital (CD2) no conecta ideas matemáticas. STEM3 se concreta en CE1 y CCEC1 no tiene actividad."),
    "6": ("Descubrir los vínculos de las matemáticas con otras áreas de conocimiento y profundizar en sus conexiones, interrelacionando conceptos y procedimientos, para modelizar, resolver problemas y desarrollar la capacidad crítica, creativa e innovadora en situaciones diversas.",
          "STEM1, STEM2, CD2, CPSAA5, CC4, CE2, CE3, CCEC1", {"CC4", "STEM2"},
          "CE2 exigiría un análisis económico que la propuesta no incluye. CCEC1 se refiere al patrimonio cultural, y Eratóstenes solo se usa como motivación. STEM1, CD2 y CE3 se concretan en otras competencias; CPSAA5 no tiene actividad."),
    "7": ("Representar conceptos, procedimientos e información matemáticos seleccionando diferentes tecnologías, para visualizar ideas y estructurar razonamientos matemáticos.",
          "STEM3, CD1, CD2, CD5, CE3, CCEC4.1, CCEC4.2", {"CD2"},
          "CCEC4.1 y CCEC4.2 se refieren a proyectos artísticos, no al diseño de una construcción. CD5, STEM3 y CE3 se concretan una sola vez, en CE1. CD1 no tiene actividad específica."),
    "8": ("Comunicar las ideas matemáticas, empleando el soporte, la terminología y el rigor apropiados, para organizar y consolidar el pensamiento matemático.",
          "CCL1, CCL3, CP1, STEM2, STEM4, CD3, CCEC3.2", {"CCL1", "STEM4", "CD3"},
          "CCL3 y CCEC3.2 no tienen actividad específica. CP1 no se evalúa, porque la lengua de trabajo con el socio no es objeto de esta materia. STEM2 se concreta en CE2 y CE3."),
    "9": ("Utilizar destrezas personales y sociales, y organizando activamente el trabajo en equipos heterogéneos, aprendiendo del error como parte del proceso de aprendizaje y afrontando situaciones de incertidumbre, para perseverar en la consecución de objetivos en el aprendizaje de las matemáticas.",
          "CP3, STEM5, CPSAA1.1, CPSAA1.2, CPSAA3.1, CPSAA3.2, CC2, CC3, CE2", {"CPSAA3.2", "CPSAA1.1"},
          "Los demás descriptores no tienen una actividad y una evidencia propias en esta secuencia."),
}

# Descriptores priorizados: (CE, descriptor, fragmento literal del RD 243/2022, anexo I, columna de Bachillerato,
# actuación concreta, por qué la conexión es real, evidencia)
DESCRIPTORES = [
    ("1", "STEM3", "diseñando y creando prototipos o modelos para generar o utilizar productos que den solución a una necesidad o problema de forma colaborativa",
     "Cada equipo diseña el modelo de sombras y, con él, la propuesta de ampliación.",
     "El reto es un proyecto: hay una necesidad real del centro y un producto que se evalúa según sus objetivos y su sostenibilidad.",
     "Libro y propuesta (R1), S14--S16"),
    ("1", "CD5", "Desarrolla soluciones tecnológicas innovadoras y sostenibles para dar respuesta a necesidades concretas",
     "El modelo de GeoGebra se entrega como herramienta que la dirección puede reutilizar cambiando la fecha y la altura del obstáculo.",
     "Aquí sí se crea una herramienta digital que responde a una necesidad concreta. Por eso CD5 se trabaja en esta competencia y en ninguna otra.",
     "Libro, parte 2 (R1), S15"),
    ("1", "CE3", "estrategias ágiles de planificación y gestión de proyectos",
     "Cada equipo planifica el producto con un tablero Kanban y lo revisa en cada sesión de trabajo.",
     "Kanban es una estrategia ágil, y S14--S17 obligan a gestionar tareas y tiempo para llegar a un resultado útil para otros.",
     "Tablero Kanban (L1), S2--S17"),
    ("2", "STEM1", "analizando críticamente las soluciones y reformulando el procedimiento",
     "El alumnado compara el cálculo a mano con GeoGebra, explica la discrepancia y rehace el procedimiento si hace falta.",
     "El descriptor describe lo mismo que pide la competencia: analizar una solución y corregir el camino seguido.",
     "F1, F3 y examen, pregunta 2"),
    ("2", "STEM2", "apreciando la importancia de la precisión y la veracidad",
     "Cada medida se repite y se calcula cómo cambia la altura con un grado de error.",
     "A diferencia de un problema de libro, la medida real tiene error, y de él depende la validez de la solución.",
     "Libro, parte 3 (R1), S14--S15"),
    ("3", "STEM1", "métodos inductivos y deductivos propios del razonamiento matemático",
     "En F2 se observan casos y se formula una conjetura (S5); después se demuestra (S6).",
     "La secuencia reproduce los dos métodos que nombra el descriptor: primero inducción y luego deducción.",
     "F2 y examen, pregunta 3"),
    ("3", "STEM2", "planteándose hipótesis y contrastándolas o comprobándolas mediante la observación",
     "En F2 se pone a prueba en GeoGebra la conjetura $\\sin 2\\alpha = 2\\sin\\alpha$ y se busca un contraejemplo.",
     "La conjetura funciona como hipótesis y GeoGebra como instrumento de observación, no como producto.",
     "F2 y observación (L1), S5"),
    ("5", "STEM1", "emplea estrategias variadas para la resolución de problemas",
     "Ángulos, perpendicularidad y distancias se abordan con producto escalar, ecuaciones de la recta y trigonometría.",
     "Conectar ideas se demuestra al poder resolver un problema por más de una vía y elegir entre ellas.",
     "Mapa conceptual (L2) y examen, pregunta 5"),
    ("6", "CC4", "actividades y hábitos que conduzcan al logro de los Objetivos de Desarrollo Sostenible",
     "Cada equipo argumenta cómo contribuye su propuesta a los ODS 7 y 11.",
     "La decisión afecta a la energía de su propio centro: una actuación local conectada con un objetivo global.",
     "Libro, parte 5 (R1), y defensa (R2)"),
    ("6", "STEM2", "mostrando una actitud crítica acerca del alcance y limitaciones de los métodos empleados",
     "Se compara la separación del mediodía con la del pliego del IDAE y se señalan los límites del modelo.",
     "El modelo matemático por sí solo no basta: el criterio técnico muestra hasta dónde llega y dónde se queda corto.",
     "Libro, partes 4 y 5 (R1)"),
    ("7", "CD2", "Crea, integra y reelabora contenidos digitales de forma individual o colectiva",
     "El equipo integra en el libro construcciones, cálculos y explicación, y cita los datos y materiales ajenos.",
     "El libro es un contenido digital colectivo que reelabora datos de terceros, por lo que también obliga a respetar su autoría.",
     "Libro, partes 2 y 7 (R1)"),
    ("8", "CCL1", "adecuación a los diferentes contextos sociales y académicos",
     "La propuesta se defiende ante la clase y la dirección.",
     "Explicar el mismo método a compañeros y a quien decide obliga a adaptar el discurso sin perder rigor.",
     "Exposición (R2), S19--S20"),
    ("8", "STEM4", "de forma clara y precisa, en diferentes formatos",
     "El método y los resultados se presentan con fórmulas, tablas, gráficos y construcciones.",
     "Cada formato aporta algo distinto: el plano convence a la dirección y la fórmula justifica el cálculo.",
     "Exposición (R2) y libro (R1)"),
    ("8", "CD3", "para comunicarse, trabajar colaborativamente y compartir información, gestionando de manera responsable sus acciones, presencia y visibilidad en la red",
     "Datos y conclusiones se comparten en el TwinSpace con avatares y sin datos personales.",
     "Es un intercambio real con otro centro, en el que la identidad digital se gestiona con reglas explícitas.",
     "Publicaciones del TwinSpace (seguimiento, sin calificación)"),
    ("9", "CPSAA3.2", "Distribuye en un grupo las tareas, recursos y responsabilidades de manera ecuánime",
     "Los cuatro roles rotan, de modo que todos los ejercen todos (sección~\\ref{sec:cooperativo}).",
     "La rotación convierte el reparto ecuánime en una regla de funcionamiento, no en una intención.",
     "Kanban y hojas de relevo (L1), R3"),
    ("9", "CPSAA1.1", "la resiliencia, la autoeficacia y la búsqueda de objetivos de forma autónoma",
     "Las conjeturas falsas y las medidas fallidas se revisan y se repiten.",
     "El reto incluye fallos reales (nubes, medidas incoherentes), que dan ocasión de perseverar.",
     "Observación (L1) y autoevaluación (R3)"),
]

# Por cada grupo y fila: (sesiones de trabajo, evidencia). Las sesiones de examen y defensa se añaden por regla.
SESIONES = [
    [([2, 3, 4], "Ficha F1 y cuestionario Q1 con operaciones interpretadas."),
     ([2, 4], "Ficha F1 con cálculo manual, comprobación y causa de la discrepancia."),
     ([4], "Problemas de perpendicularidad y ángulos resueltos.")],
    [([5], "Ficha F2 con la tabla de signos y observaciones por cuadrante."),
     ([5, 6], "Conjetura escrita en F2 y demostración en papel."),
     ([7], "Cuestionario Q2: soluciones en el intervalo y solución general.")],
    [([8, 9], "Ficha F3: elección razonada del teorema."),
     ([9], "Ficha F3: número de soluciones y procedimiento."),
     ([9], "Cuestionario Q3 y comprobación arrastrando vértices.")],
    [([10, 13], "Mapa conceptual con enlaces entre vector director, normal y ángulo."),
     ([11], "Cuestionario Q4 con posición, ángulo y distancia."),
     ([10, 12], "Ficha F4: ecuación elegida y motivo.")],
    [([14, 15], "Libro: método, construcción y comparación con otro método."),
     ([14, 15], "Libro: medidas repetidas, sensibilidad y resultado elegido."),
     ([15, 16, 17], "Libro completo con representaciones justificadas."),
     ([17], "Ensayo y defensa oral con terminología y notación correctas.")],
    [([5, 12, 14], "Registro de observación y revisión de medidas fallidas."),
     ([16, 17], "Registro de cambios del libro tras la coevaluación."),
     ([2, 14, 15, 16], "Tablero Kanban, roles rotados y registro de observación.")],
    [([14, 16], "Propuesta de ampliación con plano, cálculo de filas y decisión justificada."),
     ([16], "Apartado del libro sobre ODS, límites del modelo y defensa.")],
]


# Por cada grupo y fila: (aspecto, por qué en esas sesiones, por qué ese instrumento)
JUSTIF = [
    [("Representar y operar con vectores",
      "Se construye primero en F1 (S2), para que cada operación tenga un significado geométrico antes de formalizarla en S3 y S4.",
      "La ficha recoge la representación con tecnología y Q1 comprueba su interpretación. El examen escrito no permite usar GeoGebra."),
     ("Validar cálculos vectoriales",
      "Validar exige tener un cálculo propio: en S2 se contrasta de forma exploratoria y en S4, con la fórmula de la proyección, se explica la discrepancia. S18 comprueba si se hace sin herramienta.",
      "F1 registra el contraste entre mano y GeoGebra; la pregunta 2 del examen obliga a detectar un error ajeno."),
     ("Producto escalar en problemas",
      "El producto escalar une coordenadas y geometría, y se enseña en S4; S18 comprueba que se aplica de forma autónoma.",
      "Q1 da un diagnóstico temprano para el refuerzo por criterio de S13, y el examen verifica la transferencia.")],
    [("Investigar con la circunferencia",
      "S5 precede a propósito a la exposición de S6: hay que investigar antes de conocer la fórmula.",
      "La ficha muestra lo investigado; la observación capta si se explora antes de pedir ayuda, que no queda en el papel."),
     ("Conjeturar y demostrar",
      "La conjetura nace en S5 y se demuestra en S6, de modo que la demostración responde a una pregunta propia. S18 comprueba que se demuestra sin apoyo.",
      "F2 recoge la conjetura y la pregunta 3a del examen, la demostración individual."),
     ("Ecuaciones trigonométricas",
      "Las ecuaciones usan el ángulo doble, que se estudia en la misma sesión, y la pieza del reto les da un uso inmediato.",
      "Obtener todas las soluciones es un procedimiento: Q2 da retorno inmediato y el examen lo certifica.")],
    [("Elegir el teorema adecuado",
      "La elección se aprende en S8 con datos variados y se pone a prueba en S9, con el caso que genera más dudas.",
      "F3 y la pregunta 4 piden justificar la elección, no solo dar el resultado."),
     ("Caso ambiguo",
      "Va al final del bloque porque exige dominar antes el teorema del seno.",
      "En F3 se ve cuántas soluciones hay al arrastrar; la pregunta 4b exige obtenerlas por cálculo."),
     ("Validar triángulos",
      "S9 concentra el caso en que validar es decisivo: si $\\sin B>1$, el triángulo no existe.",
      "La comprobación arrastrando vértices solo se ve en F3; Q3 la cierra con un caso sin solución.")],
    [("Conectar vector y recta",
      "S10 deduce las ecuaciones del vector director; el mapa llega en S13, cuando ya se han visto los tres bloques y hay algo que conectar.",
      "El mapa hace visibles las conexiones y la pregunta 5 del examen comprueba que se usan."),
     ("Ángulos y distancias",
      "Reutilizan el producto escalar de S4; por eso se sitúan al final del bloque, para volver sobre él.",
      "Q4 alimenta el refuerzo por criterio de S13 y el examen verifica el dominio individual."),
     ("Elegir la ecuación de la recta",
      "S10 presenta las cinco formas y F4, en S12, obliga a elegir una para un problema real.",
      "F4 y la pregunta 5d piden explicar por qué se elige esa ecuación.")],
    [("Método y modelo",
      "Se aplica cuando ya se dispone de todas las herramientas: el método se aprueba en S13, se ejecuta en S14 y se modela en S15.",
      "El libro documenta el proceso; la defensa comprueba que todo el equipo lo entiende."),
     ("Elegir el resultado",
      "Elegir solo tiene sentido con medidas reales y repetidas (S14), y la sensibilidad al error se analiza con ellas en S15.",
      "El libro recoge datos y decisión; en la defensa hay que justificarla ante preguntas."),
     ("Integrar representaciones",
      "Integrar exige tener ya datos y modelo (S15 y S16), y S17 permite mejorarlo; las defensas muestran si otras personas lo entienden.",
      "El libro es la representación. La coevaluación aporta lo que pide el criterio: su utilidad para compartir información."),
     ("Comunicar con rigor",
      "Se ensaya en S17 y se evalúa en S19 y S20, ante un público real.",
      "La comunicación oral solo se puede evaluar en una exposición; la co/autoevaluación añade la mirada del público.")],
    [("Aprender del error",
      "Se observa donde el error aparece de forma natural: conjeturas falsas (S5), construcciones (S12) y medidas (S14).",
      "Una actitud no cabe en un examen: se observa cuando ocurre y se reflexiona en la autoevaluación."),
     ("Aceptar la crítica",
      "Necesita una crítica aprovechable: la coevaluación del borrador en S16 se aprovecha en S17, dentro del horario de clase.",
      "El registro de cambios permite ver qué se ha incorporado realmente."),
     ("Colaborar en equipo",
      "Los roles se presentan en S2 y se exigen sobre todo de S14 a S16, cuando el producto depende de todos.",
      "Solo la observación y los compañeros pueden valorar la colaboración efectiva.")],
    [("Conectar con la instalación",
      "La conexión con el criterio técnico requiere haber medido; se hace en S16, con la orientación del departamento de Tecnología.",
      "La propuesta recoge el cálculo y la defensa, su viabilidad ante quien decide."),
     ("Valorar impacto y límites",
      "La reflexión tiene sentido cuando el modelo ya existe y se conocen sus resultados.",
      "El apartado del libro la deja por escrito y la defensa la somete a preguntas.")],
]


def filas():
    for g, (bloque, cont, fs) in enumerate(GRUPOS):
        yield bloque, cont, [(*f, *SESIONES[g][i]) for i, f in enumerate(fs)]


def sesiones_de(ses, ins):
    s = set(ses)
    if EX in ins:
        s.add(18)
    if EP in ins or CO in ins:
        s.update({19, 20})
    return sorted(s)


def tabla_ce():
    L = [r"\begin{tablaSAlarga}{colspec={Q[l,wd=8.2cm] Q[l,wd=1.5cm] Q[l,wd=3.7cm] Q[l,wd=9.6cm]},",
         r"  rowsep=2pt, colsep=4pt, cells={font=\scriptsize}, row{1}={bg=urjc, fg=white, font=\footnotesize\bfseries},}",
         r"Competencia específica & Criterios & Descriptores del decreto (en negrita, los priorizados) & Descriptores no priorizados y motivo \\"]
    usados = sorted({c for *_, fs in filas() for c, *_ in fs}, key=lambda c: tuple(map(int, c.split("."))))
    for n, (texto, desc, prior, fuera) in CE.items():
        cr = ", ".join(c for c in usados if c.startswith(n + "."))
        lista = ", ".join(rf"\textbf{{{d}}}" if d in prior else d for d in desc.split(", "))
        L.append(rf"\textbf{{CE{n}.}} {texto} & {cr} & {lista} & {fuera} \\")
    L.append(r"\end{tablaSAlarga}")
    return L


def tabla_descriptores():
    L = [r"\begin{tablaSAlarga}{colspec={Q[l,wd=1cm] Q[l,wd=5.6cm] Q[l,wd=5.8cm] Q[l,wd=6.6cm] Q[l,wd=4cm]},",
         r"  rowsep=2pt, colsep=4pt, cells={font=\scriptsize}, row{1}={bg=urjc, fg=white, font=\footnotesize\bfseries},}",
         r"CE & Descriptor (fragmento literal) & Actuación concreta & Por qué la conexión es real & Evidencia \\"]
    for n, d, literal, accion, razon, evid in DESCRIPTORES:
        L.append(rf"\textbf{{CE{n}}} & \textbf{{{d}.}} «{literal}» & {accion} & {razon} & {evid} \\")
    L.append(r"\end{tablaSAlarga}")
    return L


def tabla_justificacion():
    L = [r"\begin{tablaSAlarga}{colspec={Q[l,wd=1cm] Q[l,wd=3.4cm] Q[c,wd=1.4cm] Q[l,wd=8.9cm] Q[c,wd=1.3cm] Q[l,wd=7cm]},",
         r"  rowsep=2pt, colsep=4pt, cells={font=\scriptsize}, row{1}={bg=urjc, fg=white, font=\footnotesize\bfseries},}",
         r"Crit. & Aspecto & Sesiones & Por qué en esas sesiones & Instrum. & Por qué ese instrumento \\"]
    for g, (_, _, fs) in enumerate(filas()):
        for i, (c, _, _, ins, ses, _) in enumerate(fs):
            aspecto, razon_s, razon_i = JUSTIF[g][i]
            s = ", ".join(map(str, sesiones_de(ses, ins)))
            codigos = ", ".join(CODIGOS[k] for k in sorted(ins))
            L.append(rf"\textbf{{{c}}} & {aspecto} & {s} & {razon_s} & {codigos} & {razon_i} \\")
    L.append(r"\end{tablaSAlarga}")
    return L


def tabla_relacion():
    L = [r"\begin{tablaSAlarga}{colspec={Q[l,wd=5.2cm] Q[l,wd=7.2cm] Q[c,wd=1.3cm] Q[c,wd=1.3cm] Q[c,wd=1.5cm] Q[l,wd=6.5cm]},",
         r"  rowsep=2pt, colsep=4pt, cells={font=\scriptsize}, row{1}={bg=urjc, fg=white, font=\footnotesize\bfseries},}",
         r"Criterio de evaluación & Criterio operativizado & Bloom & Sesiones & Instrum. & Evidencia de aprendizaje \\"]
    for bloque, cont, fs in filas():
        celda = r"{\textbf{" + bloque + r"}\\ " + r"\\ ".join(r"\textbullet~" + c for c in cont) + "}"
        L.append(r"\SetCell[c=6]{l,bg=rosa} " + celda + r" & & & & & \\*")
        for c, nivel, op, ins, ses, evid in fs:
            s = ", ".join(map(str, sesiones_de(ses, ins)))
            i = ", ".join(CODIGOS[k] for k in sorted(ins))
            L.append(rf"\textbf{{{c}.}} {CRIT[c]} & {op} & \textit{{{nivel}}} & {s} & {i} & {evid} \\")
    L.append(r"\end{tablaSAlarga}")
    return L


def tabla_cobertura():
    marca = {}
    for _, _, fs in filas():
        for c, _, _, ins, ses, _ in fs:
            d = marca.setdefault(c, (set(), set()))
            d[0].update(sesiones_de(ses, ins))
            d[1].update(ins)
    orden = sorted(marca, key=lambda c: tuple(map(int, c.split("."))))
    L = [r"\begin{tablaSAlarga}{colspec={Q[c,wd=1.3cm] *{20}{Q[c,wd=0.58cm]} *{8}{Q[c,wd=0.75cm]}},",
         r"  rowsep=1.5pt, colsep=2pt, cells={font=\scriptsize}, row{1}={bg=urjc, fg=white, font=\scriptsize\bfseries},",
         r"  column{22-29}={bg=rosa}, cell{1}{22-29}={bg=urjc},}",
         "Criterio & " + " & ".join(f"S{i}" for i in range(1, 21)) + " & " + " & ".join(CODIGOS) + r" \\"]
    for c in orden:
        ses, ins = marca[c]
        ms = " & ".join(r"\textbf{X}" if i in ses else "" for i in range(1, 21))
        mi = " & ".join(r"\textbf{X}" if k in ins else "" for k in range(8))
        L.append(rf"\textbf{{{c}}} & {ms} & {mi} \\")
    L.append(r"\end{tablaSAlarga}")
    return L


# Comprobaciones antes de generar
assert len(SESIONES) == len(GRUPOS) and all(len(s) == len(g[2]) for s, g in zip(SESIONES, GRUPOS))
for _, _, fs in filas():
    for c, _, op, ins, ses, evid in fs:
        assert c in CRIT and c.split(".")[0] in CE and ins and ses and evid, c
        assert op.startswith("El alumno ha"), op
        s = sesiones_de(ses, ins)
        assert FI not in ins or set(s) & {2, 5, 9, 12}, f"{c}: ficha fuera de sus sesiones"
        assert CU not in ins or set(s) & {4, 7, 9, 11}, f"{c}: cuestionario fuera de sesión"
        assert LI not in ins or set(s) & {14, 15, 16}, f"{c}: libro fuera de las sesiones 14-16"
        assert MC not in ins or 13 in s, f"{c}: mapa fuera de la sesión 13"
assert len(JUSTIF) == len(GRUPOS) and all(len(j) == len(g[2]) for j, g in zip(JUSTIF, GRUPOS)), "justificación incompleta"
for n, d, *_ in DESCRIPTORES:
    assert d in CE[n][1].split(", ") and d in CE[n][2], f"CE{n}: {d} no priorizado o fuera del decreto"
assert all(p in {d for m, d, *_ in DESCRIPTORES if m == n} for n, c in CE.items() for p in c[2]), "priorizado sin justificar"
assert all(k in {c.split(".")[0] for *_, fs in filas() for c, *_ in fs} for k in CE), "CE sin criterio"
assert {k for *_, fs in filas() for f in fs for k in f[3]} == set(range(8)), "instrumento sin usar"

salida = (
    [r"\subsection{Competencias específicas, criterios y descriptores}", r"\vspace{4pt}", ""] + tabla_ce() +
    ["", r"\subsection{Descriptores priorizados: actuación y justificación}", r"\vspace{4pt}", ""] + tabla_descriptores() +
    ["", r"\subsection{Criterios operativizados, saberes, sesiones, instrumentos y evidencias}", r"\vspace{4pt}", ""] + tabla_relacion() +
    ["", r"\subsection{Justificación pedagógica de las relaciones}", r"\vspace{4pt}", ""] + tabla_justificacion() +
    ["", r"\clearpage", r"\subsection{Cobertura: cada criterio por sesiones e instrumentos}", r"\vspace{4pt}", ""] + tabla_cobertura()
)
(HERE / "matrices_tabla.tex").write_text("\n".join(salida) + "\n", encoding="utf-8")
print("matrices_tabla.tex generado:", sum(len(f[2]) for f in GRUPOS), "filas operativizadas")
