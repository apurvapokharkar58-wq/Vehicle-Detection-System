
import os
import psycopg2
from dotenv import load_dotenv

load_dotenv()


def get_connection():
    return psycopg2.connect(
        host=os.getenv("DB_HOST"),
        port=os.getenv("DB_PORT"),
        database=os.getenv("DB_NAME"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD")
    )


def insert_vehicle_event(
    vehicle_id,
    vehicle_type,
    timestamp,
    direction,
    color="Unknown"
):
    connection = get_connection()

    try:
        cursor = connection.cursor()

        cursor.execute(
            """
            INSERT INTO vehicle_events
            (vehicle_id, vehicle_type, color, event_timestamp, direction)
            VALUES (%s, %s, %s, %s::timestamp, %s)
            """,
            (vehicle_id, vehicle_type, color, timestamp, direction)
        )

        connection.commit()
        cursor.close()

    finally:
        connection.close()
