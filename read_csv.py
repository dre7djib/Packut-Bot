import random as rd
import csv

def insertCSV(conn, file):
    with open(file, 'r', encoding='utf-8') as csv_file:
        csv_reader = csv.reader(csv_file)
        next(csv_reader)  # Skip header row
        cursor = conn.cursor()

        for row in csv_reader:
            # Remplacez les valeurs vides par None
            row = [value if value != '' else None for value in row]

            # Limitez la ligne aux 19 premières colonnes
            row = row[:18]

            # Vérifiez si la ligne a le bon nombre de valeurs
            if len(row) == 18:
                cursor.execute('''
                    INSERT OR IGNORE INTO playersView VALUES (
                        ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?
                    )
                ''', row)

    conn.commit()

def readcsv(m_players):
    player = rd.choice(m_players)
    return player