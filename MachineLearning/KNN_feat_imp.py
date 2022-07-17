from numpy import mean
from numpy import std
from numpy import absolute
import matplotlib.pyplot as plt
from pandas import read_csv
import pandas as pd
from sklearn.model_selection import cross_val_score
from sklearn.model_selection import train_test_split
import numpy as np
from sklearn.model_selection import RepeatedKFold
from sklearn.linear_model import Lasso
from sklearn.linear_model import LinearRegression
from sklearn.linear_model import Ridge
from sklearn.neighbors import KNeighborsRegressor
from sklearn.model_selection import GridSearchCV
from IPython.display import display
from sklearn.metrics import confusion_matrix
from sklearn.metrics import plot_confusion_matrix


"""
params = {'n_neighbors':[2,3,4,5,6,7,8,9]}

model = GridSearchCV(knn, params, cv=5)
model.fit(x_train,y_train)
model.best_params_
""" 

# load the dataset
#df = read_csv("C:/Users/PC/Desktop/die.csv")
df = read_csv("C:/Users/PC/Desktop/die.csv")

graph = "Hits"

df[graph] = pd.to_numeric(df[graph], downcast="float")
df["tweet"] = pd.to_numeric(df["tweet"], downcast="float")
df["sent"] = pd.to_numeric(df["sent"], downcast="float")
df["rt"] = pd.to_numeric(df["rt"], downcast="float")
df["fav"] = pd.to_numeric(df["fav"], downcast="float")
df["rep"] = pd.to_numeric(df["rep"], downcast="float")
df = df.drop(["Name"], axis = 1)

dep_var = "rep"
cond = np.random.rand(len(df))>.2
train = np.where(cond)[0]
valid = np.where(~cond)[0]

train_df = df.iloc[train]
valid_df = df.iloc[valid]

train_y = train_df["rep"]
train_xs = train_df.drop(["rep"], axis = 1)

valid_y = valid_df["rep"]
valid_xs = valid_df.drop(["rep"], axis = 1)

m = KNeighborsRegressor()

m = m.fit(train_xs, train_y)

std_score = m.score(valid_xs, valid_y)
#print(std_score)

#data = {"Hits":[0], "tweet":[0], "sent":[0], "rt":[0], "fav":[0], "rep":[0]}
data = {graph:[0], "tweet":[0], "sent":[0], "rt":[0], "f-av":[0], "rep":[0]}
feat_imp = pd.DataFrame(data)
#print(feat_imp.head())

valid_SL = valid_xs.copy()
#valid_SL["Hits"] = np.random.permutation(valid_SL["Hits"])
#feat_imp["Hits"] = std_score - m.score(valid_SL, valid_y)
valid_SL[graph] = np.random.permutation(valid_SL[graph])
feat_imp[graph] = std_score - m.score(valid_SL, valid_y)

valid_SW = valid_xs.copy()
valid_SW["tweet"] = np.random.permutation(valid_SW["tweet"])
feat_imp["tweet"] = std_score - m.score(valid_SW, valid_y)

valid_PL = valid_xs.copy()
valid_PL["sent"] = np.random.permutation(valid_PL["sent"])
#print(m.score(valid_PL, valid_y))
feat_imp["sent"] = std_score - m.score(valid_PL, valid_y)

valid_PW = valid_xs.copy()
valid_PW["rt"] = np.random.permutation(valid_PW["rt"])
feat_imp["rt"] = std_score - m.score(valid_PW, valid_y)

valid_PQ = valid_xs.copy()
valid_PQ["rt"] = np.random.permutation(valid_PQ["rt"])
feat_imp["rt"] = std_score - m.score(valid_PQ, valid_y)

valid_PF = valid_xs.copy()
valid_PF["fav"] = np.random.permutation(valid_PF["fav"])
feat_imp["fav"] = std_score - m.score(valid_PF, valid_y)

#print(feat_imp["Hits"], feat_imp["tweet"], feat_imp["sent"],
#      feat_imp["rt"], feat_imp["fav"])
print(feat_imp[graph], feat_imp["tweet"], feat_imp["sent"],
      feat_imp["rt"], feat_imp["fav"])

print(std_score)
