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
    pass    
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
    
#     return jsonify({'score': str(urban_score)})


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


# @app.route("/recommendations/")
# def show_predictions():
#     """ Returns personalized recommendation page to the user """
#     likes = request.args.getlist("like")
#     dismissed = request.args.getlist("dismissed")
#     search_cards = request.args.getlist("card")
#     try:
#         indices = [int(like) for like in likes]
#         ratings = [5 for podcast in range(len(indices))]
#         dismissed = [int(dnl) for dnl in dismissed]
#         if len(search_cards) == 0:
#             predictions = model.fit_predict(ratings, indices, dismissed)
#         else:
#             predictions = [int(search_card) for search_card in search_cards]
#         cards = get_cards(predictions)
#         id_dict = {"liked":indices, "recommended":[card["sid"] for card in cards]}
#         return render_template("recommendations.html", cards=cards, ids=id_dict)
#     except:
#         return render_template("sorry.html")


# import pandas as pd
# import podrex_db_utils as db
# import pickle
# from random import shuffle
# from flask import Flask, render_template, request, jsonify, g
# from model import PodcastRecommender, bonuses, pairwise_dist_2d
# from graph import d3Graph



# def get_db():
#     """ Returns a connection to the podrex db that can be cleanly closed by
#     flask """
#     conn = getattr(g, '_database', None)
#     if conn is None:
#         conn = g._database = db.connect_db()
#     return conn

# def get_cards(indices):
#     """
#     Returns jsonified cards ready to send to browser
#     Parameters:
#     indices (list of ints): podcast integers corresponding to spark_pid column
#     """
#     conn = get_db()
#     recommendation_data = db.get_podcast_info(conn, indices)
#     #artid, title, sid, description, itunes, stitcher, podcast website
#     cards = [{"art_id":result[0], "title":result[1], "sid":result[2],
#               "description":result[3], "itunes_url":result[4],
#               "stitcher_url":result[5], "podcast_url":result[6]}
#              for result in recommendation_data]
#     return cards

# @app.route("/dd-update/", methods=["POST"])
# def dropdown_update():
#     """ Returns data to update the dropdown card """
#     user_input = request.json
#     podcasts = []
#     try:
#         conn = get_db()
#         podcasts.append(int(user_input["podcast"]))
#         podcast_info = db.get_podcast_info(conn, podcasts)[0]
#         podcast_json = jsonify(action="populate",
#                                podcast_art_id=podcast_info[0],
#                                podcast_name=podcast_info[1],
#                                podcast_description=podcast_info[3])
#         return podcast_json
#     except ValueError:
#         podcast_json = jsonify(action="destroy",
#                                podcast_art_id="",
#                                podcast_name="",
#                                podcast_description="")
#         return podcast_json

# @app.route("/predictions/", methods=["POST"])
# def predict():
#     """
#     Gets predictions from the model and returns html
#     page and podcasts to render
#     """
#     user_inputs = request.json
#     favorites = user_inputs["favorites"]
#     thumbs = user_inputs["thumbs"]
#     if len(favorites) == 0 and len(thumbs) == 0:
#         return "empty"
#     dismissed = user_inputs["dismissed"]
#     ratings, indices = [], []
#     for k, v in thumbs.items():
#         if v > 0:
#             indices.append(int(k))
#             ratings.append(int(v))
#     for k, v in favorites.items():
#         if k != "":
#             try:
#                 pop_index = indices.index(int(k))
#                 indices.pop(pop_index)
#                 ratings.pop(pop_index)
#             except ValueError:
#                 indices.append(int(k))
#                 ratings.append(5)
#     dismissed = list({int(i) for i in dismissed})
#     if len(dismissed) <= 0:
#         dismissed = None
#     predictions = model.fit_predict(ratings, indices, dismissed)
#     return jsonify(get_cards(predictions))

# @app.route("/recommendations/")
# def show_predictions():
#     """ Returns personalized recommendation page to the user """
#     likes = request.args.getlist("like")
#     dismissed = request.args.getlist("dismissed")
#     search_cards = request.args.getlist("card")
#     try:
#         indices = [int(like) for like in likes]
#         ratings = [5 for podcast in range(len(indices))]
#         dismissed = [int(dnl) for dnl in dismissed]
#         if len(search_cards) == 0:
#             predictions = model.fit_predict(ratings, indices, dismissed)
#         else:
#             predictions = [int(search_card) for search_card in search_cards]
#         cards = get_cards(predictions)
#         id_dict = {"liked":indices, "recommended":[card["sid"] for card in cards]}
#         return render_template("recommendations.html", cards=cards, ids=id_dict)
#     except:
#         return render_template("sorry.html")