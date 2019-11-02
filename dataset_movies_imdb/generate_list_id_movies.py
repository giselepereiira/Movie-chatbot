import csv

list_ids = list()
with open('title.basics.tsv', encoding="utf8") as tsvfile:
    reader = csv.DictReader(tsvfile, dialect='excel-tab')
    for row in reader:
        if row['titleType'] is not None:
            type_project = row['titleType']
            if type_project == 'movie':
                list_ids.append(row['tconst'])


with open('movies_id_list.txt', 'w') as f:
    for item in list_ids:
        f.write("%s\n" % item)