import sqlite3
from sqlite3 import Error

def create_connection(db_file):
    conn = None
    try:
        conn = sqlite3.connect(db_file)
    except Error as e:
        print(f"Error: {e}")
        raise  # Raising the exception to propagate the error

    return conn




