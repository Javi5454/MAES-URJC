# Portfolio · Innovación Educativa

Blog estático autoalojado para el portfolio diario de clase: entradas en Markdown → **Hugo** → HTML servido por **nginx** en HTTP plano. El dominio y el HTTPS no son cosa de este proyecto: los pone el reverse proxy de tu servidor (Caddy, Traefik, Nginx Proxy Manager…).

> ¿No eres de terminal? Lee [GUIA.md](GUIA.md), que explica lo mismo paso a paso.

## Arquitectura

```
git push ──► GitHub ◄── (cada 5 min) contenedor hugo: git pull + hugo build ──► volumen site
                                                                                 │
   Internet ──► tu reverse proxy (HTTPS) ──► :8080 ──► contenedor web (nginx) ◄──┘
```

- No hay base de datos, PHP ni panel de administración, así que no hay nada que parchear aparte de las imágenes base.
- No se construye ninguna imagen propia: las dos son oficiales (`ghcr.io/gohugoio/hugo` y `nginx:alpine`), y nginx usa su configuración por defecto. Publicar es hacer push; el contenedor `hugo` lo recoge en ≤5 min.
- No depende de funciones de Portainer Business (re-pull, force redeploy, montar ficheros del repo): vale con Portainer CE o con `docker compose` a secas.
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
| `compose.yaml` | Todo el despliegue: servicio `hugo` (bucle pull + build) y servicio `web` (nginx sirviendo el volumen). Variables: `PORT` (por defecto `8080`) y `REPO`. |

## Desarrollo local

No hace falta instalar Hugo, basta con la imagen oficial. Lanza los comandos **desde esta carpeta** (`portfolio/`). Si lo haces desde la raíz del repo, Hugo no encuentra `hugo.toml` y todo devuelve 404.

```sh
cd "Innovación Educativa/portfolio"
# Servidor con live-reload en http://localhost:1313 (-D incluye borradores)
docker run --rm -p 1313:1313 -v "$PWD":/project ghcr.io/gohugoio/hugo:v0.167.0 server --bind 0.0.0.0 -D

# Nueva entrada desde la plantilla
docker run --rm -v "$PWD":/project ghcr.io/gohugoio/hugo:v0.167.0 new posts/2026-10-01-tema.md
```

La imagen de Hugo corre como uid 1000. Si tu usuario tiene otro uid, añade `--user "$(id -u):$(id -g)"`.

## Contenido multimedia

- **Imágenes:** usa un *page bundle*, es decir, `content/posts/2026-10-01-tema/index.md` con `foto.jpg` en la misma carpeta, y enlázala con `![alt](foto.jpg)`. Para imágenes compartidas entre entradas, ponlas en `static/img/` y enlaza `/img/x.jpg`.
- **Vídeo:** usa el shortcode nativo `{{< youtube ID >}}` (también existe `vimeo`). No subas vídeos al repo, porque git no es un CDN.
- El HTML crudo dentro del Markdown está desactivado (opción por defecto de Goldmark). Si lo necesitas, añade `markup.goldmark.renderer.unsafe = true` en `hugo.toml`.

## Despliegue (Portainer CE)

1. Ve a **Stacks → Add stack → Repository**.
   - Repository URL: `https://github.com/Javi5454/MAES-URJC`
   - Compose path: `Innovación Educativa/portfolio/compose.yaml`
   - **No hace falta activar GitOps updates**: la web se actualiza sola desde el contenedor `hugo`. Solo lo necesitarías si cambias el propio `compose.yaml`; en ese caso, pulsa **Pull and redeploy** a mano.
2. En **Environment variables** puedes cambiar `PORT` si el 8080 está ocupado.
3. Pulsa **Deploy the stack**. La web queda en `http://IP-del-servidor:8080`. La primera vez tarda unos segundos en aparecer, lo que tarda el clon y el primer build; mientras tanto nginx devuelve 403.

Si haces un fork, cambia la variable `REPO` por la URL de tu repo. Tiene que ser público: el contenedor clona sin credenciales.

Sin Portainer, en el propio servidor: `docker compose up -d` dentro de esta carpeta.

Para forzar una actualización sin esperar 5 minutos: `docker compose restart hugo` (o el botón *Restart* del contenedor `hugo` en Portainer).

## HTTPS / dominio (reverse proxy)

Este proyecto solo sirve HTTP en el puerto `PORT`. Para publicarlo con dominio, apunta a él el reverse proxy de tu servidor. Con Caddy:

```caddyfile
portfolio.tudominio.es {
	encode zstd gzip
	reverse_proxy IP-del-servidor:8080
}
```

- Si Caddy corre en Docker en la misma máquina, `localhost` dentro de su contenedor no es el host. Usa la IP LAN del servidor, o mete los dos stacks en una red Docker común y usa `reverse_proxy <contenedor-web>:80`. En ese caso puedes quitar `ports:` del servicio `web`.
- Caddy se encarga del certificado. Requisitos: DNS `A`/`AAAA` apuntando a tu IP pública y los puertos 80 y 443 del router redirigidos a la máquina de Caddy.
- La compresión la hace el proxy (`encode`): el nginx de este stack va con la configuración por defecto.

## Personalizar

- Textos: `hugo.toml` (`title`, `params.author`, `params.subtitle`, `params.asignatura`, `params.profesora`) y `content/_index.md`.
- Colores: variables `--paper`, `--grid`, `--pen` y `--margin-red` en `:root`. El modo oscuro tiene sus propias variables, repetidas en dos bloques: `prefers-color-scheme: dark` (tema del sistema) y `:root[data-theme="dark"]` (elegido con el botón). Si cambias una, cambia las dos. El botón de la cabecera guarda la elección en `localStorage` (`tema`); un script en `<head>` la aplica antes de pintar para que no haya parpadeo.
- Tipografías: Google Fonts, cargadas en `layouts/baseof.html`. Si quieres evitar peticiones a Google, descárgalas a `static/fonts/` y declara `@font-face`.
- Versión de Hugo: es el tag de la imagen del servicio `hugo` en `compose.yaml` (y el de los comandos de desarrollo local). Súbela a mano y prueba en local antes de hacer push.

## Problemas típicos

| Síntoma | Causa / solución |
|---|---|
| `bind: address already in use` / «port is already allocated» al desplegar | Otro servicio ocupa el 8080 (mira cuál con `sudo ss -ltnp 'sport = :8080'`). Pon otro puerto libre en la variable `PORT` del stack y apunta allí el proxy. |
| Nginx devuelve 403 en la portada | El contenedor `hugo` aún no ha generado la web o ha fallado. Mira sus logs. |
| La entrada no aparece | Tiene `draft: true` o una `date` futura (Hugo no publica entradas con fecha futura). |
| 502 desde el reverse proxy | El proxy no llega a `IP:PORT`. Comprueba con `curl http://IP-del-servidor:8080` desde la máquina del proxy. |
| El push no se refleja en la web | Aún no han pasado los 5 min o el build ha fallado. Mira los logs del contenedor `hugo`: si pone «Fallo al actualizar o generar la web», el error de Hugo está justo encima. |
| El contenedor `hugo` falla siempre en el `git pull` | Se ha reescrito el historial (force push). Borra el volumen `repo` y reinicia el stack: vuelve a clonar. |
| Error de permisos con `hugo` en local | El uid no coincide. Usa `--user "$(id -u):$(id -g)"`. |

## Fuera de alcance (a propósito)

Comentarios, buscador, analítica, RSS bonito, CMS web. Hugo genera RSS en `/index.xml` sin configurar nada. Si hace falta algo más, se añade cuando lo pidan.
