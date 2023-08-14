FROM docker.iranrepo.ir/python:3.11.4
COPY src/ Pipfile Pipfile.lock /app/
WORKDIR /app
RUN apt-get update
RUN pip install pipenv && pipenv install --system --deploy
WORKDIR /app/src
