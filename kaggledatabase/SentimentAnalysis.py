import nltk

nltk.download('vader_lexicon')
from nltk.sentiment.vader import SentimentIntensityAnalyzer

sid = SentimentIntensityAnalyzer()
sentence = 'awesome special effects'
print(sid.polarity_scores(sentence))
