import numpy as np
from sklearn.decomposition import PCA
import pandas as pd
from tools import period_length
from sklearn.cluster import KMeans
from kmodes.kmodes import KModes

input_path = '../../../data/data_cleaned/'

dataframe = pd.read_csv(input_path+'/Articles.csv')

# pca = PCA()
# pca.fit(dataframe)
# variances = pca.explained_variance_ratio_
# print(variances)
# cols = []
# for i in range(len(variances)):
#     if variances[i] < 1e-6:
#         cols.append(i)
# dataframe = dataframe.drop(dataframe.columns[cols], axis=1)

# print("computing K-Modes")
# km = KModes(n_clusters=4, init='Huang', n_init=5, verbose=1)
# clusters = km.fit_predict(dataframe)
# print(clusters)
dummies = []
cols=[]
for i in range(len(dataframe.columns)):
    if dataframe.columns[i]!="Class" and dataframe.columns[i]!="Sub_Department" and dataframe.columns[i]!="Item_Code":
        cols.append(i)
    else:
        dataframe[dataframe.columns[i]] = pd.Categorical(dataframe[dataframe.columns[i]])
        dummies.append(pd.get_dummies(dataframe[dataframe.columns[i]], prefix=dataframe.columns[i]+'_'))
print(cols)
dataframe = dataframe.drop(dataframe.columns[cols], axis=1)

#     dummies.append(pd.get_dummies(dataframe[dataframe.columns[i]], prefix=dataframe.columns[i]+'_'))

result = pd.concat(dummies, axis=1)
print(len(result.columns))
# print("Saving One-Hot-Encoded Articles...")
# result.to_csv(input_path+"hot_encoded_articles.csv", index=False, encoding='utf8')
# print("computing K-Means")
# kmeans = KMeans(n_clusters=100, random_state=0).fit(result)
# print(kmeans.labels_)