import json
import os
from datetime import datetime

import psycopg2
import redis
from psycopg2 import Error

PG_USER = os.environ.get("PG_USER", "postgres")
PG_PASSWORD = os.environ.get("PG_PASSWORD", "postgres")
PG_HOST = os.environ.get("PG_HOST", "127.0.0.1")
PG_PORT = int(os.environ.get("PG_PORT", 54321))
PG_NAME = os.environ.get("PG_NAME", "ecommerce_docker")

REDIS_HOST = os.getenv("REDIS_HOST", "127.0.0.1")
REDIS_PORT = int(os.getenv("REDIS_PORT", 6379))

try:
    connection = psycopg2.connect(
        user=PG_USER, password=PG_PASSWORD, host=PG_HOST, port=PG_PORT, database=PG_NAME
    )

    cursor = connection.cursor()

    create_table_query = """CREATE TABLE IF NOT EXISTS clickstream (
                                id SERIAL PRIMARY KEY,
                                user_id INT NOT NULL,
                                page_title VARCHAR(255),
                                page_url VARCHAR(450),
                                timestamp TIMESTAMP(0),
                                event_type VARCHAR(20)
                            );"""

    cursor.execute(create_table_query)
    connection.commit()
    print("Table created successfully in PostgreSQL")

    insert_query = """INSERT INTO clickstream (user_id, page_title, page_url, timestamp, event_type)
                      VALUES (%s, %s, %s, %s, %s);"""

    r = redis.Redis(host=REDIS_HOST, port=REDIS_PORT)
    while True:
        data = r.blpop("clickstream_queue")
        data_json = json.loads(data[1])
        record_to_insert = (
            data_json["user_id"],
            data_json["page_title"],
            data_json["page_url"],
            data_json["timestamp"],
            data_json["event_type"],
        )
        cursor.execute(insert_query, record_to_insert)
        connection.commit()
        print(
            "{} - Inserted record into database".format(
                datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            )
        )


except (Exception, Error) as error:
    print("Error while connecting to PostgreSQL", error)
finally:
    if connection:
        cursor.close()
        connection.close()
        print("PostgreSQL connection is closed")
