# database/connection.py
import mysql.connector
from config import DB_CONFIG

def create_db_connection():
    connection = None
    try:
        connection = mysql.connector.connect(
            host=DB_CONFIG['host'],
            user=DB_CONFIG['user'],
            password=DB_CONFIG['password'],
            database=DB_CONFIG['database'],
            port=DB_CONFIG['port']
        )
        print("MySQL Database connection successful")
    except Exception as e:
        print(f"An error occurred while connecting to the database: {e}")
    return connection
