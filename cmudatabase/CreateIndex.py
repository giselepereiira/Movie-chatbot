import operator
import pickle
from cmath import log10

from cmudatabase.Importer import get_data
from cmudatabase.TextProcessingUtils import clean_text
from cmudatabase.TextProcessingUtils import remove_stopwords

save_index = False


def create_index_entry(news):
    d = {}  # Dictonary for the inverted index.

    for index, row in news.iterrows():
        movie_id = row['movie_id']  # ID
        clean_plot = row['clean_plot'].split()  # CONTENT

        for i in range(len(clean_plot)):
            word = clean_plot[i]
            word_index = i + 1

            if word not in d:
                d[word] = {movie_id: [word_index]}
            else:
                if movie_id not in d[word]:
                    d[word][movie_id] = [word_index]  # Create new entry.
                else:
                    d[word][movie_id].append(word_index)  # Append new index.
    return d


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


# Normal search
query = "south korea"
movies = get_data()
d_content = create_index_entry(movies)
scores = ranked_retrieval(d_content, len(movies['movie_id']), query)
print(get_scores_output(query, scores))

if save_index:
    with open('movie_plot_index' + '.pkl', 'wb') as f:
        pickle.dump(d_content, f, pickle.HIGHEST_PROTOCOL)
