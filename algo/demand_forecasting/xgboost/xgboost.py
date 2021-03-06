from sklearn.model_selection import train_test_split
import pandas as pd
import pickle
from tools import *

def trainXGB(input_data, output_data, test_proportion=0.3, maxdepth=1000):
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=test_proportion)
    clf = XGBClassifier(max_depth=maxdepth)
    clf.fit(X_train, y_train)
    print("score:", clf.score(X_test, y_test))
    pickle.dump(clf, open(model_filename, 'wb'))
    return clf


def predictDemand(X_test, clf):
    return clf.predict(X_test)

def testXGB_on(dirname, test_proportion=0.3, maxdepth=1000):
    print("reading csv...")
    dataframe = pd.read_csv(model_input_path+dirname+'/XY.csv')
    X = dataframe.iloc[:, :-1]
    y = dataframe['Y']
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=test_proportion)
    print('Training new random forest on {}'.format(dirname))
    clf = XGBClassifier(max_depth=maxdepth)
    clf.fit(X_train, y_train)

    encoder = pickle.load(open(model_input_path+dirname+'/encoder.sav', 'rb'))

    score = clf.score(X_test, y_test)

    return score

def trainXGB_on(dirname, maxdepth=1000):
    print("reading csv...")
    dataframe = pd.read_csv(model_input_path+dirname+'/XY.csv')
    X = dataframe.iloc[:, :-1]
    y = dataframe['Y']
    try:
        print('Loading model')
        clf = pickle.load(open(model_input_path+dirname+'/XGBoost.sav', 'rb'))
    except:
        print('Failed to load model')
    print('Training new random forest on {}'.format(dirname))
    clf = XGBClassifier(max_depth=maxdepth)
    clf.fit(X, y)
    pickle.dump(clf, open(model_input_path+dirname+'/XGBoost.sav', 'wb'))


    encoder = pickle.load(open(model_input_path+dirname+'/encoder.sav', 'rb'))

    return clf, encoder

if __name__=='__main__':
    clf, encoder = testXGB_on('XY_stockbased_{}'.format(period_length))
