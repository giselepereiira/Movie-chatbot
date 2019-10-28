import json
import operator
import pickle

import nltk
import pandas as pd
from flask import Flask, Response, request

from InvertedIndexUtils import ranked_retrieval
from imdbimporter.database.DatabaseConstants import engine

nltk.download('vader_lexicon')
from nltk.sentiment.vader import SentimentIntensityAnalyzer

sid = SentimentIntensityAnalyzer()

app = Flask(__name__)

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
MOVIE_CHARACTERISTIC = 'movie_characteristic'


@app.route("/movie", methods=['GET'])
def get_movie():
    accepted_keys = [YEAR_START, GENRE, DIRECTOR_NAME, ACTOR_NAME, YEAR_END, TOP_RATED]

    for key in request.args.to_dict().keys():
        # the request comes with a parameter not allowed
        if key not in accepted_keys:
            return HTTP_REST_EMPTY

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
                "INNER JOIN people_title ON (title.tconst = people_title.id_titles)  " \
                "INNER JOIN people ON (people.nconst = people_title.id_names) "

    if actor_name is not None:
        filter.append("people.\"primary_name_vector\" @@ to_tsquery('" + actor_name.replace(" ", "&") + "')")
    if director_name is not None:
        filter.append("people.\"primary_name_vector\" @@ to_tsquery('" + director_name.replace(" ", "&") + "')")
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
    for rowproxy in rs:
        result.append(rowproxy.values())

    return Response(response=json.dumps(result, ensure_ascii=False).encode('utf-8'),
                    status=200,
                    mimetype="application/json; charset=utf-8")


@app.route("/movieInfo", methods=['GET'])
def get_movie_info():
    if MOVIE_TITLE not in request.args.to_dict().keys():
        return HTTP_REST_EMPTY
    else:

        movie_title = request.args.get(MOVIE_TITLE)

        query = "SELECT t.rating, t.language, t.\"primaryTitle\", t.\"genres\", p.\"primaryProfession\", p.\"primaryName\" " \
                "from title as t " \
                "inner join people_title on (t.tconst = people_title.id_titles)  " \
                "inner join people as p on (p.nconst = people_title.id_names) " \
                "where t.\"primary_title_vector\" @@ to_tsquery('" + movie_title.replace(" ", "&") + "')"

        rs = connection.execute(query)

        d, result, result_film = {}, {}, {"actors": set(), "directors": set()},
        for rowproxy in rs:
            for column, value in rowproxy.items():
                d = {**d, **{column: value}}

            primary_title = d.get("primaryTitle")
            if result.get(primary_title) is None:
                result.update({primary_title: result_film})

            result.get(primary_title).update({"rating": d.get("rating")})
            result.get(primary_title).update({"language": d.get("language")})
            if 'director' in d.get("primaryProfession"):
                result.get(primary_title).get("directors").add(d.get("primaryName"))
            else:
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


def get_movie_by_id(movie_id, genre, director_name, actor_name, year_start, year_end, top_rated):
    filter = ["title.tconst IN " + str(movie_id).replace('[', '(').replace(']', ')')]

    if actor_name is None and director_name is None:
        query = "SELECT \"originalTitle\" FROM title "

    else:
        query = "SELECT \"originalTitle\" FROM title " \
                "INNER JOIN people_title ON (title.tconst = people_title.id_titles)  " \
                "INNER JOIN people ON (people.nconst = people_title.id_names) "

    if actor_name is not None:
        filter.append("people.\"primary_name_vector\" @@ to_tsquery('" + actor_name.replace(" ", "&") + "')")
    if director_name is not None:
        filter.append("people.\"primary_name_vector\" @@ to_tsquery('" + director_name.replace(" ", "&") + "')")
    if year_start is not None and year_end is not None:
        filter.append("title.\"startYear\" >= " + str(year_start) +
                      " AND title.\"startYear\" <= " + str(year_end))
    elif year_start is not None:
        filter.append("title.\"startYear\" >= " + str(year_start))
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
    for rowproxy in rs:
        result.append(rowproxy.values())

    return result


@app.route("/level3", methods=['GET'])
def get_level_3():
    len_movies_dataset_cmu = 42303
    number_movies_return = 5
    len_movies_dataset_kaggle = 12500

    movie_characteristics = request.args.get(MOVIE_CHARACTERISTIC)

    year_start = request.args.get(YEAR_START)
    year_end = request.args.get(YEAR_END)
    genre = request.args.get(GENRE)
    director_name = request.args.get(DIRECTOR_NAME)
    actor_name = request.args.get(ACTOR_NAME)
    top_rated = request.args.get(TOP_RATED)

    sentiment_scores = sid.polarity_scores(movie_characteristics)

    if sentiment_scores['neg'] > sentiment_scores['pos'] and sentiment_scores['neg'] > sentiment_scores['neu']:
        # This is negative feeling
        scores = ranked_retrieval(inverted_index_kaggle_neg, len_movies_dataset_kaggle, movie_characteristics)
        doc_scores = sorted(scores.items(), key=operator.itemgetter(1), reverse=True)

        input_get_movies = list()
        for value in doc_scores:
            input_get_movies.append(str(value[0]))

        movie_list = get_movie_by_id(input_get_movies, genre, director_name, actor_name, year_start, year_end,
                                     top_rated)

        if not movie_list:
            return HTTP_REST_EMPTY

        return Response(response=json.dumps(movie_list[0: number_movies_return], ensure_ascii=False).encode('utf-8'),
                        status=200,
                        mimetype="application/json; charset=utf-8")

    if sentiment_scores['pos'] > sentiment_scores['neg'] and sentiment_scores['pos'] > sentiment_scores['neu']:
        # This is positive feeling
        scores = ranked_retrieval(inverted_index_kaggle_pos, len_movies_dataset_kaggle, movie_characteristics)
        doc_scores = sorted(scores.items(), key=operator.itemgetter(1), reverse=True)

        input_get_movies = list()
        for value in doc_scores:
            input_get_movies.append(str(value[0]))

        movie_list = get_movie_by_id(input_get_movies, genre, director_name, actor_name, year_start, year_end,
                                     top_rated)

        if not movie_list:
            return HTTP_REST_EMPTY

        return Response(response=json.dumps(movie_list[0: number_movies_return], ensure_ascii=False).encode('utf-8'),
                        status=200,
                        mimetype="application/json; charset=utf-8")

    if sentiment_scores['neu'] > sentiment_scores['neg'] and sentiment_scores['neu'] > sentiment_scores['pos']:
        # This is neutral feeling
        scores = ranked_retrieval(inverted_index_cmu, len_movies_dataset_cmu, movie_characteristics)
        doc_scores = sorted(scores.items(), key=operator.itemgetter(1), reverse=True)

        result = pd.DataFrame()
        for value in doc_scores:
            id = str(value[0])
            movie_info = movie_data.loc[(movie_data['movie_id'] == int(id))]  # & (movie_data['date'] == str(time))]
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


with open('cmudatabase\\movie_plot_index' + '.pkl', 'rb') as f:
    inverted_index_cmu = pickle.load(f)

with open('cmudatabase\\movie_all_data' + '.pkl', 'rb') as f:
    movie_data = pickle.load(f)

with open('kaggledatabase\\review_pos_index' + '.pkl', 'rb') as f:
    inverted_index_kaggle_pos = pickle.load(f)

with open('kaggledatabase\\review_neg_index' + '.pkl', 'rb') as f:
    inverted_index_kaggle_neg = pickle.load(f)

connection = engine.connect()
app.run(host='127.0.0.1', port=9001)
