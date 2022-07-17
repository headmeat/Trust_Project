import csv, re, numpy as np, time, sys, nltk, string
import pandas as pd
from nltk.corpus import stopwords
from collections import defaultdict
from nltk.stem import WordNetLemmatizer

lemmatizer = WordNetLemmatizer()

emoji_pattern = re.compile("["
        u"\U0001F600-\U0001F64F"  # emoticons
        u"\U0001F300-\U0001F5FF"  # symbols & pictographs
        u"\U0001F680-\U0001F6FF"  # transport & map symbols
        u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
                           "]+", flags=re.UNICODE)

from collections import Counter
 
def most_frequent(List):
    occurence_count = Counter(List)
    return occurence_count.most_common(1)[0][0]

def cleanse(tweet): #lemmatization 및 cleaning
    tweet = ' '.join([lemmatizer.lemmatize(w) for w in nltk.word_tokenize(tweet)])                        
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

start = time.time()
pd.set_option('display.max_columns', None)

active = dict()
origin = dict()


df = pd.read_csv('C:/Users/PC/Desktop/tweets_java2.csv', encoding='UTF-8')
print(len(df), 'tweets')

for index, row in df.iterrows():
    active[row['userId']] = set()
    origin[row['userId']] = [0, 0]

for index, row in df.iterrows():
    active[row['userId']].add(row['created_at'].split("T")[0])
    if 'RT @' in row['text']: origin[row['userId']][1] += 1
    else: 
        origin[row['userId']][0] += 1
        origin[row['userId']][1] += 1

for key in active.keys():
    active[key] = len(active[key])/90 #이시점 activeness 계산 완료. 90을 실제 수집된 날짜로 수정할 것.
    origin[key] = origin[key][0]/origin[key][1] #이시점 originality 계산 완료

df=df.loc[:,['userId', 'created_at', 'text']]

df['text'] = pd.DataFrame(df.text.apply(lambda x: cleanse(x)))

from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer
from sklearn.decomposition import LatentDirichletAllocation

vectorizer = CountVectorizer(
analyzer='word',       
min_df=3,# minimum required occurences of a word 
stop_words='english',# remove stop words
lowercase=True,# convert all words to lowercase
token_pattern='[a-zA-Z0-9]{3,}',# num chars > 3
max_features=5000,# max number of unique words
                            )
data_matrix = vectorizer.fit_transform(df.text)

lda_model = LatentDirichletAllocation(
n_components=8, # Number of topics
learning_method='online',
random_state=20,       
n_jobs = -1  # Use all available CPUs
                                     )

lda_output = lda_model.fit_transform(data_matrix)

#print(lda_output)
#print(np.argmax(lda_output, axis=1))
df['topics'] = np.argmax(lda_output, axis=1)

topic_no = dict()

df = df.groupby('userId')['topics'].apply(list).to_frame()

topics = dict()

for index, row in df.iterrows():
    topic_no[index] = most_frequent(row[0])
    topics[index] = row[0].count(most_frequent(row[0]))/len(row[0]) #이시점 focus rate 계산 완료

with open('results.csv', 'w', encoding='UTF8', newline='') as f:
    writer = csv.writer(f)
    writer.writerow(['id', 'topics','active','origin'])
    
    for key in topics.keys():
        writer.writerow([key, topic_no[key], topics[key],active[key],origin[key]])

print(topics, active, origin)

print(time.time()-start)
