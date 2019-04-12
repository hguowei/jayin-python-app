import glob

from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report
from sklearn.model_selection import train_test_split
import pydash

print(__doc__)

import joblib
import pandas as pd


def read_all():
    path = r"/Users/huang/share/data/daily_all_features/"  # use your path
    allFiles = glob.glob(path + "/*.csv")

    list_ = []

    for file_ in allFiles:
        df = pd.read_csv(file_, index_col=None, header=0)
        list_.append(df)

    return pd.concat(list_, axis=0, ignore_index=True)


def read_all2():
    path = r"/Users/huang/share/data/daily_all_features/"  # use your path
    allFiles = glob.glob(path + "/*.csv")

    list_ = []

    # csv_path = "/Users/huang/share/data/daily_all_features/date_20181130.all_features.csv"
    # iris = pd.read_csv(csv_path)
    # list1 = iris.columns.tolist()
    #
    # csv_path = "/Users/huang/share/data/daily_all_features/date_20181129.all_features.csv"
    # csv_path = "/Users/huang/share/data/daily_all_features/date_20181128.all_features.csv"
    # iris = pd.read_csv(csv_path, index_col="id")
    # list2 = iris.columns.tolist()
    #
    # print("xx1", pydash.difference(list1, list2))
    # print("xx1", pydash.difference(list2, list1))
    # exit()
    # iris = pd.read_csv(csv_path)
    for file_ in allFiles:
        try:
            df = pd.read_csv(file_)
        except:
            df = pd.read_csv(file_, index_col="id")
        list_.append(df)

    return pd.concat(list_, axis=0, ignore_index=True)


iris = read_all2()

print("columns", iris.columns.tolist())
iris.drop(["id"], axis=1, inplace=True)

label = "label"
diabetes_y_train = iris[label].values
diabetes_X_train = iris.drop([label], axis=1).values

percentage = 0.01

def map_func(value):
    if value > percentage:
        return 1
    else:
        return 0


diabetes_y_train = pydash.map_(diabetes_y_train, map_func)

X = diabetes_X_train
y = diabetes_y_train

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.33, random_state=42)

clf = RandomForestClassifier()
# clf = AutoSklearnClassifier()
clf.fit(X_train, y_train)

y_pred = clf.predict(X_train)
print(classification_report(y_train, y_pred))

model_path = "test_model.%.2f.pkl" % percentage
# print(clf.feature_importances_)
joblib.dump(clf, model_path)

y_pred = clf.predict(X_test)
print(classification_report(y_test, y_pred))

loaded_clf = joblib.load(model_path)

y_pred = loaded_clf.predict(X_test)
print("Loaded model!")
print(classification_report(y_test, y_pred))
