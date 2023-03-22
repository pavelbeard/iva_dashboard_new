##### STAGE 1 #####
FROM node:18.15.0-alpine3.17 as build

COPY package.json package-lock.json ./
RUN npm install && mkdir /react-frontend && mv ./node_modules ./react-frontend

WORKDIR /react-frontend
COPY env/prod.monitor-serv-frontend.env ./.env
COPY . .

RUN npm run build; rm -rf ./env

##### STAGE 2 #####
FROM nginx:1.23.3-alpine

COPY --from=build /react-frontend/build /usr/share/nginx/html
RUN rm /etc/nginx/conf.d/default.conf
COPY nginx/test.nginx.conf /etc/nginx/conf.d/nginx.conf

EXPOSE 80

CMD ["nginx", "-g", "daemon off;"]
