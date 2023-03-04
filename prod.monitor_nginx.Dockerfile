FROM pavelbeard/monitor-nginx:v1.0

RUN rm /etc/nginx/nginx.conf
COPY configs/prod.nginx.conf /etc/nginx/nginx.conf



