from sklearn.ensemble import RandomForestRegressor, RandomForestClassifier, GradientBoostingClassifier
from sklearn.model_selection import train_test_split
import pandas as pd
import pickle
from tools import *
from xgboost import XGBClassifier

def trainRandomForest(input_data, output_data, test_proportion=0.3, maxdepth=1000):
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=test_proportion)
    clf = RandomForestClassifier(max_depth=maxdepth)
    clf.fit(X_train, y_train)
    print("score:", clf.score(X_test, y_test))
    pickle.dump(clf, open(model_filename, 'wb'))
    return clf


def predictDemand(X_test, clf):
    return clf.predict(X_test)

def testRandomForest_on(dirname, test_proportion=0.3, maxdepth=10):
    print("reading csv...")
    dataframe = pd.read_csv(model_input_path+dirname+'/XY.csv')
    X = dataframe.iloc[:, :-1]
    y = dataframe['Y']
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=test_proportion)
    print('Training new random forest on {}'.format(dirname))
    # clf = RandomForestClassifier(max_depth=maxdepth)
    clf = XGBClassifier(silent=False,
                      scale_pos_weight=1,
                      learning_rate=0.01,
                      colsample_bytree = 0.4,
                      subsample = 0.8,
                      objective='binary:logistic',
                      n_estimators=1000,
                      reg_alpha = 0.3,
                      max_depth=4,
                      gamma=10)
    # clf = GradientBoostingClassifier(max_depth=maxdepth)
    clf.fit(X_train[0:100000], y_train[0:100000])

    encoder = pickle.load(open(model_input_path+dirname+'/encoder.sav', 'rb'))

    score = clf.score(X_test, y_test)

    return score

def trainRandomForest_on(dirname, maxdepth=10):
    print("reading csv...")
    dataframe = pd.read_csv(model_input_path+dirname+'/XY.csv')
    X = dataframe.iloc[:, :-1]
    y = dataframe['Y']
    # try:
    #     print('Loading model')
    #     clf = pickle.load(open(model_input_path+dirname+'/RandomForest.sav', 'rb'))
    # except:
    #     print('Failed to load model')
    print('Training new random forest on {}'.format(dirname))
    # clf = RandomForestClassifier(max_depth=maxdepth)
    # clf = GradientBoostingClassifier(max_depth=maxdepth)
    print(X[:10000].values)
    print(y[:10000].values)

    clf = XGBClassifier(silent=False,
                      scale_pos_weight=1,
                      learning_rate=0.01,
                      colsample_bytree = 0.4,
                      subsample = 0.8,
                      objective='binary:logistic',
                      n_estimators=1000,
                      reg_alpha = 0.3,
                      max_depth=4,
                      gamma=10)
    clf.fit(X[:10000].values, y[:10000].values)
        # pickle.dump(clf, open(model_input_path+dirname+'/RandomForest.sav', 'wb'))


    encoder = pickle.load(open(model_input_path+dirname+'/encoder.sav', 'rb'))

    return clf, encoder

if __name__=='__main__':
    score = testRandomForest_on('XY_stockbased_{}'.format(period_length))
    print('Score : {}'.format(score))
