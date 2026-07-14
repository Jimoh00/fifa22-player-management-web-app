import csv
import sqlite3 

conn = sqlite3.connect('players.db')
cursor = conn.cursor()

cursor.execute("""
    CREATE TABLE IF NOT EXISTS players (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        short_name TEXT,
        player_positions TEXT,
        overall INTEGER,
        potential INTEGER,
        value_eur REAL,
        wage_eur REAL,
        age INTEGER,
        club_name TEXT,
        nationality_name TEXT,
        preferred_foot TEXT,
        height_cm REAL,
        weight_kg REAL,
        pace INTEGER,
        shooting INTEGER,
        passing INTEGER,
        dribbling INTEGER,
        defending INTEGER,
        physic INTEGER
    )
""")

conn.commit()


with open('players_22.csv', encoding='utf-8') as file:
    reader = csv.DictReader(file)
    for row in reader:
        cursor.execute("""
            INSERT INTO players (
                short_name, 
                player_positions, 
                overall, 
                potential,
                value_eur,
                wage_eur,
                age,
                club_name,
                nationality_name,
                preferred_foot,
                height_cm,
                weight_kg,
                pace,
                shooting,
                passing,
                dribbling,
                defending,
                physic
            ) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)
        """,(
            row['short_name'] ,
            row['player_positions'] ,
            row['overall'],
            row['potential'],
            row['value_eur'],
            row['wage_eur'],
            row['age'],
            row['club_name'],
            row['nationality_name'],
            row['preferred_foot'],
            row['height_cm'],
            row['weight_kg'],
            row['pace'],
            row['shooting'],
            row['passing'],
            row['dribbling'],
            row['defending'],
            row['physic']
        ))

conn.commit()
conn.close()
print("Done loading data")