import csv

def get_ids_movies():
    list_ids = list()
    with open('movies_id_list.txt') as csv_file:
        csv_reader = csv.reader(csv_file)
        for row in csv_reader:
            list_ids.append(row[0])
    return list_ids
