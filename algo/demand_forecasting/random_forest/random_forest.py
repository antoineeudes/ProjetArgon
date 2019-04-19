from sklearn.ensemble import RandomForestRegressor, RandomForestClassifier
from sklearn.model_selection import train_test_split
import pandas as pd

def trainRandomForest(input_data, output_data, test_proportion=0.3, maxdepth=1000):
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=test_proportion)
    clf = RandomForestClassifier(max_depth=maxdepth)
    clf.fit(X_train, y_train)
    print("score:", clf.score(X_test, y_test))
    return clf


def predictDemand(X_test, clf):
    return clf.predict(X_test)


if __name__=='__main__':
    print("reading csv...")
    dataframe = pd.read_csv('../../../data/data_cleaned/RandomForest_X.csv')
    X = dataframe.iloc[:, :-1]
    y = dataframe['Y']
    print('training random forest...')
    clf = trainRandomForest(X, y)
    print(clf.predict([[0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,1,105,2017], [0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,1,0,1,192,2017]]))
