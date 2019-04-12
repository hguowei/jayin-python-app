from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report
from sklearn.model_selection import train_test_split

print(__doc__)


import joblib
import pandas as pd

csv_path = "/Users/huang/share/data/daily_all_features/date_20181129.all_features.csv"
iris = pd.read_csv(csv_path, index_col="id")
print("columns", iris.columns.tolist())
# iris.drop(["id"], axis=1, inplace=True)

label = "label"
diabetes_y_train = iris[label].values
diabetes_X_train = iris.drop([label], axis=1).values
import pydash


def map_func(value):
    if value > 0.000000001:
        return 1
    else:
        return 0


diabetes_y_train = pydash.map_(diabetes_y_train, map_func)

X = diabetes_X_train
y = diabetes_y_train

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.33, random_state=42)

clf = RandomForestClassifier()
clf.fit(X_train, y_train)

y_pred = clf.predict(X_train)
print(classification_report(y_train, y_pred))

model_path = "test_model.pkl"
# print(clf.feature_importances_)
joblib.dump(clf, model_path)


y_pred = clf.predict(X_test)
print(classification_report(y_test, y_pred))

loaded_clf = joblib.load(model_path)

y_pred = loaded_clf.predict(X_test)
print("Loaded model!")
print(classification_report(y_test, y_pred))
