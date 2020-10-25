FROM node:14

WORKDIR /usr/src/app

COPY view/package*.json ./

RUN npm install

COPY ./view .

EXPOSE 3000
