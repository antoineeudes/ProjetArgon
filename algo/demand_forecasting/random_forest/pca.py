import numpy as np
from sklearn.decomposition import PCA
import pandas as pd
from tools import period_length

input_path = '../../../data/data_cleaned/'
model_input_path = '../../../data/data_cleaned/input/'
output_path = '../../../data/data_cleaned/input/'
dirname = 'XY_sockbased_{}'.format(period_length)
try:
    os.mkdir(output_path)
except:
    pass

dataframe = pd.read_csv(input_path+dirname+'/XY.csv')
X = dataframe.iloc[:, :-1]


pca = PCA()
pca.fit(X)
print(pca.explained_variance_ratio_) 