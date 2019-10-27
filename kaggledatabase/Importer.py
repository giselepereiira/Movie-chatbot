import os
import re

import pandas as pd

from TextProcessingUtils import clean_text

path = "C:\\Users\\Gisele\\Downloads\\aclImdb\\"

url_pos = []
with open(path + "train\\urls_pos.txt", encoding="latin1") as f:
    for line in f:
        url_pos.append(re.sub('/usercomments\\n', '', line[26:]))

list_files = os.listdir(path + "train/pos/")

ordered_list_file = []
for i in range(0, len(list_files)):
    name_file = str(i) + '_7.txt'
    if name_file in list_files:
        ordered_list_file.append(name_file)
    name_file = str(i) + '_8.txt'
    if name_file in list_files:
        ordered_list_file.append(name_file)
    name_file = str(i) + '_9.txt'
    if name_file in list_files:
        ordered_list_file.append(name_file)
    name_file = str(i) + '_10.txt'
    if name_file in list_files:
        ordered_list_file.append(name_file)

positiveReviews = []
for pfile in ordered_list_file:
    with open(path + "train/pos/" + pfile, encoding="latin1") as f:
        positiveReviews.append(clean_text(f.read()))

reviews = pd.DataFrame({"review": positiveReviews, "label": 1, "file": ordered_list_file, 'url': url_pos})
reviews.to_pickle('review_pos_id.pkl')

print(reviews.head())

url_neg = []
with open(path + "train\\urls_neg.txt", encoding="latin1") as f:
    for line in f:
        url_neg.append(re.sub('/usercomments\\n', '', line[26:]))

list_files = os.listdir(path + "train/neg/")

ordered_list_file = []
for i in range(0, len(list_files)):
    name_file = str(i) + '_1.txt'
    if name_file in list_files:
        ordered_list_file.append(name_file)
    name_file = str(i) + '_2.txt'
    if name_file in list_files:
        ordered_list_file.append(name_file)
    name_file = str(i) + '_3.txt'
    if name_file in list_files:
        ordered_list_file.append(name_file)
    name_file = str(i) + '_4.txt'
    if name_file in list_files:
        ordered_list_file.append(name_file)

negativeReviews = []
for pfile in ordered_list_file:
    with open(path + "train/neg/" + pfile, encoding="latin1") as f:
        negativeReviews.append(clean_text(f.read()))

reviews = pd.DataFrame({"review": negativeReviews, "label": 0, "file": ordered_list_file, 'url': url_neg})
reviews.to_pickle('review_neg_id.pkl')
