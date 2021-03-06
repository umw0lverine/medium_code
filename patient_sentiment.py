#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Nov 24 20:34:49 2019

@author: sadrachpierre
"""


import tweepy
from textblob import TextBlob
import seaborn as sns
import matplotlib.pyplot as plt 

consumer_key = 'abc123'
consumer_secret = 'abc123'
access_token = 'abc123-abc123'
access_token_secret = 'abc123'


auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)

api = tweepy.API(auth)



import pandas as pd  
pd.set_option('display.max_rows', 10000000)
pd.set_option('display.max_columns', 1000000)

def get_related_tweets(key_word):

    twitter_users = []
    tweet_time = []
    tweet_string = [] 
    for tweet in tweepy.Cursor(api.search,q=key_word, count=1000).items(1000):
            if (not tweet.retweeted) and ('RT @' not in tweet.text):
                if tweet.lang == "en":
                    twitter_users.append(tweet.user.name)
                    tweet_time.append(tweet.created_at)
                    tweet_string.append(tweet.text)
                    #print([tweet.user.name,tweet.created_at,tweet.text])
    df = pd.DataFrame({'name':twitter_users, 'time': tweet_time, 'tweet': tweet_string})
    
    return df 





def get_sentiment(key_word):
    
    df = get_related_tweets(key_word)
    df['sentiment'] = df['tweet'].apply(lambda tweet: TextBlob(tweet).sentiment.polarity)
    df_pos = df[df['sentiment'] > 0.0]
    df_neg = df[df['sentiment'] < 0.0]
    print("Number of Positive Tweets about {}".format(key_word), len(df_pos))
    print("Number of Negative Tweets about {}".format(key_word), len(df_neg))
    sns.set()
    labels = ['Postive', 'Negative']
    heights = [len(df_pos), len(df_neg)]
    plt.bar(labels, heights, color = 'navy')
    plt.title(key_word)


get_sentiment("Metformin")    
get_sentiment("Lipitor")    
get_sentiment("Vicodin")    
get_sentiment("Simvastatin") 
get_sentiment("Lisinopril") 
