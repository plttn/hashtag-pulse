import austin_oauth
import json
from tweepy import API
from tweepy import Stream
from tweepy import OAuthHandler
from tweepy.streaming import StreamListener
import TweetClassifier2 as tc
import csv
import re
import cPickle

clf_file = open('tweet_classifier_small.pickle','rb')
classifierObj = cPickle.load(clf_file)
clf_file.close()



def ratioCalc(emotion, emotionList):
    emotionList[emotion] += 1
    return emotionList

class listener(StreamListener):
    tweetTotal = 0
    emotionList = {'0':0, '2':0, '4':0}

    def on_status(self, data):
        j = data._json
        if j['lang'] == 'en':
            tweetData = tc.strip_punctuation(data.text)
            emotion =  classifierInstance.classify(classifierObj.extract_features(tweetData.split()))
            self.tweetTotal += 1
            self.emotionList = ratioCalc(emotion, self.emotionList)
            emotionList = map(lambda x: float(x)/self.tweetTotal,self.emotionList)
            
            print emotion, self.tweetTotal, emotionList, tweetData, "\n"
        return(True)

    def on_error(self, status):
        if status == 401:
            print "make sure VM and host clock are in sync"
        else:
            print status


oauth = austin_oauth.getOAuth()

classifierInstance = classifierObj.getClassifier()

musicianStream = Stream(oauth, listener()) #sets up listener
musicianStream.filter(track=['@warriors','@spurs','@okcthunder','@trailblazers'])
#musicianStream.sample()

#musicianStream.disconnect() to close stream
