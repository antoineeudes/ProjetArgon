from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split

def trainRandomForest(input_data, output_data, test_proportion=0.4, maxdepth=1000):
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=test_proportion)
    clf = RandomForestRegressor(max_depth=max_depth)
    clf.fit(X_train, y_train)
    return clf


def predictDemand(X_test, clf):
    return clf.predict(X_test)