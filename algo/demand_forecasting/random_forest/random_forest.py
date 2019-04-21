from sklearn.ensemble import RandomForestRegressor, RandomForestClassifier
from sklearn.model_selection import train_test_split
import pandas as pd
import pickle

model_filename = 'randomforest_model.sav'
input_path = '../../../data/data_cleaned/'

def trainRandomForest(input_data, output_data, test_proportion=0.3, maxdepth=1000):
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=test_proportion)
    clf = RandomForestClassifier(max_depth=maxdepth)
    clf.fit(X_train, y_train)
    print("score:", clf.score(X_test, y_test))
    pickle.dump(clf, open(model_filename, 'wb'))
    return clf


def predictDemand(X_test, clf):
    return clf.predict(X_test)

def trainRandomForest_on(filename, test_proportion=0.3, maxdepth=1000):
    print("reading csv...")
    dataframe = pd.read_csv(input_path+filename)
    X = dataframe.iloc[:, :-1]
    y = dataframe['Y']
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=test_proportion)
    try:
        print('Loading model')
        clf = pickle.load(open('randomforest_trained_on_'+filename, 'rb'))
    except:
        print('Failed to load model')
        print('Training new random forest on {}'.format(filename))
        clf = RandomForestClassifier(max_depth=maxdepth)
        clf.fit(X_train, y_train)
        pickle.dump(clf, open('randomforest_trained_on_'+filename, 'wb'))

    print("score:", clf.score(X_test, y_test))

    return clf

if __name__=='__main__':
    # print("reading csv...")
    # dataframe = pd.read_csv('../../../data/data_cleaned/XY_7.csv')
    # X = dataframe.iloc[:, :-1]
    # y = dataframe['Y']
    # try:
    #     print('loading moel')
    #     clf = pickle.load(open(model_filename, 'rb'))
    # except:
    #     print('training random forest...')
    #     clf = trainRandomForest(X, y)
    # clf.score()
    # print(clf.predict([[0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,1,105,2017], [0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,1,0,1,192,2017]]))
    clf = trainRandomForest_on('XY_stockbased_7.csv')
    # print("score:", clf.score(X_test, y_test))
