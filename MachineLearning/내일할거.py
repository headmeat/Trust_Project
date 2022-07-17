import csv, re, numpy as np, time, sys, nltk, string
import pandas as pd
from nltk.corpus import stopwords
from collections import defaultdict
from nltk.stem import WordNetLemmatizer
import time

lemmatizer = WordNetLemmatizer()

emoji_pattern = re.compile("["
        u"\U0001F600-\U0001F64F"  # emoticons
        u"\U0001F300-\U0001F5FF"  # symbols & pictographs
        u"\U0001F680-\U0001F6FF"  # transport & map symbols
        u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
                           "]+", flags=re.UNICODE)
users = dict()
tweets = dict()

a = 'utf-8'
aa = 'windows-1252'

c = 0

def cleanse(row): #lemmatization 및 cleaning
    tweet = ' '.join([lemmatizer.lemmatize(w) for w in nltk.word_tokenize(row)])                        
    tweet = emoji_pattern.sub(r'', tweet)        
    tweet = tweet.lower()
    tweet = tweet.replace("-\n", "")
    tweet = re.sub('@[^\s]+','',tweet)
    tweet = tweet.replace('님에게 보내는 답글', '')
    tweet = tweet.replace('트윗 인용하기', '')
    tweet = tweet.replace('답글', '')
    tweet = tweet.replace('\n', ' ')
    tweet = re.sub(r"\d+", " ", tweet)
    tweet = re.sub(r'http\S+', '', tweet)
    tweet = re.sub(r"[^\w+#]", " ", tweet)
    tweet = ' '.join([w for w in tweet.split() if len(w)>3])
    return re.sub("ct", "t", tweet)

noen = dict()
start = time.time()

with open('C:/Users/PC/Desktop/save.csv', 'w', newline='', encoding=a) as f:
    writer = csv.writer(f)
    with open('C:/Users/PC/Desktop/tweets/combined_csv_bro.csv', 'r', encoding=a) as file:
        reader = csv.reader(file)
        
        for row in reader:
            if c == 0:
                c+=1
                continue
            
            c+=1
            
            if c % 10000 == 0: print(c)
            
            if len(cleanse(row[3])) > 0: writer.writerow(row)
        
print(time.time()-start)
