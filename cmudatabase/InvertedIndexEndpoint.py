import operator
import pickle

from flask import Flask, request
from math import log10

from cmudatabase.TextProcessingUtils import clean_text, remove_stopwords

app = Flask(__name__)
LEN_MOVIES_DATASET = 42303


@app.route("/level3", methods=['GET'])
def get_level_3():
    time = request.args.get('time')
    movie_characteristics = request.args.get('movie_characteristics')

    with open('movie_plot_index' + '.pkl', 'rb') as f:
        inverted_index = pickle.load(f)

    scores = ranked_retrieval(inverted_index, LEN_MOVIES_DATASET, movie_characteristics)
    doc_scores = sorted(scores.items(), key=operator.itemgetter(1), reverse=True)

    # TODO : return the 3 first movies

    with open('movie_all_data' + '.pkl', 'rb') as f:
        movie_data = pickle.load(f)

    first_doc_id = doc_scores[0][0]
    for ids in doc_scores[:][0]:
        movie_info = movie_data.loc[movie_data['movie_id'] == first_doc_id & [movie_data['date']] == time]

    return 'ola'


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

    # Helper function to print the results.


def get_scores_output(query, scores):
    doc_scores = sorted(scores.items(), key=operator.itemgetter(1), reverse=True)
    text = "Query: " + query + "\nNumber of documents: " + str(len(scores)) + "\n"
    for i in range(len(doc_scores)):
        if i == 20:
            break
        text += "{} | {}\n".format(doc_scores[i][0], doc_scores[i][1])
    return text


app.run(host='127.0.0.1', port=9001)
