FROM nginx:1.23.3-alpine

RUN rm /etc/nginx/conf.d/default.conf
COPY ../configs/nginx/nginx.conf /etc/nginx/nginx.conf