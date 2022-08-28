import psycopg2

conn = psycopg2.connect(
    host="tiny.db.elephantsql.com",
    database="wvhwwxaj",
    user="wvhwwxaj",
    password="nuuVmVsPvLq8QxO4UJL7erelfFgLDoEe")

cur = conn.cursor()

cur.execute("DROP TABLE IF EXISTS BoardGameGeek;")
cur.execute("""CREATE TABLE BoardGameGeek(
                id INTEGER,
                thumbnail VARCHAR(256),
                image VARCHAR(256),
                game VARCHAR(128),
                yearpublished INTEGER,
                minplayers INTEGER,
                maxplayers INTEGER,
                playingtime INTEGER,
                minplaytime INTEGER,
                maxplaytime INTEGER,
                minage INTEGER,
                boardgamecategory VARCHAR(256),
                usersrated INTEGER,
                average FLOAT,
                bayesaverage FLOAT,
                rank INTEGER,
                averageweight FLOAT
                )
			""")

import pandas as pd

df = pd.read_csv('/Users/kyoh/Downloads/Section3/project3/board_games_info.csv')

df = df[["id","thumbnail","image","primary","yearpublished","minplayers","maxplayers","playingtime","minplaytime",
    "maxplaytime","minage","boardgamecategory","usersrated","average","bayesaverage","Board Game Rank","averageweight"]]

df = df[0:1000]
df_list_tuple = list(df.itertuples(index=False, name=None))
sql = """INSERT INTO BoardGameGeek (id, thumbnail, image, game, yearpublished, minplayers, maxplayers, playingtime, 
    minplaytime, maxplaytime, minage, boardgamecategory, usersrated, average, bayesaverage, rank, averageweight) 
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"""
cur.executemany(sql, df_list_tuple)

conn.commit()

cur.close()
conn.close()