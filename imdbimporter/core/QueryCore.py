import json

from flask import Flask, Response, request

from imdbimporter.database.DatabaseConstants import session
from imdbimporter.models.Title import Title

app = Flask(__name__)


@app.route("/movie", methods=['GET'])
def get_movie():
    result = []
    filter = []
    http_resp_empty = Response(response=json.dumps(result, ensure_ascii=False).encode('utf-8'),
                               status=200,
                               mimetype="application/json; charset=utf-8")
    accepted_keys = ['year', 'genre', 'director', 'actor', 'language', 'year_start', 'year_end', 'rating']

    for key in request.args.to_dict().keys():
        # the request comes with a parameter not allowed
        if key not in accepted_keys:
            return http_resp_empty

    year = request.args.get('year')
    genre = request.args.get('genre')
    director_name = request.args.get('director')
    actor_name = request.args.get('actor')
    language = request.args.get('language')
    year_start = request.args.get('year_start')
    year_end = request.args.get('year_end')
    rating = request.args.get('rating')

    if actor_name is None and director_name is None:
        if year is not None:
            filter.append(Title.year == int(year))
        if genre is not None:
            filter.append(Title.genre.ilike("%" + genre + "%"))  # ilike is case insensitive

        if year_start is not None and year_end is None:
            # lower range value
            filter.append(Title.year == int(year_start))
        if year_start is not None and year_end is not None:
            # TODO add between
            print()
        if year_start is None and year_end is not None:
            filter.append(Title.year == int(year_end))

        x = session.query(Title.title)

        for i in filter:
            x = x.filter(i)
    else:
        query = "\"originalTitle\" from title " \
                "inner join people_title on (title.tconst = people_title.id_titles)  " \
                "inner join people on (people.nconst = people_title.id_names) "

        if actor_name is not None:
            filter.append("people.\"primaryName\" ilike '%" + actor_name + "%'")
        if director_name is not None:
            filter.append("people.\"primaryName\" ilike '%" + actor_name + "%'")
        if year is not None:
            filter.append("title.\"startYear\" = " + str(year))
        if genre is not None:
            filter.append("title.\"genres\" ilike '%" + genre + "%'")

        count = 0
        for i in filter:
            if count == 0:
                query = query + " WHERE "
            else:
                query = query + " AND "

            query = query + i + " "
            count = count + 1

        x = session.query(query)

    result = x.all()

    http_resp = Response(response=json.dumps(result, ensure_ascii=False).encode('utf-8'),
                             status=200,
                             mimetype="application/json; charset=utf-8")
    return http_resp





@app.route("/movieInfo", methods=['GET'])
def get_movie_info():
    result = []
    http_resp_empty = Response(response=json.dumps(result, ensure_ascii=False).encode('utf-8'),
                               status=200,
                               mimetype="application/json; charset=utf-8")

    if 'movie_title' not in request.args.to_dict().keys():
        return http_resp_empty
    else:
        filter = list()
        movie_title = request.args.get('movie_title')

        filter.append(Title.title == movie_title)
        x = session.query(Title.title)
        result = x.filter(Title.title == movie_title).all()
        if not result:
            # the movie does not exists
            return http_resp_empty
        else:
            accepted_keys = ['year', 'genre', 'director', 'actor', 'language', 'year_start', 'year_end', 'rating']

            for key in request.args.to_dict().keys():
                # the request comes with a parameter not allowed
                if key not in accepted_keys:
                    result = []
                    http_resp = Response(response=json.dumps(result, ensure_ascii=False).encode('utf-8'),
                                         status=200,
                                         mimetype="application/json; charset=utf-8")
                    return http_resp





app.run(host='127.0.0.1', port=9001)
