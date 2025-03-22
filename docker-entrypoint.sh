#!/bin/bash
envsubst < /etc/caddy/Caddyfile.template > /etc/caddy/Caddyfile
exec "$@"
