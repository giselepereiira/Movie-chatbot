from imdbimporter.database.DatabaseConstants import session

import json
from flask import Flask, Response, request

from imdbimporter.models.Title import Title

app = Flask(__name__)

# Call http://localhost:9001/ping?year=1990

@app.route("/movie", methods=['GET'])
def get_movie():
    year = request.args.get('year')
    genre = request.args.get('genre')

    filter = []

    if year is not None:
        filter.append(Title.year == int(year))
    if genre is not None:
        filter.append(Title.genre.ilike("%" + genre + "%"))

    x = session.query(Title.title)

    for i in filter:
        x = x.filter(i)

    result = x.all()

    http_resp = Response(response=json.dumps(result, ensure_ascii=False).encode('utf-8'),
                         status=200,
                         mimetype="application/json; charset=utf-8")
    return http_resp

app.run(host='127.0.0.1', port=9001)