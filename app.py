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
    print(data)
    
    

#     prediction = model.predict_proba([data['user_input']])
#     return jsonify({'probability': prediction[0][1]})

    # directions > in the template?
    # user scores five features 
    
    
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


#     data = request.json
#     print(data)
    
#     hour_24_text = data['user_input_hour']
#     print(hour_24_text, type(hour_24_text))
#     hour_24 = int(hour_24_text)
    
#     weekday_str = data['user_input_weekday']
#     weekday_int = day_str_to_int(weekday_str)
    
#     age_hours_text = data['user_input_age']
#     age_hours = int(age_hours_text)
#     age_mins = age_hours * 60
    
#     text = data['user_input_text']
    
#     arguments = (hour_24, weekday_int,
#                 age_mins, text)
#     arguments = pd.DataFrame(
#         [[text, age_mins, weekday_int, hour_24]],
#         columns=['text', 'age', 'weekday_posted', 'hour_posted'])


    
#     # prediction = model.predict_proba([data['user_input']])
    
#     predicted_score = np.exp(score_model.predict(arguments))[0]
#     predicted_comments = np.exp(comment_model.predict(arguments))[0]

#     rounded_predicted_score = round(predicted_score)
#     rounded_predicted_comments = round(predicted_comments)
    
    
#     return jsonify({'1. Score': rounded_predicted_score,
#                     '2. Number of Comments': rounded_predicted_comments})