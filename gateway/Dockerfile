FROM nginx:1.28.0-alpine-slim

RUN apk update --no-cache \
    && apt-get upgrade -y \
    && rm -rf /var/lib/apt/lists/*

COPY app.conf /etc/nginx/conf.d/default.conf