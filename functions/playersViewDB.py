import sqlite3
from sqlite3 import Error

def getPlayersByName(conn, playerName):
    sql_query = ''' SELECT * FROM playersView WHERE short_name = ? '''
    cur = conn.cursor()
    cur.execute(sql_query,(playerName,))
    results = cur.fetchall()
    converted_results = [list(result) for result in results]

    return converted_results
