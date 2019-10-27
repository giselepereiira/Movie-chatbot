import json
import operator
import pickle

import pandas as pd
from flask import Flask, request, Response
from math import log10

from cmudatabase.TextProcessingUtils import clean_text, remove_stopwords

app = Flask(__name__)
LEN_MOVIES_DATASET = 42303
NUMBER_MOVIES_RETURN = 3


@app.route("/level3", methods=['GET'])
def get_level_3():
    time = request.args.get('time')
    movie_characteristics = request.args.get('movie_characteristics')

    scores = ranked_retrieval(inverted_index, LEN_MOVIES_DATASET, movie_characteristics)
    doc_scores = sorted(scores.items(), key=operator.itemgetter(1), reverse=True)

    result = pd.DataFrame()
    for value in doc_scores:
        id = str(value[0])
        movie_info = movie_data.loc[(movie_data['movie_id'] == int(id)) & (movie_data['date'] == str(time))]
        if not movie_info.empty:
            result = result.append(movie_info)
        if len(result) == NUMBER_MOVIES_RETURN:
            break

    http_resp = Response(response=json.dumps(result['movie_name'].tolist(), ensure_ascii=False).encode('utf-8'),
                         status=200,
                         mimetype="application/json; charset=utf-8")
    return http_resp




def TFIDF(term, document, d, number_of_docs):
    # Number of times term t appeared in document d.
    tf = len(d[term][document])

    # Number of documents term t appeared in.
    df = len(d[term].keys())

    return (1 + log10(tf)) * log10(number_of_docs / df)


def ranked_retrieval(d, number_of_docs, q):
    query = clean_text(q)
    query = remove_stopwords(query).split()

    scores = {}
    for i in range(len(query)):
        # For each word in query.
        word = query[i]

        if word in d:

            # Filter matching documents.
            for document in d[word].keys():

                # Calculate TF-IDF.
                calculated_tfidf = TFIDF(word, document, d, number_of_docs)

                # Ignore score 0.
                if calculated_tfidf != 0:
                    if document in scores:
                        scores[document] += calculated_tfidf
                    else:
                        scores[document] = calculated_tfidf

    # scores = {
    #  1 => score
    #  2 => score
    # }
    return scores


with open('movie_plot_index' + '.pkl', 'rb') as f:
    inverted_index = pickle.load(f)

with open('movie_all_data' + '.pkl', 'rb') as f:
    movie_data = pickle.load(f)

app.run(host='127.0.0.1', port=9001)
