from flask import Flask, request, render_template, jsonify, session
from flask_session import Session
import random
import pandas as pd
import json
import pickle
import numpy as np
from recommend import recommend_nn, get_random_recs

nn_model = pickle.load(open('models/nn_model.pkl', 'rb'))
cities = pickle.load(open('data/cities_with_topic_scores.pkl', 'rb'))
app = Flask(__name__, static_url_path="")
app.config['SESSION_TYPE'] = 'filesystem'
Session(app)
    
@app.route('/')
def index():
    """Return the main page."""
    return render_template('index.html')


@app.route('/scores', methods=['GET', 'POST'])
def score():
    data = request.json
    user_scores = store_data(data)
    
    closest_50 = recommend_nn(nn_model, cities, user_scores)
    random_cities = get_random_recs(closest_50)
    session['random_cities'] = random_cities
    test = session.get('random_cities')
    print(test)
    return ''
    #return new questions here


def store_data(data):
    scores = data.values()
    scores_as_float = [float(score) / 10 for score in scores]
    return np.array(scores_as_float).reshape(1, -1)


def get_random_cities(var):
    return session['random_cities']


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