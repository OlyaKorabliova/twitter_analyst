import os
import nltk
import glob
import re
import random
import numpy as np
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
from nltk.classify.scikitlearn import SklearnClassifier
from sklearn.naive_bayes import MultinomialNB
from sklearn.linear_model import SGDClassifier

filenames = glob.glob("data/*.txt")
print(filenames)

labled_tweets = []
stpwords = stopwords.words('english')

for filename in filenames:
    file = open(filename, encoding='utf-8').read()
    for tweet in file.split('\n'):
        tweet = re.sub(r'[^\w\s]','', tweet)
        tweet = re.sub(" \d+", " ", tweet)
        tweet = [i.lower() for i in list(set(nltk.word_tokenize(tweet)) - set(stpwords))]
        labled_tweets.append((tweet, filename[5:-4]))

random.shuffle(labled_tweets)
print(labled_tweets[0:5])


data = [entry[0] for entry in labled_tweets]

targets = []
for entry in labled_tweets:
    t = entry[1]
    if t == 'business':
        targets.append(1)
    if t == 'entertainment':
        targets.append(2)
    if t == 'health':
        targets.append(3)
    if t == 'politics':
        targets.append(4)
    if t == 'sports':
        targets.append(5)
    if t == 'technology':
        targets.append(6)

print(data[0])
print(targets[0])

n = 400
train_data = data[n:]
test_data = data[:n]
train_targets = targets[n:]
test_targets = targets[:n]

count_vect = CountVectorizer(tokenizer=lambda doc: doc, lowercase=False)
train_vect = count_vect.fit_transform(train_data)
test_vect = count_vect.transform(test_data)
print(train_vect.shape)

count_vect.vocabulary_.get(u'algorithm')

tfidf_transformer = TfidfTransformer()
train_tfidf = tfidf_transformer.fit_transform(train_vect)
test_tfidf = tfidf_transformer.transform(test_vect)
print(train_tfidf.shape)

MNB_classifier = MultinomialNB().fit(train_tfidf, train_targets)

SGD_classifier = SGDClassifier(loss='hinge', penalty='l2', alpha=1e-3,
                               random_state=42, max_iter=5, tol=None).fit(train_tfidf, train_targets)

predicted = MNB_classifier.predict(test_tfidf)
print(np.mean(predicted == test_targets) * 100)

predicted = SGD_classifier.predict(test_tfidf)
print(np.mean(predicted == test_targets) * 100)