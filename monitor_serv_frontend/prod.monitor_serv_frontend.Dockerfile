##### STAGE 1 #####
FROM node:18.15.0-alpine3.17 as build

COPY package.json package-lock.json ./
RUN npm install && mkdir /react-frontend && mv ./node_modules ./react-frontend

WORKDIR /react-frontend
COPY . .

COPY nginx/prod.monitor-serv-frontend.env ./.env

RUN npm run build

##### STAGE 2 #####
FROM nginx:1.23.3-alpine

COPY --from=build /react-frontend/build /usr/share/nginx/html
RUN rm /etc/nginx/conf.d/default.conf
COPY nginx/prod.nginx.conf /etc/nginx/conf.d/nginx.conf
COPY nginx/gzip.conf /etc/nginx/conf.d/

WORKDIR /usr/share/nginx/html

EXPOSE 80

CMD ["nginx", "-g", "daemon off;"]
