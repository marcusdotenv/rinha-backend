import psycopg2
from dotenv import load_dotenv
import os
from psycopg2 import pool


load_dotenv()

db_config = {
        'host': os.getenv("DATABASE_HOST"),
        'database': os.getenv("DATABASE_NAME"),
        'user': os.getenv("DATABASE_USER"),
        'password': os.getenv("DATABASE_PASSWD"),
        'port': os.getenv("DATABASE_PORT"),
}

connection_pool = pool.SimpleConnectionPool(
    minconn=1,  
    maxconn=100, 
    **db_config
)

def get_connection():
    return connection_pool.getconn()

def release_connection(conn):
    connection_pool.putconn(conn)
