# syntax=docker/dockerfile:1
ARG APP_IMAGE=python:3.8

FROM $APP_IMAGE

RUN echo $HOST
WORKDIR /python-docker

COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

COPY . .

ENTRYPOINT ["python", "-m", "flask", "run", "--host=0.0.0.0","--port=5000"]