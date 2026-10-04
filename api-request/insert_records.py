import os

import psycopg2

try:  # charge le fichier .env quand le script tourne en local (hors Docker)
    from dotenv import load_dotenv
    load_dotenv(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".env"))
except ImportError:
    pass

from api_request import fetch_data, mock_fetch_data


def connect_to_db():
    print("Connecting to PostgreSQL database")
    try:
        conn = psycopg2.connect(
            host=os.getenv("DB_HOST", "localhost"),
            port=int(os.getenv("DB_PORT", "5000")),
            dbname=os.getenv("DB_NAME", os.getenv("POSTGRES_DB", "db")),
            user=os.getenv("DB_USER", os.getenv("POSTGRES_USER")),
            password=os.getenv("DB_PASSWORD", os.getenv("POSTGRES_PASSWORD")),
        )
        return conn
    except psycopg2.Error as e:
        print(f"Database connection failed: {e}")
        raise


def create_table(conn):
    print("Creating table if not exist ...")
    try:
        cursor = conn.cursor()
        cursor.execute("""
            CREATE SCHEMA IF NOT EXISTS dev;
            CREATE TABLE IF NOT EXISTS dev.raw_weather_data (
                id SERIAL PRIMARY KEY,
                city TEXT,
                temperature FLOAT,
                weather_description TEXT,
                wind_speed FLOAT,
                time TIMESTAMP,
                inserted_at TIMESTAMP DEFAULT NOW(),
                utc_offset TEXT
            );
            ALTER TABLE dev.raw_weather_data
                ADD COLUMN IF NOT EXISTS feelslike FLOAT,
                ADD COLUMN IF NOT EXISTS humidity FLOAT,
                ADD COLUMN IF NOT EXISTS pressure FLOAT;
        """)
        conn.commit()
        print("Table was created")
    except psycopg2.Error as e:
        print(f"Failed to create table: {e}")
        raise


def insert_records(conn, data):  # data is the api response
    print("Inserting weather data into the database ...")
    try:
        weather = data['current']
        location = data['location']
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO dev.raw_weather_data(
                city,
                temperature,
                weather_description,
                wind_speed,
                feelslike,
                humidity,
                pressure,
                time,
                inserted_at,
                utc_offset
            ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, NOW(), %s)
        """, (
            location['name'],
            weather['temperature'],
            weather['weather_descriptions'][0],
            weather['wind_speed'],
            weather['feelslike'],
            weather['humidity'],
            weather['pressure'],
            location['localtime'],
            location['utc_offset']
        ))
        conn.commit()
        print("Data successfully inserted")
    except psycopg2.Error as e:
        print(f"Error inserting data into the database: {e}")
        raise


def main():
    conn = None
    try:
        use_mock = os.getenv("USE_MOCK_DATA", "false").lower() == "true"
        data = mock_fetch_data() if use_mock else fetch_data()
        conn = connect_to_db()
        create_table(conn)
        insert_records(conn, data)
    except Exception as e:
        print(f"An error occurred during execution: {e}")
        raise  # l'erreur remonte pour que la tache Airflow soit marquee en echec
    finally:
        if conn is not None:
            conn.close()
            print("Database connection closed.")


if __name__ == "__main__":
    main()
