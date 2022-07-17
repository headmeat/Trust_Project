from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn import metrics
from joblib import dump, load
import pandas as pd, pickle
from sklearn.model_selection import train_test_split
dataset = pd.read_csv('C:/Users/headm/OneDrive/Desktop/csv/main.csv',encoding='iso-8859-1')
print("########## File read ##########\n")
tweets = dataset["tweet_text"].values
classes = dataset["sentiment"].values

X_train, X_test, y_train, y_test = train_test_split(tweets, classes, test_size=0.3, random_state=42)
vectorizer = CountVectorizer(analyzer = "word", tokenizer = None, preprocessor = None, max_features = 5000)
train_data_features = vectorizer.fit_transform(X_train)
test_data_features = vectorizer.transform(X_test)

model = MultinomialNB()
model.fit(train_data_features, y_train)

#MNBpredict = model.predict(test_data_features)
test = ['Acho que devo um agradecimento a você, senhor, por escrever este lindo livro e inspirar minha vida de uma forma tão positiva.', 'Essa é uma situação ridícula. ', 'eu perdi tudo ']
#X = vectorizer.transform(test)
#MNBpredict = model.predict(X)
#print(MNBpredict)

#print("Accuracy: {0:.2f}%".format(metrics.accuracy_score(y_test, MNBpredict)*100))

dump(model, 'model.joblib')
with open('vectorizer.pkl', 'wb') as fw:
        pickle.dump(vectorizer.vocabulary_, fw)
        
        
vec = CountVectorizer(decode_error = "replace", vocabulary = pickle.load(open('vectorizer.pkl', "rb")))
model = load('model.joblib')
