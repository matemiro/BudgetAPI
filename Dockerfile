# base image
FROM python:3.10-alpine

#maintainer
LABEL Author="matemiro"

# The enviroment variable ensures that the python output is set straight
# to the terminal with out buffering it first
ENV PYTHONUNBUFFERED 1

RUN apk update && \
    apk add --virtual build-deps gcc python3-dev musl-dev && \
    apk add postgresql-dev

#directory to store app source code
RUN mkdir /app

#switch to /app directory so that everything runs from here
WORKDIR /app

#copy the app code to image working directory
COPY . /app

#let pip install required packages
RUN pip install -r requirements.txt

# Install pre-commit tool
RUN pip install pre-commit