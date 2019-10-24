from imdbimporter.database.DatabaseConstants import session

import json
from flask import Flask, Response, request

from imdbimporter.models.Title import Title

app = Flask(__name__)


@app.route("/movie", methods=['GET'])
def get_movie():
    accepted_keys = ['year', 'genre', 'director', 'actor', 'language', 'year_start', 'year_end', 'rating']

    for key in request.args.to_dict().keys():
        # the request comes with a parameter not allowed
        if key not in accepted_keys:
            result = []
            http_resp = Response(response=json.dumps(result, ensure_ascii=False).encode('utf-8'),
                                 status=200,
                                 mimetype="application/json; charset=utf-8")
            return http_resp

    year = request.args.get('year')
    genre = request.args.get('genre')
    director = request.args.get('director')
    actor = request.args.get('actor')
    language = request.args.get('language')
    year_start = request.args.get('year_start')
    year_end = request.args.get('year_end')
    rating = request.args.get('rating')

    filter = list()
    if year is not None:
        filter.append(Title.year == int(year))
    if genre is not None:
        filter.append(Title.genre.ilike("%" + genre + "%"))  # ilike is case insensitive
    # TODO implement others filters when DB is ready
    # if director is not None:
    #   filter.append(Title.year == int(year))

    if year_start is not None and year_end is None:
        # lower range value
        filter.append(Title.year == int(year_start))
    if year_start is not None and year_end is not None:
        # TODO add between
        print()
    if year_start is None and year_end is not None:
        filter.append(Title.year == int(year_end))

    x = session.query(Title.title)
    session.close()

    for i in filter:
        x = x.filter(i)

    result = x.all()

    http_resp = Response(response=json.dumps(result, ensure_ascii=False).encode('utf-8'),
                         status=200,
                         mimetype="application/json; charset=utf-8")
    return http_resp


app.run(host='127.0.0.1', port=9001)
