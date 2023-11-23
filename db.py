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

def create_user(conn,name, discordId):
    crix = 500
    sql = ''' INSERT INTO user({name},{crix},{discordId})
              VALUES(?,?,?) '''
    cur = conn.cursor()
    cur.execute(sql, project)
    conn.commit()
    return cur.lastrowid

def getUserID(conn,discordId):
    sql = ''' SELECT discordId FROM user WHERE discordId == {discordID} '''
    cur = conn.cursor()
    cur.execute(sql, project)
    conn.commit()
    if cur.lastrowid is None:
        return False
    else: 
        return True


db = create_connection("data.db")