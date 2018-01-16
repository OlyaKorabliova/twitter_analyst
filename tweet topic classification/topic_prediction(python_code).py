import pickle
import nltk

classifier = pickle.load(open('model/MNB.pickle', 'rb'))
word_features = pickle.load(open('model/word_features.pickle', 'rb'))


def get_features(tweet_text):
    tweet_words = set(tweet_text)
    features = {}
    for word in word_features:
        features['contains(%s)' % str(word)] = (word in tweet_words)
    return features


def predict_topic(tweet_text):
    tweet = nltk.word_tokenize(tweet_text.lower())
    return classifier.classify(get_features(tweet))

topic = predict_topic("The stock market has gained an incredible 7.8 Trillion dollars in market value since @POTUS was elected! Looks like 4% economic growth in 4th quarter, lowest level of claims for unemployment benefits in 44 years, and black unemployment rate is the lowest (6.8%) on record!")
print(topic)

topic = predict_topic("Yesterday was a big day for the stock market. Jobs are coming back to America. Chrysler is coming back to the USA, from Mexico and many others will follow. Tax cut money to employees is pouring into our economy with many more companies announcing. American business is hot again!")
print(topic)

topic = predict_topic("Sadly, Democrats want to stop paying our troops and government workers in order to give a sweetheart deal, not a fair deal, for DACA. Take care of our Military, and our Country, FIRST!")
print(topic)

topic = predict_topic("The Democrats seem intent on having people and drugs pour into our country from the Southern Border, risking thousands of lives in the process. It is my duty to protect the lives and safety of all Americans. We must build a Great Wall, think Merit and end Lottery & Chain. USA!")
print(topic)

topic = predict_topic("Java is the best programming language.")
print(topic)

topic = predict_topic("College football’s #NationalChampionship will be decided tonight. Keep it here for highlights, updates and commentary as Alabama takes on Georgia for the title.")
print(topic)