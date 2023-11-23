import random as rd
import csv

def readcsv():
    file = open("/Users/djibril/Documents/DiscordBot/archive/male_players.csv", "r")
    m_players = list(csv.reader(file, delimiter=","))
    file.close()
    player = rd.choice(m_players)
    return player