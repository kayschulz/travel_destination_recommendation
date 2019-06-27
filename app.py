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

# show same pictures with rating system and collection
# collect initial user input ratings
# show 10 potential destinations and rating directions
# collect destination ratings
# show the top 5 recommended destinations