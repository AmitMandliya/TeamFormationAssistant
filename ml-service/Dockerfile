FROM python:3.8

WORKDIR /usr/src/app

COPY ./ml-server ./

RUN ["pip", "install", "--upgrade", "pip"]

RUN ["pip", "install", "-r", "requirements.txt"]



