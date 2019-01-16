import gensim
import tweepy
from tweepy import Stream
from tweepy.streaming import StreamListener
import json
import time
import re
from nltk.corpus import stopwords
import nltk
''' Matching ML Model Making with Tweepy for Twitter Data '''
''' Make Model with This to Use in views.matching for debate matching '''

nltk.download('stopwords')
stops = stopwords.words('english')
noisewords = ['@', 'rt', 'the', 'we', 'a', 'that', 'it', 'and', 'you']
stops.extend(noisewords)


def prepare_data(s):
    pattern = re.compile(r'\b(' + r'|'.join(stops) + r')\b\s*')
    for word in s:
        if pattern.match(word):
            s.remove(word)


# streamer for tweepy data, has time limit for training for each keyword
class Listener(StreamListener):

    def __init__(self, time_limit=60):
        self.start_time = time.time()
        self.limit = time_limit
        super(Listener, self).__init__()

    # on data received, get text from json data tweepy returns, append to sentences list
    def on_data(self, data):
        if (time.time() - self.start_time) < self.limit:
            json_load = json.loads(data)
            texts = json_load['text']
            coded = texts.encode('utf-8')
            s = str(coded)
            s = s[2:-1]
            sentences.append(s)
            return True
        # after time limit exceeded, streaming for keyword done, fix data for word2vec
        else:
            for s in sentences:
                s = s.lower()
                s = s.split()
                prepare_data(s)
                fixed_data.append(s)
            print(fixed_data)
            return False

    def on_error(self, status_code):
        print('error code:', status_code)


if __name__ == "__main__":
    auth = tweepy.OAuthHandler('SnsHkP192Jac6s8Da2AEBZabs' , '3zWgrqbYBPjbo0Fethe7PnhItLwFJDlTt9ia40Wac0jhCJiasW')
    auth.set_access_token('4910145663-br9JBO0fGQdiSYKXYx2lWWCfAbTCYpHVI50oKBW', 'LAiMxilFzO1mwgCvuvFrDakzSM3rojkLvJqqexbR6Yi08')
    api = tweepy.API(auth)
    fixed_data = []
    # keywords for training
    key_words = ['politics']
    for word in key_words:
        sentences = []
        stream = Stream(auth, listener=Listener(time_limit=10))
        stream.filter(track=[word])

model = gensim.models.Word2Vec(fixed_data)
# save model here




