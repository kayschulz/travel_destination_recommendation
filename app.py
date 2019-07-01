from flask import Flask, request, render_template, jsonify
import random
import pandas as pd
import json
import pickle
from recommend import 

nn_model = pickle.load(open('models/nn_model.pkl', 'rb'))
app = Flask(__name__, static_url_path="")
    
@app.route('/')
def index():
    """Return the main page."""
    return render_template('index.html')


@app.route()
def score_features():
    # directions > in the template?
    # user scores five features 
    
    
@app.route()
def score_random_cities():
    # will need directions in the page? > In the template?
    # shows ten random cities (different function?) with pictures
    # rating of the cities based on previous experience

@app.route()
def final_recommendations():
    # update the user score
    # show the top 5 recommended
    # this show should have pictures, short description, and link to ricksteves.com
    # quick thumbs up down on if you would want to go
