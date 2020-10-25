FROM node:14

WORKDIR /usr/src/app

COPY server/package*.json ./

RUN npm install

COPY ./server .

EXPOSE 8080

CMD dockerize -wait tcp://database:3306 -timeout 200m