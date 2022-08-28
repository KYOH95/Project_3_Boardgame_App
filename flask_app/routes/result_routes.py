from flask import Blueprint, render_template, request
import sys
sys.path.insert(0,'/Users/kyoh/Downloads/Section3/project3/flask_app/routes')
import main_routes

bp = Blueprint('result', __name__, url_prefix='/result')

@bp.route('/', methods=['POST','GET'])
def index():
    if request.method== "POST":
        
        return render_template('main.html')
    
    print(main_routes.X_test)
    
    return render_template('result.html')