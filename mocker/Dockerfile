FROM node:14

WORKDIR /usr/src/app

COPY package*.json ./

RUN npm install

COPY . .

CMD dockerize -wait tcp://database:3306 -timeout 100m