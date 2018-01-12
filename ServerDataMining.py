from time import gmtime, strftime

import argparse
import json
import string
import time
import io

import tweepy
from tweepy import OAuthHandler
from tweepy.streaming import StreamListener

consumer_key = 'Nz8KV7mU5bRrBgklgYxiKrwyd'
consumer_secret = 'YW44MtGOjNvUb8jsS5ZDg1SH4x33jUVjVMPObov0koKzpf91BN'
access_token = '2354646819-Ioz4HKaKVnymsOh0Q7bWtObTIhPBAcurZBlzvv5'
access_secret = 'qHNqtiyyaUbp6TkWzivrMuYimiiRpApeyXJYoODBvAG2u'


def get_parser():
    """Get parser for command line arguments."""
    parser = argparse.ArgumentParser(description="Twitter Downloader")
    parser.add_argument("-q",
                        "--query",
                        dest="query",
                        help="Query/Filter",
                        default='-')
    return parser


class MyListener(StreamListener):
    """Custom StreamListener for streaming data."""

    def __init__(self, query):
        query_fname = format_filename(query)
        self.outfile = "stream_%s.json" % (query_fname)

    def on_data(self, data):
        try:
            with open(self.outfile, 'a') as f:
                f.write(data)
                print(data)
                return True
        except BaseException as e:
            print("Error on_data: %s" % str(e))
            time.sleep(5)
        return True

    def on_error(self, status):
        print(status)
        return True


def format_filename(fname):
    """Convert file name into a safe string.
    Arguments:
        fname -- the file name to convert
    Return:
        String -- converted file name
    """
    return ''.join(convert_valid(one_char) for one_char in fname)


def convert_valid(one_char):
    """Convert a character into '_' if invalid.
    Arguments:
        one_char -- the char to convert
    Return:
        Character -- converted char
    """
    valid_chars = "-_.%s%s" % (string.ascii_letters, string.digits)
    if one_char in valid_chars:
        return one_char
    else:
        return '_'


@classmethod
def parse(cls, api, raw):
    status = cls.first_parse(api, raw)
    setattr(status, 'json', json.dumps(raw))
    return status


def fetchPeople(person, n_of_pages):
    while True:
        try:
            auth = OAuthHandler(consumer_key, consumer_secret)
            auth.set_access_token(access_token, access_secret)
            api = tweepy.API(auth)

            with io.open(person + '.json', 'a', encoding='utf8') as fp:
                for x in range(1, n_of_pages):
                    new_tweets = api.user_timeline(screen_name=person, page=x, tweet_mode="extended")
                    if not new_tweets:
                        break
                    tweets = [[tweet.full_text] for tweet in new_tweets if
                              (not tweet.retweeted) and ('RT @' not in tweet.full_text)]
                    for i in range(len(tweets) - 1):
                        json.dump(tweets[i], fp, ensure_ascii=False)
                    new_tweets.clear()

            #update_list_file(api, "list_of_US_Politicians.txt")

            return "Done"
        except tweepy.TweepError:
            time.sleep(60 * 15)
            continue


def update_list_file(api, filename):
    with open(filename, "a") as mainfile:
        fullname = api.get_user(person, include_entities=1).name
        mainfile.write(fullname + ' = ' + person + '.json' + "\n")

if __name__ == '__main__':
    us_politicians = ["@BillClinton", "@donnabrazile", "@NancyPelosi", "@JoeBiden", "@DWStweets",
                      "@theclobra", "@madeleine", "@kharyp", "@GDouglasJones", "@SenShelby", "@SenDanSullivan",
                      "@lisamurkowski", "@SenJohnMcCain", "@JeffFlake", "@SenTomCotton", "@JohnBoozman",
                      "@SenFeinstein", "@KamalaHarris", "@SenCoryGardner", "@SenBennetCO", "@SenBlumenthal",
                      "@ChrisMurphyCT", "@SenatorCarper", "@ChrisCoons", "@SenBillNelson", "@marcorubio",
                      "@sendavidperdue", "@SenatorIsakson", "@SenBrianSchatz", "@maziehirono", "@SenatorRisch",
                      "@MikeCrapo", "@SenDuckworth", "@SenatorDurbin", "@SenToddYoung", "@SenDonnelly", "@SenJoniErnst",
                      "@ChuckGrassley", "@SenPatRoberts", "@JerryMoran", "@SenateMajLdr", "@RandPaul",
                      "@SenJohnKennedy", "@BillCassidy", "@SenAngusKing", "@SenatorCollins", "@SenatorCardin",
                      "@ChrisVanHollen", "@SenWarren", "@SenMarkey", "@SenGaryPeters", "@SenStabenow", "@amyklobuchar",
                      "@TinaSmithMN", "@SenThadCochran", "@SenatorWicker", "@RoyBlunt", "@clairecmc", "@SenatorTester",
                      "@SteveDaines", "@SenSasse", "@SenatorFischer", "@SenCortezMasto", "@SenDeanHeller",
                      "@SenatorHassan", "@SenatorShaheen", "@SenatorMenendez", "@CoryBooker", "@MartinHeinrich",
                      "@SenatorTomUdall", "@SenGillibrand", "@SenSchumer", "@SenThomTillis", "@SenatorBurr",
                      "@SenatorHeitkamp", "@SenJohnHoeven", "@SenSherrodBrown", "@senrobportman", "@SenatorLankford",
                      "@jiminhofe", "@RonWyden", "@SenJeffMerkley", "@SenToomey", "@SenBobCasey", "@SenJackReed",
                      "@SenWhitehouse", "@SenatorTimScott", "@GrahamBlog", "@SenatorRounds", "@SenJohnThune",
                      "@SenAlexander", "@SenBobCorker", "@SenTedCruz", "@JohnCornyn", "@SenOrrinHatch", "@SenMikeLee",
                      "@SenatorLeahy", "@SenSanders", "@timkaine", "@MarkWarner", "@PattyMurray", "@SenatorCantwell",
                      "@Sen_JoeManchin", "@SenCapito", "@SenatorBaldwin", "@SenRonJohnson", "@SenatorEnzi",
                      "@SenJohnBarrasso"]

    screen_name = us_politicians[25:50]

    begin = strftime("%Y-%m-%d %H:%M:%S", gmtime())
    bg = gmtime()
    print("START TIME: " + begin)
    print("\n")
    count = 0
    for person in screen_name:
        fetchPeople(person, n_of_pages=50)
        count += 1
        print(count)
        print(person)

    end = strftime("%Y-%m-%d %H:%M:%S", gmtime())
    en = gmtime()
    print("\n")
    print("FINISH TIME: " + end)
