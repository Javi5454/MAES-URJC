# Conceptos: tu primer RAG explicado desde cero

Este documento no da nada por sabido. Puedes leerlo de principio a fin o consultarlo cuando un término te suene raro. Los ejemplos salen de este proyecto.

## La idea en una imagen

Imagina que preguntas a un profesor muy elocuente por el artículo 22 del decreto de ESO. Puede responder de memoria y sonar convincente, pero equivocarse. Un RAG equivale a darle antes **las páginas exactas del decreto** y exigirle: «contesta solo con esto y di de dónde lo sacas».

```
PREPARACIÓN (se hace una vez)
PDF → sacar el texto → cortarlo en fragmentos → convertirlos en números → guardarlos

CONSULTA (cada pregunta)
pregunta → buscar los fragmentos más útiles → dárselos al modelo → respuesta con citas
```

Todo lo demás son detalles de estas dos fases.

## 1. Los modelos de IA

**Modelo de lenguaje (LLM, *Large Language Model*).** Programa entrenado con enormes cantidades de texto para predecir qué texto viene a continuación. Claude y Qwen lo son. No consulta una base de datos cuando responde: genera el texto a partir de patrones aprendidos.

**Alucinación.** Respuesta falsa pero convincente, como un artículo inventado. En normativa es especialmente peligrosa. El RAG la reduce, pero no la elimina.

**Prompt.** Todo el texto que se envía al modelo.

**Instrucción de sistema (*system prompt*).** Parte del prompt que fija el comportamiento general. Aquí dice, entre otras cosas, «usa únicamente los fragmentos proporcionados».

**Token.** Trozo pequeño de texto con el que trabaja un modelo; suele ser una palabra corta o parte de una palabra. Ojo: BM25 también habla de *tokens*, pero allí son simplemente palabras (sección 6).

**Ventana de contexto.** Cantidad máxima de texto que un modelo puede tener presente a la vez. Las tres normas suman 793 páginas: meterlas enteras en cada pregunta sería lento o imposible con muchos modelos. En `answer.py`, `num_ctx` fija esa ventana para Ollama.

**Temperatura.** Grado de variabilidad de la respuesta. Baja significa más predecible. Aquí es 0,1 porque interesa la precisión, no la creatividad.

**Modelo de pensamiento (*thinking*).** Algunos modelos razonan en un texto intermedio antes de contestar. El proyecto lo desactiva en Ollama con `think: false` y elimina esos bloques si aparecen.

**Modelo de chat y modelo de embeddings.** Son dos herramientas distintas:

| | Modelo de chat | Modelo de embeddings |
|---|---|---|
| Entra | Texto | Texto |
| Sale | Texto (la respuesta) | Una lista de números |
| Aquí | `qwen3.5` o Claude | `bge-m3` |

**Modelo local y modelo en la nube.** Uno local se ejecuta en tu ordenador; uno en la nube, en servidores de otra empresa. Claude funciona en la nube: los fragmentos que recupere por MCP se envían a Claude como parte de la conversación. La búsqueda y los embeddings se hacen en local.

## 2. RAG

**RAG (*Retrieval-Augmented Generation*).** «Generación aumentada con recuperación»: primero se **recupera** información de tus documentos y después se **genera** la respuesta con ella.

**Recuperación (*retrieval*).** Encontrar los fragmentos útiles para una pregunta.

**Generación.** Redactar la respuesta a partir de esos fragmentos.

**Corpus.** El conjunto de documentos del sistema. Aquí, las tres normas.

**Anclaje en las fuentes (*grounding*).** Obligar a que cada afirmación se apoye en un texto recuperado.

**Por qué no basta con «subir el PDF».** Con tres documentos largos, buscar primero aporta tres ventajas: se envía menos texto, se responde más deprisa y cada afirmación puede rastrearse hasta su página.

## 3. De PDF a texto

**Capa de texto.** Un PDF puede contener texto real, seleccionable, o solo imágenes de páginas. Tus tres PDF tienen texto en todas las páginas.

**OCR (*Optical Character Recognition*).** Técnica para leer texto dentro de imágenes. Solo haría falta si los PDF fueran escaneados, por eso aquí no se usa.

**Extracción.** Sacar el texto del PDF. Se hace con la biblioteca PyMuPDF, página a página, para no perder el número de página.

**Ruido.** Texto que no aporta contenido y confunde la búsqueda, como `BOLETÍN OFICIAL DEL ESTADO` en cada página.

**Expresión regular (*regex*).** Patrón para reconocer texto. Por ejemplo, `P[aá]g\. \d+` reconoce «Pág. 205»: `[aá]` admite cualquiera de las dos letras y `\d+` significa «uno o más dígitos».

**Página física y página impresa.** La física es la posición en el archivo PDF. La impresa es la que figura en el boletín. La página 15 del PDF de un decreto puede llevar impreso otro número. Las citas usan la física, porque es la que puedes abrir directamente.

## 4. Fragmentos

**Fragmento (*chunk*).** Trozo de un documento que se indexa y se recupera como unidad.

**Troceado (*chunking*).** Cómo se corta el texto. Es una de las decisiones más influyentes:

- Si es **demasiado grande**, el fragmento mezcla temas y gasta contexto.
- Si es **demasiado pequeño**, pierde información necesaria para entenderlo.

**Troceado por estructura.** Cortar por las divisiones del documento: artículos, disposiciones, materias, cursos y bloques. Aquí tiene sentido porque así se citan las normas.

**Solape (*overlap*).** Cuando una división supera los 1.500 caracteres, se parte y cada trozo repite hasta 200 caracteres del anterior. Así, una idea situada en el corte no desaparece.

**Metadatos.** Datos sobre un fragmento. Un fragmento de ejemplo:

```
norma:    decreto-65-eso
sección:  Anexo II
materia:  MATEMÁTICAS
curso:    2º ESO
bloque:   Criterios de evaluación
páginas:  234-235
texto:    Competencia específica 1. 1.1. Interpretar y analizar...
```

Sirven para citar y para filtrar.

## 5. Embeddings: cómo se busca por significado

**Vector.** Una lista ordenada de números, como `[0,12, -0,40, 0,88]`.

**Dimensión.** Cuántos números tiene el vector. Los de `bge-m3` tienen 1.024.

**Embedding.** Vector que representa el significado de un texto. Piensa en un mapa: los textos con significado parecido quedan cerca, aunque usen palabras distintas. Así, «pasar de curso» queda cerca de «promoción de curso», y lejos de «Plan de Contingencia».

Nadie decide qué significa cada número: el modelo aprende esa organización durante su entrenamiento.

**Similitud del coseno.** Mide si dos vectores apuntan en la misma dirección. Se interpreta así:

- Cerca de 1: significado muy parecido.
- Cerca de 0: poca relación.

**Normalizar.** Ajustar cada vector para que su longitud sea 1. Después, la similitud del coseno se calcula con una multiplicación sencilla, el **producto escalar**.

**Búsqueda semántica.** Convertir la pregunta en vector y buscar los fragmentos cuyos vectores están más cerca. Se llama semántica porque atiende al significado.

**Índice.** Estructura preparada para buscar rápido, como el índice de un libro. Aquí son los archivos de `data/`:

| Archivo | Contenido |
|---|---|
| `chunks.jsonl` | Fragmentos y metadatos. JSONL es un formato de texto con un registro por línea |
| `embeddings.npy` | Los vectores, en formato binario de NumPy |
| `meta.json` | Qué modelo se usó |

**NumPy.** Biblioteca de Python para operar con muchos números de golpe.

**Base de datos vectorial.** Programa especializado en guardar y buscar vectores. Es útil con millones. Con 2.326 fragmentos se pueden comparar todos directamente, lo que se llama **búsqueda exacta**.

**Reindexar.** Volver a construir el índice. Hay que hacerlo si cambian los PDF, el troceado o el modelo de embeddings: los vectores de modelos distintos no son comparables.

## 6. Búsqueda por palabras

**Búsqueda léxica.** Busca coincidencias de palabras, no de significado. Es mejor con términos exactos como «artículo 28» o «CCL2».

**Tokenizar.** Separar un texto en palabras. El proyecto pasa a minúsculas y quita acentos: «Evaluación» se convierte en `evaluacion`.

**Palabras vacías (*stopwords*).** Palabras muy comunes, como «de» o «la», que apenas ayudan a distinguir textos y se ignoran.

**BM25.** Fórmula clásica que puntúa un fragmento según tres ideas:

1. Las palabras **raras** valen más: «estocástico» distingue más que «educación».
2. Repetir una palabra ayuda, pero cada repetición aporta menos.
3. Se compensa la longitud, para que un texto no gane solo por ser largo.

## 7. Búsqueda híbrida

**Búsqueda híbrida.** Combinar búsqueda semántica y léxica, porque cada una acierta donde la otra falla.

**Ranking.** Lista ordenada de resultados.

**RRF (*Reciprocal Rank Fusion*).** Forma de unir varios rankings. Las puntuaciones de cada buscador están en escalas diferentes, así que RRF solo usa la posición. Cada lista da a un resultado `1 / (60 + posición)`, y se suman:

| Fragmento | Semántica | BM25 | Cálculo | Total |
|---|---|---|---|---|
| A | 1.º | 3.º | 1/61 + 1/63 | 0,0323 |
| B | 1.º | no aparece | 1/61 | 0,0164 |
| C | 2.º | 2.º | 1/62 + 1/62 | 0,0323 |

Aparecer bien situado en las dos listas puntúa mucho más que aparecer en una. El 60 es un valor habitual que suaviza la ventaja de las primeras posiciones.

**Top-k.** Número de resultados que se conservan. Por defecto, `k = 8`.

**Filtro.** Restricción previa por metadatos. `--curso "2º ESO"` evita que compitan fragmentos de otros cursos.

**Filtro estricto y preferencia.** Un filtro elimina todo lo que no cumple la condición. Una preferencia solo da ventaja. Cuando escribes «2º de ESO» en la pregunta, el sistema añade una tercera lista a RRF con fragmentos de ese curso: suben posiciones, pero un artículo general también puede aparecer.

## 8. Citas y fiabilidad

**Cita.** Referencia a la fuente, por ejemplo `[decreto-65-eso, Artículo 22, p. 15]`.

**Identificador `[F1]`.** El modelo recibe los fragmentos numerados y escribe `[F1]`, más difícil de equivocar que una referencia larga. Después, el código lo sustituye por la cita completa.

**Validación.** Comprobación automática de que cada cita existe y de que los párrafos llevan alguna. **No confirma que la fuente diga lo que afirma el modelo**; eso lo tienes que revisar tú.

**Rechazo.** Cuando la información no está, el modelo debe contestar «No lo encuentro en estas normas.». Es un comportamiento deseado.

## 9. Cómo se conecta todo

**CLI (*Command Line Interface*).** Programa que se usa escribiendo comandos en la terminal, como `rag-normativa ask`.

**Ollama.** Programa que descarga y ejecuta modelos en tu ordenador.

**API.** Forma acordada para que un programa pida algo a otro. El proyecto llama a la API local de Ollama en `http://localhost:11434`, donde `localhost` significa «este mismo ordenador».

**API key.** Contraseña para usar una API de pago o remota. Este proyecto no la necesita.

**MCP (*Model Context Protocol*).** Estándar para conectar asistentes de IA con herramientas externas. Es como un enchufe común: el mismo servidor sirve para cualquier cliente compatible.

- **Servidor MCP:** ofrece las herramientas. Aquí, `mcp_server.py`.
- **Cliente MCP:** las usa. Por ejemplo, Claude Code.
- **Herramienta:** función que el modelo puede pedir que se ejecute, como `buscar_normativa`.
- **stdio:** canal por el que cliente y servidor se envían mensajes, usando la entrada y salida estándar del programa.

**Agente.** Programa en el que un modelo puede decidir qué herramientas usar para cumplir un objetivo, en lugar de limitarse a contestar. Claude Code y OpenCode son agentes.

**OpenCode.** Agente para la terminal que puede trabajar con modelos locales de Ollama y actuar como cliente MCP. Con él, un modelo local consulta este RAG igual que lo hace Claude.

**Capacidad `tools` (llamada a herramientas).** Habilidad de un modelo para pedir la ejecución de una herramienta con unos datos concretos. El modelo solo la solicita: quien la ejecuta es el agente. Sin esta capacidad, un modelo no puede usar MCP. `ollama show <modelo>` indica si la tiene.

**Permiso.** Confirmación que pide el agente antes de ejecutar una acción. `--auto` en OpenCode la aprueba sin preguntar, lo que resulta arriesgado porque también puede cubrir editar archivos o ejecutar comandos.

**Las dos rutas con un modelo local:**

| | `rag-normativa ask` | OpenCode + MCP |
|---|---|---|
| Quién busca | El programa, siempre | El modelo, si decide usar la herramienta |
| Validación de citas | Sí | No |
| Conversación con seguimiento | No | Sí |
| Mejor para | Consultas fiables y rápidas | Trabajar con la normativa junto a otros archivos |

## 10. Herramientas de programación

**Python.** Lenguaje en el que está escrito el proyecto.

**Biblioteca o dependencia.** Código de terceros que el proyecto reutiliza. Se declaran en `pyproject.toml`.

**Entorno virtual (`.venv`).** Carpeta con un Python y unas bibliotecas exclusivos del proyecto, para no interferir con el resto del ordenador.

**uv.** Herramienta que crea ese entorno e instala las dependencias. `uv.lock` anota las versiones exactas para poder reproducirlas.

**`.gitignore`.** Lista de archivos que git no debe versionar. Aquí incluye los PDF y el índice.

## 11. Cómo saber si funciona

**Test.** Comprobación automática de una pieza concreta: por ejemplo, que una cita inventada se detecta.

**Conjunto de evaluación.** Preguntas con su respuesta conocida. Aquí, `eval/preguntas.yaml` indica la norma y la página correctas.

**hit@5.** Porcentaje de preguntas en las que la página correcta aparece entre los 5 primeros resultados. Un 20 de 21 significa que falló en una.

Esta métrica solo evalúa la recuperación. Que aparezca el fragmento correcto no garantiza que el modelo lo interprete bien.

## Errores habituales al empezar

| Error | Consecuencia |
|---|---|
| Preocuparse por el modelo antes que por la recuperación | El mejor modelo no puede usar un fragmento que no recibe |
| Trocear sin mirar el documento | Artículos partidos y materias mezcladas |
| No guardar página ni sección | Respuestas imposibles de verificar |
| Cambiar el modelo de embeddings sin reindexar | Búsquedas sin sentido |
| No probar preguntas sin respuesta | El sistema inventa en lugar de admitir que no sabe |
| Confiar en una cita sin abrirla | Una cita real puede no respaldar la afirmación |
