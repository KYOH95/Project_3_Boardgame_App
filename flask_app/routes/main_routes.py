from numpy import RankWarning
import pandas as pd
from flask import Blueprint, render_template, request
import psycopg2
import postgresql_info

bp = Blueprint('main', __name__, url_prefix='/main')

#main page
@bp.route('/', methods=['POST','GET'])
def index():
    data = get_dataset()
    if request.method== "POST":
        X_test = {'yearpublished': [int(request.form["yearpublished"])],
            'minplayers': [int(request.form["minplayers"])],
            'maxplayers': [int(request.form["maxplayers"])],
            'minplaytime': [int(request.form["minplaytime"])],
            'maxplaytime': [int(request.form["maxplaytime"])],
            'minage': [int(request.form["minage"])],
            'averageweight' : [int(request.form["averageweight"])],
            'category' : [request.form["category"]]
            }
        
        y_game = get_result(X_test)
        y_image, y_description, y_yearpublished, y_minplayers, y_maxplayers, y_playingtime, y_minage, y_boardgamecategory, y_usersrated, y_average, y_rank, y_averageweight = get_info(data,y_game)

        return render_template('result.html', result_game=y_game, result_image=y_image, result_description=y_description, result_yearpublished=y_yearpublished, result_minplayers=y_minplayers, result_maxplayers=y_maxplayers, result_playingtime=y_playingtime, result_minage=y_minage, result_boardgamecategory=y_boardgamecategory, result_usersrated=y_usersrated, result_average=y_average, result_rank=y_rank, result_averageweight=y_averageweight)
    return render_template('main.html')

#get dataset from the database
def get_dataset():
    conn = psycopg2.connect(
        host=postgresql_info.host,
        database=postgresql_info.database,
        user=postgresql_info.user,
        password=postgresql_info.password)

    cur = conn.cursor()
    cur.execute("SELECT * FROM boardgamegeek")
    data = cur.fetchall()
    cur.close()
    conn.close()
    
    return data
    
#get result(game) from the model
def get_result(X):
    import pickle
    model = None
    X = pd.DataFrame(X)
    with open('model.pkl','rb') as pickle_file:
        model = pickle.load(pickle_file)

    return list(model.predict(X))[0]
    
#get information of the game
def get_info(data,game):
    for i in range(len(data)):
        if data[i][3] == game:
            image = data[i][2]
            description = data[i][4]
            yearpublished = data[i][5]
            minplayers = data[i][6]
            maxplayers = data[i][7]
            playingtime = data[i][8]
            minage = data[i][11]
            usersrated = data[i][13]
            average = round(data[i][14],2)
            rank = data[i][16]
            averageweight = round(data[i][17],2)
            # boardgamecategory = data[i][12]
            boardgamecategory = data[i][12].replace("[","").replace("]","").replace(","," /").replace("'","").replace('"','')
        
    return image, description, yearpublished, minplayers, maxplayers, playingtime, minage, boardgamecategory, usersrated, average, rank, averageweight
    


    
