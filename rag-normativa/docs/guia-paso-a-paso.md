# Guía: cómo construir un RAG sobre normativa

Esta guía explica cómo se ha construido este proyecto y por qué, pensando en quien hace su primer RAG. Sirve para reproducirlo o adaptarlo a otros documentos. El código completo está en `src/rag_normativa/`.

Si es tu primera vez, lee antes [Conceptos: tu primer RAG explicado desde cero](conceptos.md). Cada paso empieza con un apartado **Qué vas a hacer** en lenguaje sencillo, y los fragmentos de código son extractos para entender la idea: la versión completa está en cada módulo.

## 1. Qué es un RAG

Un modelo de lenguaje no conoce con fiabilidad el texto exacto de un decreto: puede inventar un artículo y sonar convincente. Un RAG (*Retrieval-Augmented Generation*, «generación aumentada con recuperación») equivale a darle antes las páginas adecuadas. Funciona en dos fases:

1. **Recuperar** los fragmentos relevantes de tus documentos.
2. **Generar** la respuesta usando solo esos fragmentos, citándolos.

La calidad depende sobre todo de la recuperación: si el fragmento correcto no llega al modelo, la respuesta no puede ser buena.

## 2. Prepara el proyecto

**Qué vas a hacer:** crear una carpeta aislada con su propio Python y sus bibliotecas (el *entorno virtual*), para que el proyecto no interfiera con nada más. `uv` se encarga de ello, y Ollama ejecuta los modelos en tu ordenador.

```bash
uv init --package rag-normativa
```

Dependencias, es decir, bibliotecas de terceros que reutilizamos:

| Biblioteca | Para qué sirve |
|---|---|
| `pymupdf` | Leer el texto de los PDF |
| `numpy` | Operar con vectores (listas de números) |
| `rank-bm25` | Buscar por palabras |
| `requests` | Comunicarse con Ollama |
| `mcp` | Crear el servidor que usa Claude |
| `pyyaml` | Leer las preguntas de evaluación |

Descarga también el modelo de embeddings, el que convierte texto en números:

```bash
ollama pull bge-m3
```

Mantén los PDF y el índice fuera de git: añade sus rutas a `.gitignore`.

## 3. Conoce tus documentos antes de programar

**Qué vas a hacer:** inspeccionar los archivos para decidir con datos cómo tratarlos. Es el paso que más se salta quien empieza, y el que evita más problemas.

Antes de elegir técnicas, responde a estas preguntas abriendo los PDF con código:

- **¿Tienen texto o son imágenes?** Cuenta los caracteres por página. Aquí todas tenían texto, así que no hizo falta OCR, la técnica que lee texto dentro de imágenes.
- **¿Qué se repite en cada página?** Cabeceras, fechas o códigos de verificación son ruido.
- **¿Cómo se marcan las divisiones?** En estos boletines aparecen `Artículo 22. Promoción y permanencia`, `DISPOSICIÓN FINAL PRIMERA`, títulos de materia en mayúsculas y `2º ESO.`.

Ojo: una norma puede usar formatos distintos. El Decreto 64 pone `Artículo 1` y el título en la línea siguiente; el 65, todo en una línea.

## 4. Extrae el texto conservando la página

**Qué vas a hacer:** convertir cada PDF en texto limpio, recordando de qué página viene cada línea.

La página es parte de la cita, así que se guarda desde el principio. El *ruido* (texto repetido sin contenido, como las cabeceras) se elimina comparando cada línea completa con *expresiones regulares*, que son patrones para reconocer texto. Por ejemplo, `\d+` significa «uno o más dígitos» (`extract.py`):

```python
_RUIDO = [re.compile(p, re.IGNORECASE) for p in (
    r"BOLET[IÍ]N OFICIAL DEL ESTADO",
    r"P[aá]g\. \d+",
    r"cve: BOE-[A-Z0-9-]+",
)]

def is_noise(line: str) -> bool:
    return any(p.fullmatch(line) for p in _RUIDO)
```

`fullmatch` evita borrar frases normales que solo contengan esas palabras.

## 5. Trocea siguiendo la estructura

**Qué vas a hacer:** dividir las normas en trozos manejables, llamados *fragmentos* o *chunks*. Cuando alguien pregunte, se recuperarán unos pocos en lugar de 793 páginas.

Partir cada N caracteres separa un artículo de su título o mezcla dos materias. Es mejor recorrer las líneas manteniendo un **estado**, es decir, recordando en qué sección, materia, curso y bloque estamos, y cerrar el fragmento cuando empieza una división nueva (`chunking.py`).

Si una división es demasiado larga, se parte en ventanas de hasta 1.500 caracteres con 200 de *solape*: cada trozo repite el final del anterior, para no perder ideas en el corte.

Cada fragmento guarda sus *metadatos*, los datos sobre el fragmento: norma, páginas, sección, materia, curso y bloque. Además, se antepone una cabecera al texto que se convierte en vector, porque los currículos repiten frases casi idénticas entre materias:

```python
@property
def embedding_text(self) -> str:
    cabecera = " | ".join(x for x in (self.norma, self.section, self.materia, self.curso, self.bloque) if x)
    return f"{cabecera}\n{self.text}"
```

**Comprueba el resultado antes de seguir**: número de fragmentos, tamaño máximo, lista de secciones y materias detectadas. Es más barato corregir aquí que depurar respuestas malas después.

## 6. Crea los embeddings

**Qué vas a hacer:** representar el significado de cada fragmento con números, para poder buscar por sentido y no solo por palabras exactas.

Un *embedding* convierte un texto en un *vector*, una lista de números; los de `bge-m3` tienen 1.024. Es como situar cada texto en un mapa: los de significado parecido quedan cerca, aunque usen palabras distintas.

Para medir esa cercanía se usa la *similitud del coseno*: cerca de 1 significa muy parecido. Si se *normaliza* cada vector para que mida 1, esa medida se obtiene con una multiplicación sencilla, el producto escalar (`embeddings.py`):

```python
response = requests.post(f"{OLLAMA_URL}/api/embed", json={"model": model, "input": lote})
matriz = np.asarray(response.json()["embeddings"], dtype=np.float32)
matriz /= np.linalg.norm(matriz, axis=1, keepdims=True)
```

Usa el mismo modelo al indexar y al consultar. Por eso `meta.json` lo registra y la carga falla si no coincide.

Con pocos miles de fragmentos no necesitas una base de datos vectorial, un programa especializado en guardar vectores: basta comparar la pregunta con todos ellos.

## 7. Combina búsqueda semántica y léxica

**Qué vas a hacer:** dada una pregunta, encontrar los mejores fragmentos usando dos buscadores complementarios.

Cada método falla donde el otro acierta:

- Los **embeddings** (búsqueda semántica, por significado) entienden paráfrasis: «pasar de curso» encuentra «promoción».
- **BM25** (búsqueda léxica, por palabras) acierta en términos exactos: «artículo 28» o «CCL2». Da más valor a las palabras poco frecuentes y compensa la longitud de los textos.

Para unir ambas listas se usa *Reciprocal Rank Fusion* (RRF). Como las puntuaciones de cada buscador no son comparables, solo mira la posición: cada lista da `1 / (60 + posición)` y se suman. Un fragmento 1.º en una lista y 3.º en la otra obtiene 1/61 + 1/63 ≈ 0,0323, el doble que si solo apareciera 1.º en una (`retrieve.py`):

```python
def rrf(rankings, k=60):
    scores = {}
    for ranking in rankings:
        for rank, item in enumerate(ranking, 1):
            scores[item] = scores.get(item, 0.0) + 1.0 / (k + rank)
    return scores
```

Los filtros por norma, materia o curso se aplican antes de ordenar. Son los metadatos del paso 5 dando valor: una pregunta de 2º de ESO no debe competir con el mismo bloque de Bachillerato.

Esto se aprendió midiendo. Los currículos repiten frases casi iguales entre cursos, así que «Criterios de evaluación de Matemáticas de 2º de ESO» traía otros cursos. La solución no fue un filtro automático, que habría ocultado artículos generales al preguntar cómo se pasa «de primero a segundo de Bachillerato». `detect_curso` reconoce el curso en la pregunta y añade a RRF una tercera lista con fragmentos de ese curso, de modo que se favorecen sin excluir lo demás. Antes de corregirlo se añadieron preguntas de otros cursos, para no ajustar el sistema a un único ejemplo.

## 8. Genera respuestas con citas

**Qué vas a hacer:** dar al modelo los fragmentos encontrados y obligarle a responder solo con ellos.

El *prompt*, el texto que se envía al modelo, impone reglas claras (`answer.py`): usar solo los fragmentos, citar cada afirmación como `[F1]` y responder una frase exacta si no hay información. La *temperatura*, que controla cuánto varían las respuestas, se fija baja (0,1) para priorizar la precisión.

Las citas se comprueban con código, porque las instrucciones no son una garantía:

1. Si `[F9]` no existe entre los fragmentos, se marca como inválida.
2. Los párrafos sin cita generan un aviso.
3. Los `[F1]` válidos se sustituyen por la referencia completa, por ejemplo `[decreto-65-eso, Artículo 22, p. 15]`.

Esto detecta citas inventadas, pero no si una cita real respalda lo afirmado. Para eso hay que leer la fuente.

## 9. Conecta distintos modelos

**Qué vas a hacer:** ofrecer la misma búsqueda a modelos diferentes.

Separar recuperación y generación permite reutilizar la misma base:

- **Modelos locales**: la *CLI* (programa que se maneja con comandos) `ask` envía los fragmentos a Ollama por su *API*, la vía para que un programa pida algo a otro. Cambiar de modelo es cambiar `--model`.
- **Claude y otros clientes MCP**: MCP es un estándar, como un enchufe común, para conectar asistentes con herramientas externas. Un servidor expone la búsqueda como *herramientas*, y el propio cliente decide cuándo usarlas y redacta. Ten en cuenta que Claude funciona en la nube, así que los fragmentos recuperados se le envían como parte de la conversación.

`FastMCP` describe cada herramienta al cliente a partir de los tipos y del *docstring*, el comentario que explica la función:

```python
@mcp.tool()
def buscar_normativa(consulta: str, norma: str | None = None, k: int = 8) -> list[dict]:
    """Busca fragmentos relevantes. Cita cada afirmación con el campo 'cita'."""
```

Un servidor MCP por stdio no debe escribir nada propio en la salida estándar, porque ese canal transporta el protocolo.

### El mismo servidor en OpenCode

La ventaja de MCP es que el servidor no cambia al cambiar de cliente: solo hay que registrarlo. Cada programa tiene su archivo y su formato. Claude Code lee `.mcp.json`, y OpenCode, `opencode.json`:

```json
{
  "$schema": "https://opencode.ai/config.json",
  "mcp": {
    "servers": {
      "rag-normativa": {
        "type": "local",
        "command": ["uv", "run", "--quiet", "--project", "rag-normativa", "rag-normativa-mcp"],
        "codemode": false,
        "timeout": { "startup": 60000 }
      }
    }
  }
}
```

Qué significa cada campo:

- `type: "local"`: OpenCode arranca el servidor en tu ordenador.
- `command`: el programa que lanza y sus argumentos.
- `codemode: false`: muestra las herramientas directamente al modelo, lo que es más sencillo para un modelo local.
- `timeout.startup`: margen de arranque, en milisegundos.

Ollama no se configura aquí porque OpenCode lo detecta en `http://127.0.0.1:11434`. El formato de estos archivos puede cambiar entre versiones: si algo falla, consulta la [documentación de OpenCode](https://opencode.ai/docs/mcp-servers/).

Con este sistema es **el modelo quien decide si busca**, y nada valida sus citas. Por eso conviene pedirle expresamente que use la herramienta y revisar el resultado.

## 10. Evalúa con preguntas de referencia

**Qué vas a hacer:** comprobar con datos si el sistema encuentra lo que debe.

Sin medir, cada ajuste es una intuición. `eval/preguntas.yaml` es el *conjunto de evaluación*: recoge preguntas y la página donde está la respuesta:

```yaml
- {pregunta: "¿Cuándo promociona de curso un alumno de ESO en Madrid?", norma: decreto-65-eso, paginas: [15]}
- {pregunta: "¿Cuál es la capital de Francia?", sin_respuesta: true}
```

Dos reglas importantes:

- Localiza las páginas correctas **en el PDF**, no con tu buscador; si no, mides el sistema contra sí mismo.
- Incluye preguntas **sin respuesta**, para comprobar que el modelo sabe decir que no lo encuentra.

La métrica `hit@5` indica en cuántas preguntas aparece la página correcta entre los cinco primeros resultados.

## 11. Amplía el sistema

### Añadir una norma

1. Coloca el PDF en la raíz e ignóralo en `.gitignore`.
2. Añade una entrada `Norma(...)` en `config.py`.
3. Revisa cabeceras y formato de títulos; añade patrones si difieren.
4. Reconstruye el índice, revisa los fragmentos y añade preguntas de evaluación.

### Usar otro modelo

- **Chat**: `ollama pull <modelo>` y `--model <modelo>`. No requiere reindexar.
- **Embeddings**: define `RAG_EMBEDDING_MODEL` y **reconstruye el índice**, porque los vectores de modelos distintos no son comparables.

## 12. Lista de comprobación

- [ ] Los PDF tienen texto o se ha aplicado OCR.
- [ ] Las cabeceras y pies se eliminan.
- [ ] Cada fragmento conserva página y sección.
- [ ] Se han revisado fragmentos a mano contra el PDF.
- [ ] La búsqueda combina semántica y léxica.
- [ ] Las citas se validan con código.
- [ ] Hay evaluación, incluidas preguntas sin respuesta.
- [ ] PDF e índice no se versionan.
- [ ] Están documentados los límites: vigencia, texto consolidado y necesidad de verificar.
