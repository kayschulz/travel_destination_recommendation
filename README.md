# European Travel Recommendation

## Business Understanding
I often find that I have the time, means, and desire to go on vaction, but unless I have family obligations, I have no clue where I to go. I have created an application that takes into account certain features (often setting features) that are of interest when taking a trip. Using this user input as well as some knowledge of the user's previous experience, the application will recommend the 5 European destinations that are most similar to their rating of the features.

## Data Understanding
I used Selenium to scrape text summaries ricksteves.com as well as Wikipedia. I additionally scraped photos from Rick Steves for use on the website. Please note that the XPath I used for images has changed since I completed scraping for the project. I stored these summaries in MongoDB collections.

## Data Preparation
I used both text summaries for a city to perform LDA topic modeling. To perform the LDA model, I had to add additional stop words so that I would not get topics such as "French" or "European". I utilized gensim to tokenize my text.
From LDA modeling I discovered 5 clear topics:
* Forest/Mountain
* Palaces/Castles
* Coastal/Water
* Historical
* Urban

Once I had the LDA model, I scored each summary by the probability it belonged to a topic. I then used the average of the Rick Steve and Wikipedia summary scores to give each city an aggregate score for each topic.

## Modeling
I created a cold start recommendation system that uses nearest neighbors with Euclidean distance to make recommendations. The model takes in user scores on the same five topics and gives back the 50 closest neighbors. Ten of these 50 are then randomly selected to collect information on user's previous experience. If one of these ten cities has been visited by the user, the initial topic ratings are adjusted by becoming more similar to visited cities they liked, and less similar to visited cities that they disliked. These previous experience ratings are also saved in MongoDB for future implementation of an ALS model. The updated ratings go back into the nearest neighbors model, a new 50 closest are generated, but only the top 5 are shown to the user. 

## Evaluation
Since I will not have user data in the construction of the model, can’t objectively evaluate the model before deployment. Therefore, when the 5 top destinations are shown, I ask the user if they would be interested in visiting the given destination. I can then subjectively see how well the model is performing.

## Deployment
The model will be deployed using a Flask app. The user first uses a slider bar to rate the setting options. When they select `Next` the ten random cities will be shown. The user then slides a bar to the left or right (been and disliked, been and liked respectively) or keeps it in the middle (have not been). The user then selects a button `Show Recommendations` which shows their recommendation. If the user clicks on the picture, a pop-up appears with the short Rick Steves summary and a link to the appropriate page on his website. This section also asks users for input on interest in their recommendations with a thumbs up thumbs down button. 

