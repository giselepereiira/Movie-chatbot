import pickle

save_index = False


def create_index_entry(movies):
    d = {}  # Dictonary for the inverted index.

    for index, row in movies.iterrows():
        movie_id = row['url']  # ID
        clean_plot = row['review'].split()  # CONTENT

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


with open('review_neg_id' + '.pkl', 'rb') as f:
    review_pos = pickle.load(f)

d_content = create_index_entry(review_pos)

with open('review_neg_index' + '.pkl', 'wb') as f:
    pickle.dump(d_content, f, pickle.HIGHEST_PROTOCOL)
