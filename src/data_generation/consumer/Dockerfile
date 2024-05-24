FROM python:3.12-alpine

LABEL maintainer="Alireza Hanifi"

WORKDIR /src

ENV PG_USER=postgres
ENV PG_PASSWORD=postgres
ENV PG_HOST=postgres_alpine
ENV PG_PORT=5432
ENV PG_NAME=ecommerce_docker
ENV REDIS_HOST=redis
ENV REDIS_PORT=6379

COPY requirements.txt .

RUN pip install --upgrade pip && \
    pip install -r requirements.txt

COPY . .

CMD ["python3", "consumer_app.py"]