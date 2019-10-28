import json

from flask import Flask, Response, request

from imdbimporter.database.DatabaseConstants import engine

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

    genre = request.args.get('genre')
    director_name = request.args.get('director')
    actor_name = request.args.get('actor')
    language = request.args.get('language')
    year_start = request.args.get('year_start')
    year_end = request.args.get('year_end')
    rating = request.args.get('rating')

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
    if year_start is not None:
        filter.append("title.\"startYear\" >= " + str(year_start) +
                      " AND title.\"startYear\" <= " + str(year_end))
    if genre is not None:
        filter.append("title.\"genres\" ilike '%%" + genre + "%%'")
    # language has many null's

    count = 0
    for i in filter:
        if count == 0:
            query = query + " WHERE "
        else:
            query = query + " AND "

        query = query + i + " "
        count = count + 1

    rs = connection.execute(query)

    result = []
    for rowproxy in rs:
        result.append(rowproxy.values())

    return Response(response=json.dumps(result, ensure_ascii=False).encode('utf-8'),
                    status=200,
                    mimetype="application/json; charset=utf-8")

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
            return http_resp_empty
        else:
            return Response(response=json.dumps(result, ensure_ascii=False).encode('utf-8'),
                            status=200,
                            mimetype="application/json; charset=utf-8")

    return http_resp_empty


@app.route("/movie/<id>")
def get_movie_by_id(id):
    query = "select \"originalTitle\" FROM title WHERE tconst = '" + id + "'"
    rs = connection.execute(query)

    result = []
    for rowproxy in rs:
        result.append(rowproxy.values())

    http_resp = Response(response=json.dumps(result, ensure_ascii=False).encode('utf-8'),
                         status=200,
                         mimetype="application/json; charset=utf-8")
    return http_resp


@app.route("/level3", methods=['GET'])
def get_level_3():
    year = request.args.get('time')
    year = request.args.get('movie_characteristics')

    # TODO: implement the search
    # process characteristic : remove stopwrods...

    return 'ola'


connection = engine.connect()
app.run(host='127.0.0.1', port=9001)
