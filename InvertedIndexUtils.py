from math import log10

from TextProcessingUtils import clean_text


def TFIDF(term, document, d, number_of_docs):
    # Number of times term t appeared in document d.
    tf = len(d[term][document])

    # Number of documents term t appeared in.
    df = len(d[term].keys())

    return (1 + log10(tf)) * log10(number_of_docs / df)


def ranked_retrieval(d, number_of_docs, q):
    query = clean_text(q).split()

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
