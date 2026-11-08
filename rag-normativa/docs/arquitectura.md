# Arquitectura

Documento técnico de referencia. Todos los términos están explicados en [Conceptos](conceptos.md), y la construcción paso a paso en la [guía](guia-paso-a-paso.md).

## Flujo de datos

```
INDEXADO
PDF → extract.py → chunking.py → embeddings.py (bge-m3) → data/
      páginas      fragmentos    vectores                 chunks.jsonl, embeddings.npy, meta.json

CONSULTA
pregunta → retrieve.py ─┬─ similitud de embeddings ─┐
                        └─ BM25 léxico ─────────────┴─ RRF → fragmentos
fragmentos ─┬─ mcp_server.py → Claude redacta y cita
            └─ answer.py → modelo de Ollama → validación de citas
```

El servidor MCP solo recupera: redacta el modelo que lo llama, ya sea Claude u otro de Ollama a través de OpenCode. Por eso la validación de citas solo actúa en la CLI, que recupera, llama a Ollama y comprueba el resultado.

## Módulos

| Módulo | Responsabilidad |
|---|---|
| `config.py` | Catálogo de normas, rutas, modelos y tamaños |
| `extract.py` | Texto por página, sin cabeceras ni pies |
| `chunking.py` | Fragmentos con metadatos y formato de cita |
| `embeddings.py` | Llamada a `/api/embed` de Ollama y normalización |
| `index.py` | Escritura y carga del índice |
| `retrieve.py` | Filtros, búsqueda semántica, BM25 y RRF |
| `answer.py` | Prompt, llamada a `/api/chat` y validación |
| `evaluate.py` | Métrica hit@k y prueba de rechazos |
| `cli.py`, `mcp_server.py` | Interfaces |

## Esquema de un fragmento

| Campo | Ejemplo | Significado |
|---|---|---|
| `id` | `decreto-65-eso-00042` | Identificador |
| `norma` | `decreto-65-eso` | Identificador de la norma |
| `page_start`, `page_end` | `15` | Página física del PDF, desde 1 |
| `printed_start` | `550` | Página impresa del boletín, si existe |
| `section` | `Artículo 22` | Artículo, disposición, apartado o anexo |
| `materia` | `MATEMÁTICAS` | Solo en los currículos |
| `curso` | `2º ESO` | Solo cuando el texto lo indica |
| `bloque` | `Criterios de evaluación` | Bloque curricular |
| `text` | | Texto limpio |

Las citas usan siempre la **página física del PDF**, para poder abrirla directamente.

## Decisiones

| Decisión | Motivo |
|---|---|
| Troceado por estructura | Un artículo o bloque curricular es la unidad con la que se cita. Se parte a 1.500 caracteres con 200 de solape |
| Sin OCR | Las 793 páginas tienen capa de texto |
| Metadatos dentro del texto a vectorizar | Muchos currículos usan frases casi iguales; la cabecera distingue materia y curso |
| Búsqueda híbrida | Los embeddings captan el sentido; BM25 acierta en términos exactos como «artículo 28» |
| RRF | Combina rankings sin calibrar puntuaciones de escalas distintas |
| Curso detectado como lista extra de RRF | Favorece el curso mencionado. Un filtro estricto excluiría artículos generales en preguntas como «promocionar de primero a segundo de Bachillerato» |
| NumPy en lugar de base vectorial | Son 2.326 fragmentos: la búsqueda exacta es inmediata y no añade infraestructura |
| `bge-m3` | Modelo local multilingüe, sin enviar datos a terceros |
| Citas `[F1]` internas | Un identificador corto es más fiable que copiar referencias largas. El código lo sustituye por la cita completa |
| `mcp<2` | La versión 2 cambió la API de `FastMCP` |
| Python 3.12 | El sistema tiene 3.15, posterior al rango admitido por el proyecto |

## Detección de estructura

- **Artículos y disposiciones**: por expresiones regulares, solo antes del primer anexo.
- **LOMLOE**: es un artículo único con apartados («Veinte. El artículo 28 queda…»), que se tratan como secciones.
- **Materias**: línea en mayúsculas dentro de los anexos cuyo texto siguiente, antes del próximo título en mayúsculas, contiene «Competencias específicas».
- **Cursos y bloques**: líneas como `2º ESO.` o `Criterios de evaluación.`.

## Validación de respuestas

`validate_answer` comprueba que cada `[Fn]` corresponde a un fragmento recibido y marca los párrafos sin cita. **No demuestra que el fragmento respalde la afirmación**: eso sigue requiriendo leer la fuente.

## Resultados medidos

Corpus del 8 de noviembre de 2026, `bge-m3` y `qwen3.5:35b-a3b`:

- 2.326 fragmentos; indexado en alrededor de 1 minuto en un Apple M5 Pro.
- hit@5 sin filtros: 28 de 30 antes de detectar el curso en la pregunta y 30 de 30 después. Los dos fallos iniciales recuperaban otros cursos o materias parecidas.
- Rechazos correctos: 3 de 3.

Nueve de las 30 preguntas se añadieron para comprobar este arreglo en otros cursos, y sus páginas se tomaron de los metadatos del troceado. El 100 % indica que no hay fallos conocidos en este conjunto, no que el sistema nunca falle.

El conjunto de evaluación es pequeño y lo escribió quien diseñó el sistema: orienta, pero no garantiza la calidad.

## Límites

- La LOMLOE contiene modificaciones de la LOE, no el texto consolidado.
- El corpus es una foto fija; no detecta cambios normativos posteriores.
- Las tablas (por ejemplo, las del Anexo I del Decreto 64) se extraen como texto lineal y pueden perder la relación entre filas y columnas.
- La detección depende del formato actual de los boletines; otras normas pueden requerir nuevos patrones.
