from flask import Flask, request, render_template, jsonify, session
from flask_session import Session
import random
import pandas as pd
import json
import pickle
import numpy as np
from recommend import recommend_nn, get_random_recs, get_updated_n_recommendation

nn_model = pickle.load(open('models/nn_model.pkl', 'rb'))
cities = pickle.load(open('data/cities_with_topic_scores.pkl', 'rb'))
app = Flask(__name__, static_url_path="")
app.config['SESSION_TYPE'] = 'mongodb'
Session(app)
    
@app.route('/')
def index():
    """Return the main page."""
    return render_template('index.html')


@app.route('/scores', methods=['GET', 'POST'])
def score():
    data = request.json
    user_scores = store_data(data)
    session['user_scores'] = user_scores
    
    closest_50 = recommend_nn(nn_model, cities, user_scores)
    random_cities = get_random_recs(closest_50)
    session['random_cities'] = random_cities
    numbers = list(range(10))
    random_cities_dict = dict(zip(numbers, random_cities))

    print(random_cities_dict)
    return jsonify(random_cities_dict)


def store_data(data):
    scores = data.values()
    scores_as_float = [float(score) / 10 for score in scores]
    return np.array(scores_as_float).reshape(1, -1)


def get_random_cities(var):
    return session['random_cities']


def store_ratings(data):
    ratings = data.values()
    return [float(rating) for rating in ratings]

@app.route('/recommend', methods=['GET','POST'])
def recommend():
    data = request.json
    user_ratings = store_ratings(data)
    user_score = session.get('user_scores')
    random_recs = session.get('random_cities')
    visited = []
    for ind, rating in enumerate(user_ratings):
        if rating != 0:
            visited.append(random_recs[ind])
    closest = get_updated_n_recommendation(user_score, cities, random_recs,
                                  nn_model, user_ratings, visited)
    recommendations = {}
    for i, place in enumerate(closest[:5]):
        recommendations[i] = place[0]
    return jsonify(recommendations)
    