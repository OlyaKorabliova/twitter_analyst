import re
import nltk
import glob
import random
import pickle
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.classify.scikitlearn import SklearnClassifier
from sklearn.svm import LinearSVC
from sklearn.naive_bayes import MultinomialNB
from sklearn.linear_model import LogisticRegression
from sklearn.linear_model import SGDClassifier

nltk.download('stopwords')
nltk.download('punkt')

filenames = glob.glob("data/*.txt")
print(filenames)

labled_tweets = []
all_words = []
stpwords = stopwords.words('english')

for filename in filenames:
    file = open(filename, encoding='utf-8').read()
    for tweet in file.split('\n'):
        tweet = re.sub(r'[^\w\s]', '', tweet)
        tweet = re.sub(" \d+", " ", tweet)
        tweet = [i.lower() for i in list(set(word_tokenize(tweet)) - set(stpwords))]
        all_words += tweet
        labled_tweets.append((tweet, filename[5:-4]))  # extract target names from filename

random.shuffle(labled_tweets)
print(labled_tweets[0:5])

word_features = list(all_words)
print(word_features[0:5])
print(all_words[0:5])


def get_features(tweet_text):
    tweet_words = set(tweet_text)
    features = {}
    for word in word_features:
        features['contains(%s)' % str(word)] = (word in tweet_words)
    return features

feature_set = [(get_features(text), label) for (text, label) in labled_tweets]

n = 400
train_set = feature_set[n:]
test_set = feature_set[:n]

print(len(train_set), len(test_set))

print(test_set[0])

# Train and test classifiers

NaiveBayes_classifier = nltk.NaiveBayesClassifier.train(train_set)
print("NaiveBayes accuracy:", (nltk.classify.accuracy(NaiveBayes_classifier, test_set)) * 100)

LinearSVC_classifier = SklearnClassifier(LinearSVC())
LinearSVC_classifier.train(train_set)
print("LinearSVC_classifier accuracy:", (nltk.classify.accuracy(LinearSVC_classifier, test_set)) * 100)

LogisticRegression_classifier = SklearnClassifier(LogisticRegression(multi_class='ovr'))  # one-vs-rest
LogisticRegression_classifier.train(train_set)
print("LogisticRegression_classifier accuracy:", (nltk.classify.accuracy(LogisticRegression_classifier, test_set)) * 100)

MNB_classifier = SklearnClassifier(MultinomialNB())
MNB_classifier.train(train_set)
print("MNB_classifier accuracy:", (nltk.classify.accuracy(MNB_classifier, test_set)) * 100)

SGD_classifier = SklearnClassifier(SGDClassifier(loss='hinge', penalty='l2', alpha=1e-3, random_state=42, max_iter=5, tol=None))
SGD_classifier.train(train_set)
print("SGD_classifier accuracy:", (nltk.classify.accuracy(SGD_classifier, test_set)) * 100)


# Save models
'''
save_word_features = open("word_features.pickle", "wb")
pickle.dump(word_features, save_word_features)
save_word_features.close()

save_classifier = open("NaiveBayes.pickle", "wb")
pickle.dump(NaiveBayes_classifier, save_classifier)
save_classifier.close()

save_classifier = open("SVC.pickle", "wb")
pickle.dump(LinearSVC_classifier, save_classifier)
save_classifier.close()

save_classifier = open("LogisticRegression.pickle", "wb")
pickle.dump(LogisticRegression_classifier, save_classifier)
save_classifier.close()

save_classifier = open("MNB.pickle","wb")
pickle.dump(MNB_classifier, save_classifier)
save_classifier.close()

save_classifier = open("SGD.pickle","wb")
pickle.dump(SGD_classifier, save_classifier)
save_classifier.close()
'''