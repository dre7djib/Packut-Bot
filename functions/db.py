import sqlite3
import os
from sqlite3 import Error

def create_connection(db_file):
    conn = None
    try:
        conn = sqlite3.connect(db_file)
    except Error as e:
        print(f"Error: {e}")
        raise  # Raising the exception to propagate the error

    return conn

def createDb():
    script_directory = os.path.dirname(os.path.abspath("/Users/djibril/Documents/DiscordBot/main.py"))
    database_path = os.path.join(script_directory, 'data.db')
    conn = sqlite3.connect(database_path)
    cur = conn.cursor()

    sql_players = '''CREATE TABLE IF NOT EXISTS players ( Id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT, playerID VARCHAR(50), playerName VARCHAR(50), valueCrix DECIMAL(2, 10), position VARCHAR(50), photoLink VARCHAR(255), userId INTEGER) '''
    sql_playersView = ''' CREATE TABLE IF NOT EXISTS playersView ( player_id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT, player_url TEXT, fifa_version TEXT, fifa_update TEXT, update_as_of TEXT,short_name TEXT,long_name TEXT,player_positions TEXT,overall INTEGER,potential INTEGER,value_eur INTEGER,wage_eur INTEGER,age INTEGER,dob TEXT,height_cm INTEGER,weight_kg INTEGER,club_team_id INTEGER,club_name TEXT)'''
    sql_user = '''CREATE TABLE IF NOT EXISTS user (userId INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,name VARCHAR(255),crix DECIMAL(2, 10),discordId VARCHAR(255))'''

    # Players
    cur.execute(sql_players)
    # PlayersView
    cur.execute(sql_playersView)
    # User
    cur.execute(sql_user)

    conn.commit()
    conn.close()


