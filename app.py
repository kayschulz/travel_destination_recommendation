from flask import Flask, request, render_template, jsonify, session
from flask_session import Session
import random
import pandas as pd
import json
import pickle
import numpy as np
import pymongo
from recommend import recommend_nn, get_random_recs, get_city_scores

# connect to mongoDB Atlas
with open('.secrets/password.txt', 'r') as f:
    conn_string = f.read().strip()

mc = pymongo.MongoClient(conn_string)
city_db = mc['city_database']
user_coll = city_db['user_collection']
user_satisfaction = city_db['user_satisfaction']

# load necessary pickled files
nn_model = pickle.load(open('models/nn_model.pkl', 'rb'))
cities = pickle.load(open('data/cities_with_topic_scores.pkl', 'rb'))
app = Flask(__name__, static_url_path="")

# connect to flask session
app.config['SESSION_TYPE'] = 'mongodb'
Session(app)
    
@app.route('/')
def index():
    """Return the main page."""
    return render_template('theme.html')


@app.route('/scores', methods=['GET', 'POST'])
def score():
    """
    Returns a dictionary of 10 random cities from the 50 closest cities
    """
    data = request.json
    user_scores = store_data(data)
    
    # store user_score variable   
    session['user_scores'] = user_scores
    
    closest_50 = recommend_nn(nn_model, cities, user_scores)
    random_cities = get_random_recs(closest_50)
    
    # store random cities variable
    session['random_cities'] = random_cities
    
    # create dictionary for javascript
    numbers = list(range(10))
    random_cities_dict = dict(zip(numbers, random_cities))

    return jsonify(random_cities_dict)


def store_data(data):
    """
    Convert json data values to an array of floats
    """
    scores = data.values()
    scores_as_float = [float(score) / 10 for score in scores]
    return np.array(scores_as_float).reshape(1, -1)

def store_ratings(data):
    """
    Convert json data values to a list of ints
    """
    ratings = data.values()
    return [int(rating) for rating in ratings]


def update_user_scores(user_score, random_recs, user_ratings, cities):
    """
    Updates user score using user's city ratings
    """
    user_score = user_score.tolist()
    for ind, city in enumerate(random_recs):
        rating = user_ratings[ind]
        if rating != 0:
            city_score = get_city_scores(cities, city)
            if rating == -1:
                for i, score in enumerate(city_score):
                    score = -1 * score
                    city_score[i] = score
            user_score.extend(city_score)

    new_score = []
    for i in range(5):
        new_score.append(np.mean([item[i] for item in user_score]))

    return np.array(new_score).reshape(1, -1)


def update_recommendations(nn_model, cities, updated_scores, visited):
    updated_recs = recommend_nn(nn_model, cities, updated_scores)

    updated_city_recs = [rec[0] for rec in updated_recs]

    indices_to_remove = []
    for updated_city in updated_city_recs:
        if updated_city in visited:
            index = updated_city_recs.index(updated_city)
            indices_to_remove.append(index)

    for index in sorted(indices_to_remove, reverse=True):
        del updated_recs[index]
    
    return updated_recs[:5]
    
@app.route('/recommend', methods=['GET','POST'])
def recommend():
    """
    Updates user scores from city ratings. 
    Updates the recommendations for those new ratings. 
    Removes cities that have been visited.
    Add user ratings to mongodb atlas
    """
    data = request.json
    user_ratings = store_ratings(data)
    
    # get stored variables
    user_score = session.get('user_scores')
    random_recs = session.get('random_cities')
    
    # convert cities to strings
    random_recs = [str(rec) for rec in random_recs]
    
    # add to mongodb collection
    city_ratings = dict(zip(random_recs, user_ratings))
    user_coll.insert_one(city_ratings)
    
    # create a visited cities list
    visited = []
    for ind, rating in enumerate(user_ratings):
        if rating != 0:
            visited.append(random_recs[ind])

    updated_scores = update_user_scores(user_score, random_recs, user_ratings, cities)
    updated_recs = update_recommendations(nn_model, cities, updated_scores, visited)
    
    # to jsonify-able format
    recommendations = {}
    for i, place in enumerate(updated_recs):
        recommendations[i] = place[0]
   
    return jsonify(recommendations)


@app.route('/rate_recs', methods=['GET','POST'])
def rate_recs():
    data = request.json
    satisfaction = store_ratings(data)
    satisfaction_score = {'satisfaction_score': sum(satisfaction) / 5}
    user_satisfaction.insert_one(satisfaction_score)
    return ''
