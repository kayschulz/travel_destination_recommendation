# European Travel Recommendation

## Business Understanding
I never traveled as a child, but I always wanted to. Now that I’m an adult and can pay for my own vacations, I want to travel, but I never know where to go. I would like to create an application that features a short interest quiz to give recommendations on where to travel based on the results of the quiz.

## Data Understanding
I have yet to find a resource that has a clear layout of descriptions of cities around the world. However, I have found ricksteves.com which only contains European cities, but each city has the same web structure. I would like to scrape ricksteves.com for short summaries on both country and city. I may also want to scrape some of the pictures and experiences, but this may be a stretch goal. 

## Data Preparation
I’m not sure how exactly to prepare the data yet, as I will largely be making my own dataset. I may use NLP for topic model

## Modeling
I'll set aside a final validation set of feature labeled cities, maybe 20%. I want to make a cold-start model of a recommendation system as I will not have user data. Since this data is not labeled, I will likely use a KNN model. 

## Evaluation
Since I will not have user data in the construction of the model, can’t objectively evaluate the model before deployment. I will however, ask users to rate their recommendations for subjectective evaluation of the recommender.

## Deployment
The model will be deployed using a Flask app. When the user goes to the website, they will click on pictures of scenery/activities that appeal to their travel needs. When the user is satisfied with their decisions they will press a button “Find my travel destination” that will reveal the five predicted locations based on their criteria. A retroactive question will be asked “If you have been to _blank_; did you like or dislike?”. Then a final five prediction will be given due to this additional feedback. The final prediction will also have a question for tracking evaluation: “thumbs up / thumbs down”. 

