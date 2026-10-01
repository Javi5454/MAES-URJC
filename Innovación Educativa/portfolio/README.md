# Portfolio · Innovación Educativa

Blog estático autoalojado para el portfolio diario de clase: entradas en Markdown → **Hugo** → HTML servido por **Caddy**, que se encarga también del HTTPS (Let's Encrypt) automáticamente.

> ¿No eres de terminal? Lee [GUIA.md](GUIA.md), que explica lo mismo paso a paso.

## Arquitectura

```
git push ──► Portainer (GitOps polling) ──► docker build
                                             ├─ stage 1: ghcr.io/gohugoio/hugo  →  hugo --minify  →  /project/public
                                             └─ stage 2: caddy:2-alpine         ←  COPY public → /srv
                                                          │
                                   :80 / :443 (tcp+udp) ◄─┘  certificados en el volumen caddy_data
```

- No hay base de datos, PHP ni panel de administración, así que no hay nada que parchear aparte de las imágenes base.
- La imagen final contiene la web ya renderizada. Desplegar consiste en reconstruir la imagen.
- El tema es propio y mínimo, sin submódulos ni temas de terceros.

## Ficheros

| Ruta | Qué es |
|---|---|
| `hugo.toml` | Título, autor, subtítulo, asignatura, profesora y paginación. |
| `content/_index.md` | Texto de presentación de la portada (debajo van asignatura, profesora y el índice de entradas, numerado por orden cronológico). |
| `content/posts/*.md` | Las entradas. Las que tienen `draft: true` no se publican. |
| `archetypes/posts.md` | Plantilla que usa `hugo new posts/...`. |
| `content/presentacion/index.md` | Página «Presentación»: texto en Markdown; `foto` (fichero en la misma carpeta, Hugo lo recorta a 480×600 en WebP) y `enlaces` (lista `nombre`/`url`) en el front matter. El favicon de cada enlace se descarga en el build (`resources.GetRemote` al servicio de favicons de Google) y se sirve local; si no hay red, el enlace sale sin icono. Los `mailto:` llevan un sobre SVG. |
| `layouts/{baseof,list,single,presentacion}.html` | El tema: esqueleto con navegación, portada (índice), entrada y presentación (`layout: presentacion`). |
| `static/css/style.css` | Estilos. Los tokens de color y tipografía están en `:root`. |
| `Dockerfile` | Build multi-stage Hugo → Caddy. |
| `Caddyfile` | `{$DOMAIN}` + `file_server` + compresión. |
| `compose.yaml` | Servicio, puertos y volúmenes, más la variable `DOMAIN`. |

## Desarrollo local

No hace falta instalar Hugo, basta con la imagen oficial. Lanza los comandos **desde esta carpeta** (`portfolio/`). Si lo haces desde la raíz del repo, Hugo no encuentra `hugo.toml` y todo devuelve 404.

```sh
cd "Innovación Educativa/portfolio"
# Servidor con live-reload en http://localhost:1313 (-D incluye borradores)
docker run --rm -p 1313:1313 -v "$PWD":/project ghcr.io/gohugoio/hugo:v0.167.0 server --bind 0.0.0.0 -D

# Nueva entrada desde la plantilla
docker run --rm -v "$PWD":/project ghcr.io/gohugoio/hugo:v0.167.0 new posts/2026-10-01-tema.md

# Probar la imagen de producción tal cual (HTTP en :80)
docker compose up --build
```

La imagen de Hugo corre como uid 1000. Si tu usuario tiene otro uid, añade `--user "$(id -u):$(id -g)"`.

## Contenido multimedia

- **Imágenes:** usa un *page bundle*, es decir, `content/posts/2026-10-01-tema/index.md` con `foto.jpg` en la misma carpeta, y enlázala con `![alt](foto.jpg)`. Para imágenes compartidas entre entradas, ponlas en `static/img/` y enlaza `/img/x.jpg`.
- **Vídeo:** usa el shortcode nativo `{{< youtube ID >}}` (también existe `vimeo`). No subas vídeos al repo, porque git no es un CDN.
- El HTML crudo dentro del Markdown está desactivado (opción por defecto de Goldmark). Si lo necesitas, añade `markup.goldmark.renderer.unsafe = true` en `hugo.toml`.

## Despliegue (Portainer)

1. Ve a **Stacks → Add stack → Repository**.
   - Repository URL: este repo. Si es privado, activa *Authentication* con un PAT de GitHub con permiso `contents:read`.
   - Compose path: `Innovación Educativa/portfolio/compose.yaml`
   - Activa **GitOps updates**, en modo *Polling* cada 5 min aproximadamente, y marca **Re-pull image and redeploy** o *Force redeployment*. Desde ese momento, cada `git push` acaba publicado.
2. En **Environment variables**, pon `DOMAIN` cuando tengas dominio. Mientras no exista, se usa `:80` (HTTP plano).

Sin Portainer, en el propio servidor: `git pull && docker compose up -d --build`.

## HTTPS / dominio

Requisitos para que Caddy obtenga el certificado:
- Un registro DNS `A` (y `AAAA` si tienes IPv6) que apunte a la IP pública del servidor. Sirven DuckDNS y servicios similares.
- Los puertos **80 y 443** abiertos/redirigidos en el router hacia el servidor. El 80 es necesario para el challenge HTTP-01.
- `DOMAIN=portfolio.tudominio.es` en el entorno del stack.

Caddy renueva solo. **No borres el volumen `caddy_data`**: si lo pierdes, Caddy vuelve a pedir certificados y puedes acabar chocando con los rate limits de Let's Encrypt.

## Personalizar

- Textos: `hugo.toml` (`title`, `params.author`, `params.subtitle`, `params.asignatura`, `params.profesora`) y `content/_index.md`.
- Colores: variables `--paper`, `--grid`, `--pen` y `--margin-red` en `:root`. El modo oscuro tiene sus propias variables en el bloque `prefers-color-scheme: dark`.
- Tipografías: Google Fonts, cargadas en `layouts/baseof.html`. Si quieres evitar peticiones a Google, descárgalas a `static/fonts/` y declara `@font-face`.
- Versión de Hugo: es el tag del `FROM` en `Dockerfile`. Súbela a mano y prueba en local antes de hacer push.

## Problemas típicos

| Síntoma | Causa / solución |
|---|---|
| `bind: address already in use` al levantar el stack | Otro servicio ocupa el puerto 80 o 443. Cambia el mapeo en `compose.yaml` (p. ej. `8080:80`), aunque entonces no habrá HTTPS automático. |
| La entrada no aparece | Tiene `draft: true` o una `date` futura (Hugo no publica entradas con fecha futura). |
| El certificado no se emite | Revisa `docker logs <contenedor>`. Normalmente el DNS aún no se ha propagado o el puerto 80 no llega desde fuera. |
| El push no se refleja en la web | El polling de Portainer aún no ha saltado o el build ha fallado. Mira el estado del stack en Portainer. |
| Error de permisos con `hugo` en local | El uid no coincide. Usa `--user "$(id -u):$(id -g)"`. |

## Fuera de alcance (a propósito)

Comentarios, buscador, analítica, RSS bonito, CMS web. Hugo genera RSS en `/index.xml` sin configurar nada. Si hace falta algo más, se añade cuando lo pidan.
