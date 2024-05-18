FROM python:alpine3.11

RUN pip install --upgrade pip

COPY requirements.txt ./requirements.txt
RUN pip install -r requirements.txt

WORKDIR /app

COPY . .
