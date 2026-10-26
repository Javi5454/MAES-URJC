# Actividad 1 — Matriz de competencias

Matriz de competencias de la situación de aprendizaje «Medir lo que no se puede alcanzar» (Matemáticas I, 1.º de Bachillerato).

## Archivos

| Archivo | Qué es | ¿Se edita a mano? |
|---|---|---|
| `matriz.py` | Datos de la matriz y generador | **Sí**: aquí se cambia la matriz |
| `matriz_tabla.tex` | Tabla LaTeX generada | No, se sobrescribe |
| `Matriz_competencias_DCM.xlsx` | Excel generado | No, se sobrescribe |
| `Actividad_1_JGL_DCM.tex` | Documento (portada, introducción, leyenda); incluye `matriz_tabla.tex` | Sí |
| `Actividad_1_JGL_DCM.pdf` | PDF compilado | No |

## Requisitos

- Python 3 con `openpyxl`:
  ```sh
  python3 -m venv .venv && .venv/bin/pip install openpyxl
  ```
- TeX Live con `tabularray` y `pdflscape` (vienen en `texlive-latex-extra`).

## Regenerar todo

Desde esta carpeta:

```sh
.venv/bin/python matriz.py        # genera matriz_tabla.tex y el .xlsx
pdflatex Actividad_1_JGL_DCM.tex  # dos veces: tabularray necesita una segunda pasada para maquetar la tabla
pdflatex Actividad_1_JGL_DCM.tex
```

El script comprueba antes de generar que todos los criterios usados existen y que no queda ningún instrumento sin usar; si algo falla, se para con un `AssertionError`.

## Cómo modificar la matriz (en `matriz.py`)

- **Instrumentos**: `INSTR` (nombre largo, para el Excel) y `CORTO` (nombre de la cabecera girada en el PDF), en el mismo orden. Las constantes `EX, CU, FI, LI, EP, MC, OB, CO` son sus posiciones; si añades un instrumento, añade también su constante.
- **Criterios de evaluación**: diccionario `CRIT`, con el texto literal del Decreto 64/2022. Para usar uno nuevo (p. ej. `"8.2"`), añádelo aquí primero.
- **Grupos de contenidos**: lista `GRUPOS`. Cada grupo es:
  ```python
  ("Bloque del decreto", [
      "Contenido literal 1.",
      "Contenido literal 2.",
  ], [
      ("1.1", "Criterio operativizado...", [EX, FI]),  # X en Examen y Fichas
  ]),
  ```
  Cada tupla interior es una fila: código del criterio, texto operativizado e instrumentos marcados con X.

## Notas de maquetación

- Un grupo nunca se parte entre dos páginas. Si un grupo crece demasiado y no cabe en una página, divídelo en dos.
- Los anchos de columna están en `colspec`, dentro de la función `tex()`. La página de la matriz va en horizontal con márgenes de 1,5 cm (`\newgeometry` en el `.tex`).
