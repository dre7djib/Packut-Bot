import sqlite3
from sqlite3 import Error

def createUser(conn,name, discordId):
    crix = 500
    sql = ''' INSERT INTO user (name, crix, discordId)
              VALUES (?, ?, ?) '''
    cur = conn.cursor()
    cur.execute(sql, (name, crix, discordId))
    conn.commit()
    return cur.lastrowid

def getUserId(conn,discordId):
    sql = ''' SELECT discordId FROM user WHERE discordId = ? '''
    cur = conn.cursor()
    cur.execute(sql, (discordId,))
    result = cur.fetchone()
    if result is None:
        return False
    else:
        return True

# Crix
def getCrix(conn,discordId):
    sql = ''' SELECT crix FROM user WHERE discordId = ? '''
    cur = conn.cursor()
    cur.execute(sql, (discordId,))
    result = cur.fetchone()
    return result[0]

def setCrix(conn,crix,discordId):
    sql = ''' UPDATE user SET crix = ? WHERE discordId = ? '''
    cur = conn.cursor()
    cur.execute(sql, (crix,discordId))
    result = cur.fetchone()
    return cur.lastrowid