"""

first version of pricing estimator

"""

#from fastai.imports import *
#from fastai.structured import *
#from pandas_summary import DataFrameSummary
import pandas as pd
from matplotlib import pyplot as plt
import seaborn as sns
import math
from sklearn.ensemble import RandomForestRegressor
import numpy as np
import scipy
#from IPython.display import display
#from sklearn import metrics
#from sklearn.model_selection import RandomizedSearchCV

df = pd.read_csv("num_items_clean.csv")
print(df.info())

"""
# plot the distribution
plt.figure(figsize=(10, 6))
sns.distplot(df['price'], bins=30)
plt.show()
"""
"""
# Plot the correlation heatmap
plt.figure(figsize=(14, 8))
corr_matrix = df.corr().round(2)
sns.heatmap(data=corr_matrix,cmap='coolwarm',annot=True)
plt.show()
"""


#Scatter plot to observe the correlations between the features that are highly correlated with price
target_var = df['price']
plot1 = plt.figure(1)
plt.scatter(df['words'],target_var)
plt.xlabel('space')
plt.ylabel('words')
plot2 = plt.figure(2)
plt.scatter(df['postID'],target_var)
plt.xlabel('postID')
plt.ylabel('price')
plt.show()


# A function to split our training data into a training set to train our  model and a validations set, which will be used to validate our model.
def split_vals(a,n):
    return a[:n],a[n:]
# Functions that will help us calculate the RMSE and print the score.


def rmse(x,y):
    return math.sqrt(((x-y)**2).mean())


def print_score(m):
    res = [rmse(m.predict(X_train),y_train),rmse(m.predict(X_valid),y_valid),m.score(X_train,y_train),m.score(X_valid,y_valid)]
    if hasattr(m,'oob_score_'):res.append(m.oob_score_)
    print(res)

n_valid = 100
n_train = len(df)-n_valid
X_train, X_valid = split_vals(df.drop('price',axis=1), n_train)
y_train, y_valid = split_vals(df['price'], n_train)
X_test = df

m = RandomForestRegressor(n_jobs=1, oob_score=True)
m.fit(X_train, y_train)
print_score(m)

# check for importance of features

def feat_importance(m,df_train):
    importance = m.feature_importances_
    importance = pd.DataFrame(importance,index=df_train.columns,columns=["Importance"])
    return importance.sort_values(by=['Importance'],ascending=False)

importance = feat_importance(m,X_train)
print(importance[:])

# dependency between features

#Discarding features with feature coefficients less than 0.01
to_keep = importance[importance['Importance'] > 0.01].index
df_raw_train_keep = df_raw_train[to_keep].copy()
df_raw_test_keep = df_raw_test[to_keep].copy()
#Splitting data into training and validation set
X_train, X_valid = split_vals(df_raw_train_keep,n_train)
# Fitting our Random Forest Model after discarding the less important features.

#Dendogram plot
from scipy.cluster import hierarchy as hc
corr = np.round(scipy.stats.spearmanr(df_raw_train_keep).correlation,4)
corr_condensed = hc.distance.squareform(1-corr)
z = hc.linkage(corr_condensed,method='average')
fig = plt.figure(figsize=(16,10))
dendogram = hc.dendrogram(z,labels=df_raw_train_keep.columns,orientation='left',leaf_font_size=16)
plt.show()