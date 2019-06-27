from sklearn.neighbors import NearestNeighbors
import pickle
import pandas as pd
import numpy as np
import pymongo

mc = pymongo.MongoClient()
city_db = mc['city_database']
user_coll = city_db['user_collection']


def get_initial_user_score():
    """Collect initial user score"""
    print('Rate on a scale of 0-10. 0 meaning not important and 10 meaning very important')
    user_scores = []
    user_scores.append(int(input(f"How important is a forest/mountain setting: ")) / 10)
    user_scores.append(int(input(f"How important is visiting palaces/castles: ")) / 10)
    user_scores.append(int(input(f"How important is a costal/water setting: ")) / 10)
    user_scores.append(int(input(f"How important is historical sites: ")) / 10)
    user_scores.append(int(input(f"How important is an urban setting: ")) / 10)
    print('\n')
    return user_scores
    

def recommend_nn(nn_model, cities, user_scores):
    """
    Gives the nearest neighbors from user rating on five topics.
    The number of neighbors is determined prior to this function
    during the instantiation of the nn_model.
    """
    user_scores = np.array(user_scores).reshape(1, -1)
    distances, closest_fifty = nn_model.kneighbors(user_scores)

    destinations = []
    for index in closest_fifty[0]:
        destination = (cities.iloc[index]['city'], 
                       cities.iloc[index]['country'])
        destinations.append(destination)
    distances = [distance for distance in distances[0]]
    return list(zip(destinations, distances))


def get_random_recs(closest_50, n=10):
    """Generates n random recommendations from
       top 50 recommended destinations"""
    return np.random.choice(np.array(closest_50)[:, 0], n, replace=False)


def get_city_scores(cities_df, city):
    topics = ['forest_mountain', 'palaces','island_water',
              'historical_ww2','urban']
    city_score = cities_df.loc[cities_df['city'] == city, topics].values.tolist()
    return city_score


def update_user_score(user_score, cities, random_recs, city_rating):
    """
    Finds the new user score by averging the original user input with a
    positive or negative score if the user liked (1) or disliked (-1) a
    city. If the user has not been to the city, it is not included in
    the average calculation.
    """
    user_score = [user_score]
    for ind, city in enumerate(random_recs):
        rating = int(city_rating[ind])
        if rating != 0:
            city_score = get_city_scores(cities, city[0])
            if rating == -1:
                for i, score in enumerate(city_score[0]):
                    score = -1 * score
                    city_score[0][i] = score
            user_score.extend(city_score)
    
    new_score = []
    for i in range(5):
        new_score.append(np.mean([item[i] for item in user_score]))

    return new_score


def get_updated_n_recommendation(user_score, cities, random_recs,
                                 nn_model, ratings, visited_cities):
    """
    Give the n top recommended desitinations by distance with updated
    user score.Also remove destinations already known to have visited
    """
    user_score = update_user_score(user_score, cities, random_recs, ratings)
    updated_recs = recommend_nn(nn_model, cities, user_score)

    updated_city_recs = [rec[0] for rec in updated_recs]
    
    indices_to_remove = []
    for updated_city in updated_city_recs:
        if updated_city in visited_cities:
            index = updated_city_recs.index(updated_city)
            indices_to_remove.append(index)

    for index in sorted(indices_to_remove, reverse=True):
        del updated_recs[index]

    return updated_recs


def get_user_city_ratings(nn_model, cities, user_score, city_ratings, ignore, visited):
    """
    Asks user to rate 10 random cities. 
    User Input Meanings:
        1 - visited and liked
        -1 - visited and disliked
        0 - has not visited
    """
    closest = recommend_nn(nn_model, cities, user_score)
    user_dict = {}
    while sum([abs(rating) for rating in city_ratings]) > 5:
        random_recs = get_random_recs(closest)
        for i, rec in enumerate(random_recs):
            if rec not in ignore:
                rating = int(input(f"Rate {random_recs[i]}: "))
                city_ratings[i] = rating
                user_dict[str(rec)] = rating
                if rating != 0:
                    visited.append(rec)
        ignore.extend(random_recs)
        print('\n')
        # new closest
        closest = get_updated_n_recommendation(user_score, cities, random_recs, nn_model, city_ratings, visited)
    
    user_coll.insert_one(user_dict)
    
    return closest
        
        
def make_recommendations(cities_df, nn_model, ignore_cities=[],visited_cities=[], city_ratings = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1]):
    """
    Finds the five most recommended cities determined by user input and previously visited cities
    """
    user_score = get_initial_user_score() 
    closest_50 = get_user_city_ratings(nn_model, cities_df, user_score,
                                       city_ratings, ignore_cities, visited_cities)
    return closest_50[0:5]
