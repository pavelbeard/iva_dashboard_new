FROM pavelbeard/monitor-nginx:v1.0

RUN rm /etc/nginx/conf.d/default.conf
COPY nginx.conf /etc/nginx/nginx.conf