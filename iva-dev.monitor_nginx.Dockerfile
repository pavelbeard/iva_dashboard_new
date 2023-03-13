FROM pavelbeard/monitor-nginx:v1.0

RUN rm /etc/nginx/nginx.conf
COPY configs/iva-dev.nginx.conf /etc/nginx/nginx.conf



