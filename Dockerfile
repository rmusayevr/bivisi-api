FROM python:3.10

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

COPY requirements.txt ./

RUN pip install --no-cache-dir -r requirements.txt --use-deprecated=legacy-resolver

COPY . .