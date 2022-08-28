import psycopg2
import pandas as pd

#connect to postgresql cloud database
conn = psycopg2.connect(
    host="tiny.db.elephantsql.com",
    database="wvhwwxaj",
    user="wvhwwxaj",
    password="nuuVmVsPvLq8QxO4UJL7erelfFgLDoEe")

#connect cursor
cur = conn.cursor()

#create table
cur.execute("DROP TABLE IF EXISTS BoardGameGeek;")
cur.execute("""CREATE TABLE BoardGameGeek(
                id INTEGER,
                thumbnail VARCHAR(256),
                image VARCHAR(256),
                game VARCHAR(128),
                description VARCHAR(16384),
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

#read csv file from local computer
df = pd.read_csv('/Users/kyoh/Downloads/Section3/project3/board_games_info.csv')

#make meaningful dataframe with valualble columns from the whole dataset
df = df[["id","thumbnail","image","primary","description","yearpublished","minplayers","maxplayers","playingtime","minplaytime",
    "maxplaytime","minage","boardgamecategory","usersrated","average","bayesaverage","Board Game Rank","averageweight"]]

#only need 0-1000 most reviewed(famous) games
df = df[0:1000]

df_list_tuple = list(df.itertuples(index=False, name=None))
sql = """INSERT INTO BoardGameGeek (id, thumbnail, image, game, description, yearpublished, minplayers, maxplayers, playingtime, 
    minplaytime, maxplaytime, minage, boardgamecategory, usersrated, average, bayesaverage, rank, averageweight) 
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"""

#load dataset into the database(postgresql)
cur.executemany(sql, df_list_tuple)

conn.commit()#데이터베이스 안에 확정지어 적재

cur.close()
conn.close()