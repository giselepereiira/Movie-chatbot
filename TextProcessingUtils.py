import re

import nltk
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer

nltk.download('stopwords')
stop_words = set(stopwords.words('english'))
ps = PorterStemmer()

# function for text cleaning
def clean_text(text):

    # remove backslash-apostrophe
    text = re.sub("\'", "", text)
    # remove everything except alphabets
    text = re.sub("[^a-zA-Z]", " ", text)
    # remove whitespaces
    text = ' '.join(text.split())
    # convert text to lowercase
    text = text.lower()
    # remove stiopwords
    text = ' '.join([w for w in text.split() if not w in stop_words])
    # stemming
    text = ' '.join([ps.stem(w) for w in text.split()])

    return text
