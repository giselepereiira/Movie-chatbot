import csv

import pandas as pd
from tqdm import tqdm

from cmudatabase.TextProcessingUtils import clean_text
from cmudatabase.TextProcessingUtils import remove_stopwords


def get_data():
    meta = pd.read_csv("movie.metadata.tsv", sep='\t', header=None)

    # rename columns
    meta.columns = ["movie_id", 1, "movie_name", 3, 4, 5, 6, 7, "genre"]
    plots = []

    with open("plot_summaries.txt", 'r', encoding="utf8") as f:
        reader = csv.reader(f, dialect='excel-tab')
        for row in tqdm(reader):
            plots.append(row)

    movie_id = []
    plot = []

    # extract movie Ids and plot summaries
    for i in tqdm(plots):
        movie_id.append(i[0])
        plot.append(i[1])

    # create dataframe
    movies = pd.DataFrame({'movie_id': movie_id, 'plot': plot})
    # change datatype of 'movie_id'
    meta['movie_id'] = meta['movie_id'].astype(str)

    movies['clean_plot'] = movies['plot'].apply(lambda x: clean_text(x))

    movies['clean_plot'] = movies['clean_plot'].apply(lambda x: remove_stopwords(x))

    return movies


def get_data_movies():
    meta = pd.read_csv("movie.metadata.tsv", sep='\t', header=None)

    # rename columns
    meta.columns = ["movie_id", 1, "movie_name", "date", "revenue", "runtime", "languages", "countries", "genre"]
    meta.to_pickle("movie_all_data.pkl")


get_data_movies()
