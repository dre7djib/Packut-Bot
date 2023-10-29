import random as rd
import csv

def readcsv():
    file = open("/Users/djibril/Documents/DiscordBot/archive/male_players.csv", "r")
    m_players = list(csv.reader(file, delimiter=","))
    file.close()
    player = rd.choice(m_players)
    return player



# m_players.append(pd.read_csv(r"/Users/djibril/Documents/DiscordBot/archive/male_players.csv"))
# m_coachs = pd.read_csv(r"/Users/djibril/Documents/DiscordBot/archive/male_coaches.csv")
# f_players = pd.read_csv(r"/Users/djibril/Documents/DiscordBot/archive/female_players.csv")
# f_coachs = pd.read_csv(r"/Users/djibril/Documents/DiscordBot/archive/female_coaches.csv")
