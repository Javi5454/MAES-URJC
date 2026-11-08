# RAG de normativa educativa

Consulta con citas la LOMLOE y los decretos 64/2022 (Bachillerato) y 65/2022 (ESO) de la Comunidad de Madrid. Funciona en local y sirve para dos tipos de modelo:

- **Claude** (Code o Desktop), mediante un servidor MCP. No necesita API key.
- **Cualquier modelo de Ollama**, mediante una CLI.
- **OpenCode con un modelo local**, también mediante MCP y sin enviar datos fuera de tu ordenador.

Más información:

- [Conceptos: tu primer RAG explicado desde cero](docs/conceptos.md) (empieza por aquí si es tu primer RAG)
- [Guía paso a paso para construir un RAG así](docs/guia-paso-a-paso.md)
- [Arquitectura y decisiones](docs/arquitectura.md)

> Herramienta de estudio, no asesoramiento jurídico. La LOMLOE aquí indexada es la ley que **modifica** la LOE, no el texto consolidado, y las normas pueden haber cambiado. Comprueba las citas en el PDF y la versión vigente.

## Requisitos

- macOS o Linux, con [uv](https://docs.astral.sh/uv/) y [Ollama](https://ollama.com/) en marcha.
- Los tres PDF en la raíz del repositorio. Están ignorados por git, así que hay que tenerlos en local:
  - `BOE-A-2020-17264.pdf`
  - `Decreto-64-2022-Curriculum-de-Bachillerato_Madrid.pdf`
  - `Decreto-65-2022_ordenacion-y-el-curriculo-ESO-en-CAM.pdf`

## Instalación

Desde la carpeta `rag-normativa/`:

```bash
uv sync --extra dev
```

```bash
ollama pull bge-m3
```

```bash
uv run rag-normativa index
```

El índice se guarda en `data/`. Hay que reconstruirlo si cambian los PDF, el troceado o el modelo de embeddings.

## Uso desde la terminal

Buscar fragmentos, sin modelo de chat:

```bash
uv run rag-normativa search "criterios de evaluación" --materia matemáticas --curso "2º ESO"
```

Preguntar a un modelo local:

```bash
uv run rag-normativa ask "¿Cuándo promociona de curso un alumno de ESO?" --norma decreto-65-eso
```

Usar otro modelo de Ollama:

```bash
uv run rag-normativa ask "¿Qué es el Plan de Contingencia?" --model llama3.2
```

Filtros disponibles: `--norma` (`lomloe`, `decreto-64-bach`, `decreto-65-eso`), `--materia`, `--curso` y `-k`. Si la pregunta menciona un curso («2º de ESO», «segundo de Bachillerato»), la búsqueda lo favorece automáticamente sin excluir el resto. Usa `--curso` cuando quieras limitar los resultados **solo** a ese curso.

Después de responder, `ask` avisa de las citas inexistentes (y termina con código 1) y de los párrafos sin cita.

## Uso desde Claude

### Claude Code

El archivo `.mcp.json` de la raíz del repositorio ya registra el servidor. Abre Claude Code en la raíz, acepta el servidor `rag-normativa` y pregunta, por ejemplo: «Según el decreto de ESO de Madrid, ¿cuándo se obtiene el título?».

### Claude Desktop

Añade esto en *Settings → Developer → Edit Config*, con la ruta real del repositorio y la ruta absoluta de `uv` (`which uv`):

```json
{
  "mcpServers": {
    "rag-normativa": {
      "command": "/opt/homebrew/bin/uv",
      "args": ["run", "--quiet", "--project", "/RUTA/AL/REPO/rag-normativa", "rag-normativa-mcp"]
    }
  }
}
```

## Uso desde OpenCode con un modelo local

[OpenCode](https://opencode.ai/docs/) es un asistente de programación para la terminal. Puede usar este RAG a través de MCP y trabajar con un modelo de Ollama, de modo que **las normas y la conversación se quedan en tu ordenador**. El archivo `opencode.json` de la raíz del repositorio ya registra el servidor.

Requisitos: haber construido el índice, tener Ollama en marcha y usar un modelo con la capacidad `tools`. Compruébalo con:

```bash
ollama show qwen3.5:35b-a3b
```

Abre OpenCode **desde la raíz del repositorio**, porque la ruta del servidor es relativa a esa carpeta:

```bash
opencode -m ollama/qwen3.5:35b-a3b
```

O lanza una sola pregunta:

```bash
opencode run -m ollama/qwen3.5:35b-a3b "Usa buscar_normativa y responde citando el campo cita: ¿cuándo promociona un alumno de ESO en Madrid?"
```

Aprueba la herramienta cuando OpenCode lo pida. Evita `--auto` en este repositorio: aprobaría también otras acciones del modelo, como editar archivos o ejecutar comandos.

Probado con OpenCode 2.2.5 y `qwen3.5:35b-a3b`. Ten en cuenta:

- **Pide siempre que use la herramienta y cite.** OpenCode es un agente generalista y un modelo local puede contestar de memoria si no se lo indicas.
- **No hay validación automática de citas.** Esa comprobación solo existe en `rag-normativa ask`. Con OpenCode, revisa tú las citas; `leer_pagina` te ayuda a verificarlas.
- **Una cita real no garantiza una respuesta correcta.** En la prueba, el modelo citó bien el artículo 23 del decreto de ESO, pero presentó «superar todas las materias» como requisito, cuando el decreto dice que quienes las superan titulan «en todo caso» y deja la decisión al equipo docente en otros supuestos.
- **`opencode mcp list` puede indicar «No MCP servers configured»** aunque el servidor funcione: ocurrió en la versión probada. Para comprobarlo, usa `/mcps` dentro de OpenCode o haz una consulta de prueba.
- **Si el modelo olvida instrucciones o corta los resultados**, puede faltarle contexto. Reinicia Ollama con una ventana mayor, por ejemplo `OLLAMA_CONTEXT_LENGTH=16384 ollama serve`, o reduce `k`.

## Herramientas MCP

| Herramienta | Función |
|---|---|
| `listar_normas` | Lista las normas y sus identificadores |
| `buscar_normativa` | Búsqueda híbrida con filtros; cada resultado trae su `cita` |
| `leer_pagina` | Devuelve una página completa del PDF para verificar una cita |

## Que el modelo use el RAG sin pedírselo

Un modelo conectado por MCP decide por sí mismo si usa una herramienta. Para que tienda a usarla siempre:

| Programa | Dónde está la instrucción |
|---|---|
| Claude Code | `CLAUDE.md`, en la raíz del repositorio, que importa `AGENTS.md` |
| OpenCode | `AGENTS.md`, en la raíz del repositorio |
| Claude Desktop | Hay que añadirla en las instrucciones de un Proyecto o en tus preferencias, porque no lee estos archivos |

Abre una sesión nueva desde la raíz del repositorio para que se apliquen. Aun así, el modelo podría ignorarlas. La única vía donde la búsqueda ocurre siempre es `rag-normativa ask`.

## Configuración

| Variable | Valor por defecto |
|---|---|
| `OLLAMA_URL` | `http://localhost:11434` |
| `RAG_EMBEDDING_MODEL` | `bge-m3` |
| `RAG_CHAT_MODEL` | `qwen3.5:35b-a3b` |

## Comprobaciones

```bash
uv run pytest
```

```bash
uv run rag-normativa evaluate --model qwen3.5:35b-a3b
```

## Problemas frecuentes

| Síntoma | Solución |
|---|---|
| «No hay índice» | Ejecuta `uv run rag-normativa index` |
| «No puedo conectar con Ollama» | Abre Ollama o ejecuta `ollama serve` |
| «¿Has descargado el modelo?» | Ejecuta `ollama pull <modelo>` |
| El servidor no aparece en Claude | Reinicia el cliente y comprueba la ruta de `uv` |
| OpenCode no encuentra las herramientas | Ábrelo desde la raíz del repositorio y revisa `/mcps` |
