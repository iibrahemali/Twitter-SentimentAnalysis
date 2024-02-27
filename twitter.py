import tweepy
import csv
from textblob import TextBlob
import re

# Replace the placeholder values in the code with your actual Twitter API credentials
consumer_key = 'YOUR_CONSUMER_KEY'
consumer_secret = 'YOUR_CONSUMER_SECRET'
access_token = 'YOUR_ACCESS_TOKEN'
access_token_secret = 'YOUR_ACCESS_TOKEN_SECRET'

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)

api = tweepy.API(auth)

# Replace 'YOUR_SEARCH_QUERY' with the search query you're interested in
search_query = 'YOUR_SEARCH_QUERY'
tweet_count = 100

public_tweets = api.search_tweets(q=search_query, result_type='mixed', count=tweet_count, lang='en', tweet_mode='extended')
public_tweets1 = api.search_tweets(q=search_query, result_type='recent', count=tweet_count, lang='en', tweet_mode='extended')

def clean_tweet(tweet):
    return ' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)", " ", tweet.full_text).split())

with open('tweets.csv', 'w') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(["Tweet", "Sentiment Score", "Subjectivity Score"])
    totalSent = 0
    totalSubj = 0
    count = 0

    for tweet in public_tweets:
        analysis = TextBlob(tweet.full_text)
        score = analysis.sentiment.polarity
        subject = analysis.sentiment.subjectivity
        count += 1
        totalSent += score
        totalSubj += subject
        writer.writerow([clean_tweet(tweet.full_text), score, subject])

    for tweet in public_tweets1:
        analysis = TextBlob(tweet.full_text)
        score = analysis.sentiment.polarity
        subject = analysis.sentiment.subjectivity
        count += 1
        totalSent += score
        totalSubj += subject
        writer.writerow([clean_tweet(tweet.full_text), score, subject])

    if count > 0:
        writer.writerow(['Average Sentiment Score', totalSent/count])
        writer.writerow(['Average Subjectivity Score', totalSubj/count])

print(f"Logged tweeted sentiments of {count} tweets to tweets.csv")
if count > 0:
    print(f"The Average Sentiment Score is {totalSent/count}")
    print(f"The Average Subjectivity Score is {totalSubj/count}")
