# warnings.filterwarnings('ignore')
import pandas as pd
import psycopg2
import numpy as np
# import seaborn as sns
import warnings
import random
import pickle
import postgresql_info
pd.options.display.float_format = '{:.3f}'.format

conn = psycopg2.connect(
    host=postgresql_info.host,
    database=postgresql_info.database,
    user=postgresql_info.user,
    password=postgresql_info.password)

cur = conn.cursor()

sql = "SELECT * FROM boardgamegeek"
cur.execute(sql)
data = cur.fetchall()

cur.close()
conn.close()

#save data into "df_origin" as dataframe
df_origin = pd.DataFrame(data, columns=["id","thumbnail","image","game","description","yearpublished","minplayers","maxplayers","playingtime","minplaytime",
    "maxplaytime","minage","boardgamecategory","usersrated","average","bayesaverage","rank","averageweight"])

#copy for the modeling dataset
df = df_origin.copy()

#delete column"index, id, thumbnail, image, description, playingtime, usersrated, average, bayesaverage, rank, "
df = df.drop(["id", "thumbnail", "image", "description","playingtime", "usersrated", "average", "bayesaverage", "rank"], axis = 1)

#build new column 'category' for machine learning
df["category"] = None
for i in range(0,len(df)):
  temp_list = df["boardgamecategory"][i].strip("[ ]").replace("'","").split(", ")
  df["category"][i] = temp_list[random.randint(0,len(temp_list)-1)]

#delete useless column
df = df.drop(["boardgamecategory"], axis = 1)

#seperate data into two parts: target or nontarget
X = df.drop(columns="game")
y = df["game"]

#build the pipeline using transform the dataset for the future modeling
from sklearn.pipeline import make_pipeline
from category_encoders import OrdinalEncoder
from sklearn.impute import SimpleImputer
from sklearn.ensemble import RandomForestClassifier

pipe = make_pipeline(
    OrdinalEncoder(handle_missing="value"), 
    SimpleImputer(), 
    RandomForestClassifier()
)

#fit the model
pipe.fit(X, y)

# #test the model
# X_test = {'yearpublished': [2000],
#           'minplayers': [4],
#           'maxplayers': [8],
#           'minplaytime': [60],
#           'maxplaytime': [120],
#           'minage': [12],
#           'averageweight' : [2.0],
#           'category' : ["Card Game"]
#           }
# X_test = pd.DataFrame(X_test)
# y_pred = pipe.predict(X_test)
# print("오늘의 보드게임은",list(y_pred)[0])


#pickling
with open('model.pkl','wb') as pickle_file:
    pickle.dump(pipe, pickle_file)

