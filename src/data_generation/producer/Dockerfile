FROM python:3.12-alpine

LABEL maintainer="Alireza Hanifi"

WORKDIR /src

ENV REDIS_HOST=redis
ENV REDIS_PORT=6379

COPY requirements.txt .

RUN pip install --upgrade pip && \
    pip install -r requirements.txt

COPY . .

CMD ["python3", "producer_app.py"]