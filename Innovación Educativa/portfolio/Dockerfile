FROM ghcr.io/gohugoio/hugo:v0.167.0 AS build
COPY --chown=hugo . .
RUN hugo --minify

FROM caddy:2-alpine
COPY Caddyfile /etc/caddy/Caddyfile
COPY --from=build /project/public /srv
