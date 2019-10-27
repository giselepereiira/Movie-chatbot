import json
import operator
import pickle

import nltk
import pandas as pd
from flask import Flask, request, Response

from InvertedIndexUtils import ranked_retrieval

nltk.download('vader_lexicon')
from nltk.sentiment.vader import SentimentIntensityAnalyzer

sid = SentimentIntensityAnalyzer()


app = Flask(__name__)
LEN_MOVIES_DATASET = 12500
NUMBER_MOVIES_RETURN = 3


@app.route("/level3", methods=['GET'])
def get_level_3():
    time = request.args.get('time')
    movie_characteristics = request.args.get('movie_characteristic')

    sentiment_scores = sid.polarity_scores(movie_characteristics)

    if sentiment_scores['neg'] > sentiment_scores['pos'] and sentiment_scores['neg'] > sentiment_scores['neu']:
        print('negative feeling')

    if sentiment_scores['pos'] > sentiment_scores['neg'] and sentiment_scores['pos'] > sentiment_scores['neu']:
        print('positive feeling')

    if sentiment_scores['neu'] > sentiment_scores['neg'] and sentiment_scores['neu'] > sentiment_scores['pos']:
        print('neutral feeling')

    # TODO: add this sentiment ?

    scores = ranked_retrieval(inverted_index, LEN_MOVIES_DATASET, movie_characteristics)
    doc_scores = sorted(scores.items(), key=operator.itemgetter(1), reverse=True)

    result = pd.DataFrame()

    # TODO: get movie title from id

    # for value in doc_scores:
    #   id = str(value[0])
    #  movie_info = movie_data.loc[(movie_data['movie_id'] == int(id)) & (movie_data['date'] == str(time))]
    # if not movie_info.empty:
    # result = result.append(movie_info)
    # if len(result) == NUMBER_MOVIES_RETURN:
    #   break

    http_resp = Response(response=json.dumps([], ensure_ascii=False).encode('utf-8'),
                         status=200,
                         mimetype="application/json; charset=utf-8")
    return http_resp

with open('review_pos_index' + '.pkl', 'rb') as f:
    inverted_index = pickle.load(f)

# with open('movie_all_data' + '.pkl', 'rb') as f:
#   movie_data = pickle.load(f)

app.run(host='127.0.0.1', port=9001)
