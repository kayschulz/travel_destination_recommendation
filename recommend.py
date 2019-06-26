from sklearn.neighbors import NearestNeighbors
import pickle
import pandas as pd
import numpy as np


def recommend_nn(nn_model, city_df, user_input=[0, 0, 0, 0, 0]):
    """
    Gives the nearest neighbors from user rating on five topics.
    The number of neighbors is determined prior to this function
    during the instantiation of the nn_model.
    """
    user_scores = np.array(user_input).reshape(1, -1)
    distances, closest_five = nn_model.kneighbors(user_scores)

    destinations = []
    for index in closest_five[0]:
        destination = (city_df.iloc[index]['city'], 
                       city_df.iloc[index]['country'])
        destinations.append(destination)
    distances = [distance for distance in distances[0]]
    return list(zip(destinations, distances))


def get_random_recs(closest_50, n=5):
    """Generates n random recommendations from
       top 50 recommended destinations"""
    return np.random.choice(np.array(closest_50)[:, 0], n, replace=False)


def get_city_scores(cities_with_scores, city):
    topics = ['forest_mountain', 'palaces','island_water',
              'historical_ww2','urban']
    city_score = cities_with_scores.loc[cities_with_scores['city'] == city, 
                                        topics].values.tolist()
    return city_score


def update_user_score(user_score, cities_with_scores, 
                      random_recs, city_rating=[0, 0, 0, 0, 0]):
    """
    Finds the new user score by averging the original user input with a
    positive or negative score if the user liked (1) or disliked (-1) a
    city. If the user has not been to the city, it is not included in
    the average calculation.
    """
    user_score = [user_score]
    for ind, city in enumerate(random_recs):
        if city_rating[ind] == 1:
            city_score = get_city_scores(cities_with_scores, city[0])
            user_score.extend(city_score)
        elif city_rating[ind] == -1:
            city_score = get_city_scores(cities_with_scores, city[0])
            city_score_neg = [i * -1 for i in city_score]
            user_score.extend(city_score)
    new_score = []
    for i in range(5):
        new_score.append(np.mean([item[i] for item in user_score]))

    return new_score


def get_updated_n_recommendation(user_score, cities_with_scores, random_recs,
                                 nearest_neighbor, city, n=5,
                                 city_rating=[0, 0, 0, 0, 0]):
    """
    Give the top n recommended desitinations by distance with updated
    user score.Also remove destinations already known to have visited
    """
    updated_user_score = update_user_score(user_score, cities_with_scores,
                                           random_recs, city_rating)
    updated_recs = recommend_nn(nearest_neighbor, city, updated_user_score)

    updated_city_recs = [rec[0][0] for rec in updated_recs]
    random_city_recs = [rec[0] for rec in random_recs]

    random_rec_rating = dict(zip(random_city_recs, city_rating))

    indices_to_remove = []
    for key, val in random_rec_rating.items():
        if (key in updated_city_recs) & (val != 0):
            index = updated_city_recs.index(key)
            indices_to_remove.append(index)

    for index in sorted(indices_to_remove, reverse=True):
        del updated_recs[index]

    return updated_recs[0:n]
