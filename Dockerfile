# Fáze 1: Build aplikace pomocí Node.js
FROM node:20-alpine as build

WORKDIR /app

# Kopírujeme package.json a lock pro instalaci závislostí
COPY webapp/package*.json ./
RUN npm ci

# Kopírujeme zdrojové kódy
COPY webapp/ .

# Vytvoříme produkční build (do složky dist)
RUN npm run build

# Fáze 2: Servírování statických souborů přes NGINX
FROM nginx:alpine

# Nakopírujeme buildnuté soubory z fáze 1
COPY --from=build /app/dist /usr/share/nginx/html

# Povolíme SPA routing tím, že vše směrujeme na index.html
RUN echo 'server { \
    listen       80; \
    server_name  localhost; \
    root   /usr/share/nginx/html; \
    include /etc/nginx/mime.types; \
    \
    location / { \
        index  index.html index.htm; \
        try_files $uri $uri/ /index.html; \
    } \
    \
    # Správné nastavení cache pro statické assety \
    location /assets/ { \
        try_files $uri =404; \
        expires 1y; \
        add_header Cache-Control "public, max-age=31536000, immutable"; \
    } \
}' > /etc/nginx/conf.d/default.conf

EXPOSE 80

CMD ["nginx", "-g", "daemon off;"]
