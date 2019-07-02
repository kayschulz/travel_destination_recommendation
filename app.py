from flask import Flask, request, render_template, jsonify
import random
import pandas as pd
import json
import pickle
from recommend import *

nn_model = pickle.load(open('models/nn_model.pkl', 'rb'))
app = Flask(__name__, static_url_path="")
    
@app.route('/')
def index():
    """Return the main page."""
    return render_template('index.html')


@app.route('/predict', methods=['GET', 'POST'])
def predict():
    data = request.json
    stored = store_data(data)
    print(stored)
    return jsonify(data)
    #return new questions here


def store_data(data):
    scores = data.values()
    scores_as_float = [float(score) / 10 for score in scores]
#     forest_text = data['user_input_forest']
#     forest_score = float(forest_text) / 10
    
#     castle_text = data['user_input_castle']
#     castle_score = float(castle_text) / 10  
    
#     water_text = data['user_input_water']
#     water_score = float(water_text) / 10  
    
#     historical_text = data['user_input_historical']
#     historical_score = float(historical_text) / 10  
    
#     urban_text = data['user_input_urban']
#     urban_score = float(urban_text) / 10 
    
    return scores_as_float


#jsonify(action="populate",)
    
    
# @app.route()
# def score_random_cities():
#     # will need directions in the page? > In the template?
#     # shows ten random cities (different function?) with pictures
#     # rating of the cities based on previous experience

# @app.route()
# def final_recommendations():
#     # update the user score
#     # show the top 5 recommended
#     # this show should have pictures, short description, and link to ricksteves.com
#     # quick thumbs up down on if you would want to go