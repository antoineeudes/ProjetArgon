import numpy as np
from sklearn.decomposition import PCA

dataframe = pd.read_csv(input_path+dirname+'/XY.csv')
    X = dataframe.iloc[:, :-1]