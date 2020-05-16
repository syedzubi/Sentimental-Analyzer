
# Create your views here.
from django.shortcuts import render
import os
import csv
import tweepy, datetime
from textblob import TextBlob
import time
import re
import pandas as pd
import nltk
from nltk.stem.porter import *
from wordcloud import WordCloud, STOPWORDS
import matplotlib.pyplot as plt
import seaborn as sns
import requests
import warnings
import json
import numpy as np
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from googletrans import Translator

import sys
import tweepy
import csv
import pandas as pd

def sentiment_analyzer_scores(text):
    analyser = SentimentIntensityAnalyzer()
    score = analyser.polarity_scores(text)
    # translator = Translator()
    lb = score['compound']
    if lb >= 0.05:
        return 1
    elif (lb > -0.05) and (lb < 0.05):
        return 0
    else:
        return -1

def get_sentiment_class(text):
    score = sentiment_analyzer_scores(text)
    sentiment_class = "neutral"
    if(score == 1):
        sentiment_class = "positive"
    elif(score == -1):
        sentiment_class = "negative"

    return sentiment_class


def remove_pattern(input_txt, pattern):
    r = re.findall(pattern, input_txt)
    for i in r:
        input_txt = re.sub(i, '', input_txt)
    return input_txt

def clean_tweets(lst):
    # remove twitter Return handles (RT @xxx:)
    lst = np.vectorize(remove_pattern)(lst, "RT @[\w]*:")
    # remove twitter handles (@xxx)
    lst = np.vectorize(remove_pattern)(lst, "@[\w]*")
    # remove URL links (httpxxx)
    lst = np.vectorize(remove_pattern)(lst, "https?://[A-Za-z0-9./]*")
    # remove special characters, numbers, punctuations (except for #)
    lst = np.core.defchararray.replace(lst, "[^a-zA-Z#]", " ")
    # remove extra spaces
    lst = np.core.defchararray.replace(lst, "[\s]+", " ")
    # replace \n with space
    lst = np.core.defchararray.replace(lst, "\n", " ")

    return lst


def assign_sentiments(filteredTweets):
    sentiments = []
    for tweet in filteredTweets:
        senti = {}
        sentiment_class = get_sentiment_class(tweet)
        senti["sentiment"] = sentiment_class
        senti["tweet"] = tweet
        sentiments.append(senti)

    return sentiments

def fetch_tweets(keyword):
    # Credentials
    consumer_key = "y8N01iTXrbcaVyPfzDwnjpoA7"
    consumer_secret = "NCIxq1KnzQ4T2OodopMp7cXVvdMpylv5sXZLO1IhRfP6UAd6bK"
    access_token = "720135280540291076-OiU7CUNKpGzo1k4PsNpDcebVDdifpfx"
    access_token_secret = "T6S59ChbUoYZxZO9GxgN9dnen7HG90WQinSJt3obWRBtg"

    # Authenticating
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    api = tweepy.API(auth)

    count = 50
    tweetsSearchResults = api.search(keyword, count = 50)
    filteredTweets = []
    for tweet in tweetsSearchResults:
        unFilteredTweet = tweet.text
        print("Tweet is :", tweet.text)
        filteredList = clean_tweets([unFilteredTweet])
        filteredTweets.append(filteredList[0])

    write_tweets_in_file(filteredTweets)
    print("k=>",keyword)

def write_tweets_in_file(filteredTweets):
    positive_tweets = []
    negative_tweets = []
    neutral_tweets = []

    sentimentsDict = assign_sentiments(filteredTweets)
    for sentimentObj in sentimentsDict:
        # print ("sentimentObj:", sentimentObj)
        if(sentimentObj["sentiment"] == "positive"):
            positive_tweets.append(sentimentObj["tweet"])
        elif(sentimentObj["sentiment"] == "negative"):
            negative_tweets.append(sentimentObj["tweet"])
        else:
            neutral_tweets.append(sentimentObj["tweet"])

    df1 = pd.DataFrame({"S No": list(range(1, len(positive_tweets) + 1)), "Tweets": positive_tweets, "Sentiments": ["positive"] * len(positive_tweets)})
    df2 = pd.DataFrame({"S No": list(range(1, len(negative_tweets) + 1)), "Tweets": negative_tweets, "Sentiments": ["positive"] * len(negative_tweets)})
    df3 = pd.DataFrame({"S No": list(range(1, len(neutral_tweets) + 1)), "Tweets": neutral_tweets, "Sentiments": ["positive"] * len(neutral_tweets)})

    df1.to_csv('Analysis/Positive.csv', index=False)
    df2.to_csv('Analysis/Negative.csv', index=False)
    df3.to_csv('Analysis/Neutral.csv', index=False)


#for both new and old positive and negative count
positiveCountArr =  [0]
negativeCountArr = [0]
neutralCounterArr = [0]


def index(request):
    return  render(request, 'user_interface.html')

def getIndex(request):
    index = request.POST.get('index')
    keyword = request.POST.get('searchValue')
    fetch_tweets(keyword)
    MEDIA = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    FILE_NAME = os.path.join(MEDIA,'Analysis')
    positiveFileName = os.path.join(FILE_NAME,'Positive.csv')
    negativeFileName = os.path.join(FILE_NAME,'Negative.csv')
    neutralFileName = os.path.join(FILE_NAME,'Neutral.csv')

    countArray = [] #for new count will contain positive and negative both
    positiveRows = [] #for rows
    negativeRows = [] #for rows
    neutralRows=[]

    # positive csv fetch
    with open(positiveFileName,encoding='utf-8') as csvfile:
        csvreader = csv.reader(csvfile)
        for row in csvreader:
            positiveRows.append(row)
        positiveCount = csvreader.line_num
        positiveCountArr.append(positiveCount)
        countArray.append(positiveCount)

    #negative csv fetch
    with open(negativeFileName,encoding='utf-8') as csvfile:
        csvreader = csv.reader(csvfile)
        for row in csvreader:
            negativeRows.append(row)
        negativeCount = csvreader.line_num
        negativeCountArr.append(negativeCount)
        countArray.append(negativeCount)

    with open(neutralFileName,encoding='utf-8') as csvfile:
        csvreader = csv.reader(csvfile)
        for row in csvreader:
            neutralRows.append(row)
        neutralCount = csvreader.line_num
        neutralCounterArr.append(neutralCount)
        countArray.append(neutralCount)

    if(len(positiveCountArr) > 8):
       del positiveCountArr[1]

    if(len(negativeCountArr) > 8):
        del negativeCountArr[1]

    if(len(neutralCounterArr) > 8):
        del neutralCounterArr[1]

    return  render(request, 'getIndex.html',{'temp':countArray,'positiveCountArr':positiveCountArr,'negativeCountArr':negativeCountArr,'index':index})
