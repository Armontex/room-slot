FROM nginx:1.27-alpine

RUN apk add --no-cache openssl \
    && mkdir -p /etc/nginx/certs \
    && openssl req -x509 -nodes -days 365 \
    -newkey rsa:2048 \
    -keyout /etc/nginx/certs/roomslot.key \
    -out /etc/nginx/certs/roomslot.crt \
    -subj "/CN=roomslot.local" \
    -addext "subjectAltName=DNS:roomslot.local,DNS:api.roomslot.local"

COPY nginx.conf /etc/nginx/nginx.conf
