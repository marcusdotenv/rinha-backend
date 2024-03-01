import psycopg2
from dotenv import load_dotenv
import os


load_dotenv()

def connect_db():
    db_config = {
        'host': os.getenv("DATABASE_HOST"),
        'database': os.getenv("DATABASE_NAME"),
        'user': os.getenv("DATABASE_USER"),
        'password': os.getenv("DATABASE_PASSWD"),
        'port': os.getenv("DATABASE_PORT"),
    }
    try:
        conn = psycopg2.connect(**db_config)
        return conn

    except psycopg2.Error as e:
       raise Exception("Was not possible to connect to database")
