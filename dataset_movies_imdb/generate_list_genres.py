import csv
import get_id_movies

list_ids_movies = get_id_movies.get_ids_movies()

list_genres = list()
with open('title.basics.tsv', encoding="utf8") as tsvfile:
    reader = csv.DictReader(tsvfile, dialect='excel-tab')
    for row in reader:
        if row['tconst'] in list_ids_movies:
            if row['genres'] is not None:
                all_genres_row = row['genres'].lower().split(",")
                for genre in all_genres_row:
                    if genre not in list_genres:
                        list_genres.append(genre)

list_genres.remove("\\n")

with open('genres_movies_list.txt', 'w') as f:
    for item in list_genres:
        f.write("%s\n" % item)
