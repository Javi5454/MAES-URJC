# Guía rápida: tu portfolio de clase en una web propia

Esta guía es para quien quiere tener su diario de clase como una web bonita **sin pelearse con la informática**. Si te manejas con terminal y Docker, tienes la versión técnica en [README.md](README.md).

## ¿Qué es esto?

Es una pequeña web con aspecto de cuaderno cuadriculado. Cada día escribes una entrada contando:

- **Qué hicimos** en clase.
- **Tu reflexión**: qué te llevas y qué harías distinto como docente.
- **Material**, si lo tienes: fotos, vídeos…

Las entradas aparecen ordenadas por fecha, con el día escrito en el margen rojo, como en un cuaderno de verdad.

## Escribir una entrada nueva (desde el navegador)

No necesitas instalar nada. Todo se hace en la web de GitHub:

1. Entra en el repositorio y ve a la carpeta `Innovación Educativa/portfolio/content/posts/`.
2. Pulsa **Add file → Create new file**.
3. Ponle de nombre la fecha y el tema, sin espacios ni tildes, por ejemplo `2026-10-01-aprendizaje-cooperativo.md`.
4. Pega esto y rellénalo:

   ```
   ---
   title: "Aprendizaje cooperativo"
   date: 2026-10-01
   ---

   ## Qué hicimos

   Escribe aquí...

   ## Reflexión

   Escribe aquí...

   ## Material
   ```

5. Pulsa **Commit changes**. En unos minutos la entrada aparece en la web.

### Pequeños trucos para escribir

| Quieres… | Escribe… |
|---|---|
| Un subtítulo | `## Mi subtítulo` |
| **Negrita** | `**texto**` |
| *Cursiva* | `*texto*` |
| Una lista | Líneas que empiecen por `- ` |
| Un enlace | `[texto](https://dirección.com)` |
| Una cita destacada | Una línea que empiece por `> ` |

## Añadir fotos

1. Al crear la entrada, en vez de un fichero suelto crea una **carpeta**: escribe el nombre como `2026-10-01-tema/index.md` y GitHub crea la carpeta él solo.
2. Entra en esa carpeta y sube la foto con **Add file → Upload files**.
3. En el texto de la entrada pon: `![Descripción de la foto](nombre-de-la-foto.jpg)`

Consejo: haz las fotos más pequeñas antes de subirlas (con 1–2 MB sobra). Así la web carga rápido.

## Añadir vídeos

Los vídeos no se suben a la web porque pesan demasiado. Súbelos a **YouTube** (pueden ser "ocultos") y copia el código del vídeo, que es lo que va detrás de `v=` en la dirección. Por ejemplo, en `youtube.com/watch?v=abc123XYZ` el código es `abc123XYZ`.

En la entrada escribe:

```
{{< youtube abc123XYZ >}}
```

## Guardar una entrada sin publicarla

Añade `draft: true` debajo de la fecha. Mientras esté así, la entrada no se ve en la web. Cuando esté lista, borra esa línea.

## Tu presentación (foto, quién eres y enlaces)

La página **Presentación** está en la carpeta `content/presentacion/`:

1. Sube tu foto a esa carpeta con **Add file → Upload files** y llámala `foto.jpg`. Si le pones otro nombre, cámbialo también en la línea `foto:`. Da igual el tamaño, porque la web la recorta sola.
2. Edita `index.md`: escribe sobre ti debajo de la segunda línea `---`.
3. En `enlaces` cambia o añade los tuyos, siempre con la misma forma:
   ```
     - nombre: "Mi blog"
       url: "https://miblog.com"
   ```
   Respeta los espacios del principio: cuentan.

Si no quieres foto, deja `foto: ""`.

## Cambiar el título o tu nombre

Abre el fichero `hugo.toml`, pulsa el lápiz ✏️ para editar y cambia lo que va entre comillas en `title`, `author`, `subtitle`, `asignatura` y `profesora`. El texto de bienvenida de la portada está en `content/_index.md`.

## Montarla por primera vez

Esta parte es la única "técnica" y solo se hace una vez. Necesitas un servidor (un ordenador o miniPC siempre encendido) con **Docker** y **Portainer**. Si alguien te lo ha montado, pásale esta lista:

1. En Portainer: **Stacks → Add stack → Repository**.
2. Pega la dirección del repositorio de GitHub. Tiene que ser **público**.
3. En *Compose path* escribe: `Innovación Educativa/portfolio/compose.yaml`
4. Pulsa **Deploy the stack**.

No hace falta activar nada más: la web mira GitHub cada 5 minutos y se actualiza sola. Funciona con la versión gratuita de Portainer (Community Edition).

Con eso la web ya funciona dentro de tu casa: entra en `http://dirección-del-servidor:8080` desde el navegador. Si ese puerto ya lo usa otra cosa, añade en Portainer la variable `PORT` con otro número, por ejemplo `8090`.

### Que se vea desde internet (con candado 🔒)

Esta web no se encarga de eso, para que puedas tener varias webs en el mismo servidor. Lo hace un programa aparte, llamado **reverse proxy**, que tiene quien gestione el servidor (por ejemplo, Caddy). Hacen falta tres cosas:

1. Un **dominio**, es decir, un nombre como `miportfolio.duckdns.org`. DuckDNS es gratis.
2. Que el dominio apunte a la IP de tu casa y que el router deje pasar los puertos **80** y **443** hacia el servidor.
3. Que el reverse proxy envíe ese dominio a la web, al puerto `8080`. Pásale a quien lo gestione el apartado "HTTPS / dominio" del [README.md](README.md).

## Si algo no va

- **Mi entrada no aparece:** revisa que no tenga `draft: true` y que la fecha no sea de un día futuro. Espera unos 5 minutos.
- **La foto no se ve:** comprueba que el nombre de la foto en el texto es exactamente igual al del fichero, mayúsculas incluidas.
- **La web no carga:** pregunta a quien gestione el servidor y enséñale el [README.md](README.md).
