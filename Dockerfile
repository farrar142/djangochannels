FROM python:3.10

WORKDIR /usr/src/app

COPY . .
RUN apt-get update && apt-get install pygraphviz -y
RUN pip3 install -r requirements.txt