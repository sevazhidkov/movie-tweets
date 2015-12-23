#!/usr/bin/env python
import os
import json
try:
    import requests
except ImportError:
    print(
        'Script requires requests package. \n'
        'You can install it by running "pip install requests"'
    )
    exit()

LOKLAK_API_URL = 'http://loklak.org/api/'
MYAPIFILMS_URL = 'http://api.myapifilms.com/'
MYAPIFILMS_TOKEN = os.environ['MYAPIFILMS_TOKEN']


def send_request(url):
    try:
        return requests.get(url)
    except requests.exceptions.RequestException as error:
        print('Error while sending request: ', error)
        exit()


def get_last_movies():
    response = requests.get(
        MYAPIFILMS_URL + 'imdb/inTheaters',
        params={'token': MYAPIFILMS_TOKEN, 'language': 'en-us', 'format': 'json'}
    )
    movies = json.loads(response.text)['data']['inTheaters'][1]['movies']
    movies_names = []
    for movie in movies:
        movies_names.append(movie['title'])
    return movies_names


def search_tweets(query):
    response = requests.get(
        LOKLAK_API_URL + 'search.json',
        params={'q': query}
    )
    print(response.text)
    tweets = json.loads(response.text)['statuses']
    tweets_texts = []
    for tweet in tweets:
        tweets_texts.append(tweet['text'])
    return tweets_texts

last_movies = get_last_movies()
print('Choose one of last movies and print it number.')
for i in range(len(last_movies)):
    print(i, last_movies[i])

movie_number = input('Movie number: ')
if not movie_number.isdigit():
    print('Movie number should be digit')
    exit()
movie_number = int(movie_number)
if not movie_number >= 0 or not movie_number <= len(last_movies):
    print('Choose correct number.')
    exit()

print('OK, loading tweets from Loklak about this movie')
tweets = search_tweets(last_movies[movie_number])
print('\n'.join(tweets))
