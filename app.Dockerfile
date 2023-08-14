FROM docker.iranrepo.ir/python:3.11.4

WORKDIR /app

COPY . /app/

RUN pip install pipenv && pipenv install --system

EXPOSE 8000:8000

WORKDIR /app/src
