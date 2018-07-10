
# coding: utf-8

# In[1]:


####Import Libraries

import pandas as pd
import numpy as np
import tweepy
import requests
import matplotlib.pyplot as plt
import json
import re


# In[12]:


#### Gather


# In[2]:


# Using Requests library to download a file then store it in a tsv file
url = 'https://d17h27t6h515a5.cloudfront.net/topher/2017/August/599fd2ad_image-predictions/image-predictions.tsv'
response = requests.get(url)

with open('image_predictions.tsv', 'wb') as file:
    file.write(response.content)

# Read the downloaded file into a dataframe 'image_predictions'
image_predictions = pd.read_csv('image_predictions.tsv', sep = '\t', encoding = 'utf-8')


# In[3]:


#test
image_predictions


# In[4]:


# Read in csv file as a Pandas DataFrame
archive = pd.read_csv('twitter-archive-enhanced.csv')
archive.head(1)


# In[6]:


# Obtain API keys, secrets, and tokens my twitter account 
consumer_key = 'zKz1KdbaKvReJHc5qGlnHqGHT '
consumer_secret = 'jNPkQ0TcVPuGbLf9pA1zWR46XGtKxRi35FmLhd7EQpPCtmiBPh'
access_token = '84074990-hO6Z3Tg0aPlS5CZxov9ImSbLWf5HB6Rii6QADcqLD'
access_secret = '5xeboab06kBXNyOnFTTy3eurPYdBz8zjvVADczZgPcULv'

# Tweepy query variables as shown in the example
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_secret)
api = tweepy.API(auth, 
                 parser = tweepy.parsers.JSONParser(), # Parse the result to Json Object
                 wait_on_rate_limit = True, # Automatically wait for rate limits to replenish
                 wait_on_rate_limit_notify = True) # Print a notification when Tweepy is waiting for rate limits to replenish


# In[8]:


# Liste where we will store the dictionaries of our result
df_list = []
# Liste frame where we will store the tweet_id of the errors
error_list = []


# Get the tweet object for all the teweets in archive dataframe 
for tweet_id in archive['tweet_id']:
    try:
        page = api.get_status(tweet_id, tweet_mode = 'extended')
        # Print one page to look at the structure of the returned file
        # and the names of attributes
        # print(json.dumps(page, indent = 4))
        #break
        
        favorites = page['favorite_count'] # How many favorites the tweet had
        retweets = page['retweet_count'] # Count of the retweet
        user_followers = page['user']['followers_count'] # How many followers the user had
        user_favourites = page['user']['favourites_count'] # How many favorites the user had
        date_time = page['created_at'] # The date and time of the creation
        
        df_list.append({'tweet_id': int(tweet_id),
                        'favorites': int(favorites),
                        'retweets': int(retweets),
                        'user_followers': int(user_followers),
                        'user_favourites': int(user_favourites),
                        'date_time': pd.to_datetime(date_time)})
        # Catch the exceptions of the TweepError
    except Exception as e:
        print(str(tweet_id)+ " _ " + str(e))
        error_list.append(tweet_id)


# In[9]:


# lengh of the result
print("The lengh of the result", len(df_list))
# The tweet_id of the errors
print("The lengh of the errors", len(error_list))

