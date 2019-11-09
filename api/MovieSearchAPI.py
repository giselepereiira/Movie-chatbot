# This is to avoid to send too much information and rising time out exceptions on the client
import json
import operator
import pickle

import nltk
import pandas as pd
from flask import Flask, Response, request

from imdbdatabase.DatabaseConstants import engine
from utils.InvertedIndexUtils import ranked_retrieval
from utils.TextProcessingUtils import clean_text

nltk.download('vader_lexicon')
from nltk.sentiment.vader import SentimentIntensityAnalyzer

sid = SentimentIntensityAnalyzer()

app = Flask(__name__)

HOST = '127.0.0.1'
PORT = 9001

# used in every method
HTTP_REST_EMPTY = Response(response=json.dumps([], ensure_ascii=False).encode('utf-8'),
                           status=200,
                           mimetype="application/json; charset=utf-8")

# Filters name
GENRE = 'genre'
YEAR_START = 'year_start'
DIRECTOR_NAME = 'director'
ACTOR_NAME = 'actor'
YEAR_END = 'year_end'
TOP_RATED = 'rating'
MOVIE_TITLE = 'movie_title'
MOVIE_ATTRIBUTE = 'movie_attribute'

# This is to avoid to send too much information and rising time out exceptions on the client
LEN_MAXIMUM_RESULT_RETURN = 100


# Return a movie given criteria
@app.route("/list-movie", methods=['GET'])
def get_movie():
    # accepted_keys = [YEAR_START, GENRE, DIRECTOR_NAME, ACTOR_NAME, YEAR_END, TOP_RATED]

    # for key in request.args.to_dict().keys():
        # the request comes with a parameter not allowed
    #   if key not in accepted_keys:
    #      return HTTP_REST_EMPTY

    genre = request.args.get(GENRE)
    director_name = request.args.get(DIRECTOR_NAME)
    actor_name = request.args.get(ACTOR_NAME)
    year_start = request.args.get(YEAR_START)
    year_end = request.args.get(YEAR_END)
    top_rated = request.args.get(TOP_RATED)

    filter = []

    if actor_name is None and director_name is None:
        query = "SELECT \"originalTitle\" FROM title "

    else:
        query = "SELECT \"originalTitle\" FROM title " \
                "INNER JOIN title_principals ON (title.tconst = title_principals.tconst)  " \
                "INNER JOIN people ON (people.nconst = title_principals.nconst)"

    if actor_name is not None:
        filter.append("people.\"primary_name_vector\" @@ to_tsquery('english', '" + actor_name.replace(" ", "&") + "')")
    if director_name is not None:
        filter.append(
            "people.\"primary_name_vector\" @@ to_tsquery('english', '" + director_name.replace(" ", "&") + "')")
    if year_start is not None and year_end is not None:
        filter.append("title.\"startYear\" >= " + str(year_start) +
                      " AND title.\"startYear\" <= " + str(year_end))
    elif year_start is not None:
        filter.append("title.\"startYear\" = " + str(year_start))
    if genre is not None:
        filter.append("title.\"genres\" ilike '%%" + genre + "%%'")

    count = 0
    for i in filter:
        if count == 0:
            query = query + " WHERE "
        else:
            query = query + " AND "

        query = query + i + " "
        count = count + 1

    if top_rated is not None:
        query = query + " ORDER BY RATING DESC NULLS LAST LIMIT " + str(top_rated)

    rs = connection.execute(query)

    result = []
    for row_proxy in rs:
        result.append(row_proxy.values())
        if len(result) == LEN_MAXIMUM_RESULT_RETURN:
            break

    return Response(response=json.dumps(result, ensure_ascii=False).encode('utf-8'),
                    status=200,
                    mimetype="application/json; charset=utf-8")


# Return info movie given the movie title
@app.route("/movie-info", methods=['GET'])
def get_movie_info():

    if MOVIE_TITLE not in request.args.to_dict().keys():
        return HTTP_REST_EMPTY
    else:

        movie_title = request.args.get(MOVIE_TITLE)

        query = "SELECT t.rating, t.\"startYear\", t.language, t.\"primaryTitle\", t.\"genres\", p.\"primaryName\", tp.category " \
                "from title as t " \
                "inner join title_principals tp on (t.tconst = tp.tconst)  " \
                "inner join people as p on (p.nconst = tp.nconst) " \
                "where t.\"primary_title_vector\" @@ to_tsquery('english','" + movie_title.replace(" ", "&") + "')"

        rs = connection.execute(query)

        director_names = set(["director", "producer"])
        actor_names = set(["actress", "self", "actor"])

        result = {}
        for row_proxy in rs:
            d, result_film = {}, {"actors": set(), "directors": set()}
            for column, value in row_proxy.items():
                d = {**d, **{column: value}}

            primary_title = d.get("primaryTitle")
            if result.get(primary_title) is None:
                result.update({primary_title: result_film})

            result.get(primary_title).update({"rating": d.get("rating")})
            result.get(primary_title).update({"language": d.get("language")})
            result.get(primary_title).update({"genres": d.get("genres")})
            result.get(primary_title).update({"year_start": d.get("startYear")})

            if d.get("category") in director_names:
                result.get(primary_title).get("directors").add(d.get("primaryName"))
            elif d.get("category") in actor_names:
                result.get(primary_title).get("actors").add(d.get("primaryName"))

        for i in result:
            directors = result.get(i).get("directors")
            actors = result.get(i).get("actors")

            result.get(i).update({"directors": list(directors)})
            result.get(i).update({"actors": list(actors)})

        if not result:
            # the movie does not exists
            return HTTP_REST_EMPTY
        else:
            return Response(response=json.dumps(result, ensure_ascii=False).encode('utf-8'),
                            status=200,
                            mimetype="application/json; charset=utf-8")


@app.route("/movie-with-attribute", methods=['GET'])
def get_movie_based_on_attribute():
    len_movies_dataset_cmu = 42303
    number_movies_return = 5
    len_movies_dataset_kaggle = 12500

    movie_attribute = request.args.get(MOVIE_ATTRIBUTE)

    year_start = request.args.get(YEAR_START)
    year_end = request.args.get(YEAR_END)
    genre = request.args.get(GENRE)
    director_name = request.args.get(DIRECTOR_NAME)
    actor_name = request.args.get(ACTOR_NAME)
    top_rated = request.args.get(TOP_RATED)

    sentiment_scores = sid.polarity_scores(clean_text(movie_attribute))

    if sentiment_scores['neg'] > sentiment_scores['pos'] and sentiment_scores['neg'] > sentiment_scores['neu']:
        # This is negative feeling
        scores = ranked_retrieval(inverted_index_kaggle_neg, len_movies_dataset_kaggle, movie_attribute)
        doc_scores = sorted(scores.items(), key=operator.itemgetter(1), reverse=True)

        input_get_movies = list()
        for index, value in enumerate(doc_scores):
            input_get_movies.append((str(value[0]), index))

        movie_list = get_movie_by_id(input_get_movies, genre, director_name, actor_name, year_start, year_end,
                                     top_rated)

        if not movie_list:
            return HTTP_REST_EMPTY

        return Response(response=json.dumps(movie_list[0: number_movies_return], ensure_ascii=False).encode('utf-8'),
                        status=200,
                        mimetype="application/json; charset=utf-8")

    if sentiment_scores['pos'] > sentiment_scores['neg'] and sentiment_scores['pos'] > sentiment_scores['neu']:
        # This is positive feeling
        scores = ranked_retrieval(inverted_index_kaggle_pos, len_movies_dataset_kaggle, movie_attribute)
        doc_scores = sorted(scores.items(), key=operator.itemgetter(1), reverse=True)

        input_get_movies = list()
        for index, value in enumerate(doc_scores):
            input_get_movies.append((str(value[0]), index))

        movie_list = get_movie_by_id(input_get_movies, genre, director_name, actor_name, year_start, year_end,
                                     top_rated)

        if not movie_list:
            return HTTP_REST_EMPTY

        return Response(response=json.dumps(movie_list[0: number_movies_return], ensure_ascii=False).encode('utf-8'),
                        status=200,
                        mimetype="application/json; charset=utf-8")

    if sentiment_scores['neu'] > sentiment_scores['neg'] and sentiment_scores['neu'] > sentiment_scores['pos']:
        # This is neutral feeling
        scores = ranked_retrieval(inverted_index_cmu, len_movies_dataset_cmu, movie_attribute)
        doc_scores = sorted(scores.items(), key=operator.itemgetter(1), reverse=True)

        result = pd.DataFrame()
        for value in doc_scores:
            movie_info = movie_data.loc[(movie_data['movie_id'] == int(str(value[0])))]
            if year_start is not None:
                movie_info = movie_info.loc[movie_data['date'] == str(year_start)]
            if genre is not None:
                movie_info = movie_info.loc[movie_data['genre'].contains(genre)]  # todo: to lower case genre

            if not movie_info.empty:
                result = result.append(movie_info)
            if len(result) == number_movies_return:
                break

        if result.empty:
            return HTTP_REST_EMPTY
        else:

            return Response(response=json.dumps(result['movie_name'].tolist(), ensure_ascii=False).encode('utf-8'),
                            status=200,
                            mimetype="application/json; charset=utf-8")


# Auxiliary  method to return the movie title given the id
def get_movie_by_id(movie_id, genre, director_name, actor_name, year_start, year_end, top_rated):
    filter = []

    join = "JOIN (VALUES " + str(movie_id).replace('[', '').replace(']', '') + \
           ") AS x(id, ordering) ON title.tconst = x.id "

    if actor_name is None and director_name is None:
        query = "SELECT \"originalTitle\" FROM title " + join

    else:
        query = "SELECT \"originalTitle\" FROM title " + join + \
                "INNER JOIN title_principals ON (title.tconst = title_principals.tconst)  " \
                "INNER JOIN people ON (people.nconst = title_principals.nconst) "

    if actor_name is not None:
        filter.append("people.\"primary_name_vector\" @@ to_tsquery('english', '" + actor_name.replace(" ", "&") + "')")
    if director_name is not None:
        filter.append(
            "people.\"primary_name_vector\" @@ to_tsquery('english', '" + director_name.replace(" ", "&") + "')")
    if year_start is not None and year_end is not None:
        filter.append("title.\"startYear\" >= " + str(year_start) +
                      " AND title.\"startYear\" <= " + str(year_end))
    elif year_start is not None:
        filter.append("title.\"startYear\" = " + str(year_start))
    if genre is not None:
        filter.append("title.\"genres\" ilike '%%" + genre + "%%'")

    count = 0
    for i in filter:
        if count == 0:
            query = query + " WHERE "
        else:
            query = query + " AND "

        query = query + i + " "
        count = count + 1

    query = query + " ORDER BY x.ordering"

    rs = connection.execute(query)

    result = []
    for rowproxy in rs:
        result.append(rowproxy.values())

    return result


with open('..\\cmudatabase\\movie_plot_index' + '.pkl', 'rb') as f:
    inverted_index_cmu = pickle.load(f)

with open('..\\cmudatabase\\movie_all_data' + '.pkl', 'rb') as f:
    movie_data = pickle.load(f)

with open('..\\kaggledatabase\\review_pos_index' + '.pkl', 'rb') as f:
    inverted_index_kaggle_pos = pickle.load(f)

with open('..\\kaggledatabase\\review_neg_index' + '.pkl', 'rb') as f:
    inverted_index_kaggle_neg = pickle.load(f)

connection = engine.connect()
app.run(host=HOST, port=PORT)
