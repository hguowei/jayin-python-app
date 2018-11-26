from sklearn.cross_validation import train_test_split
from sklearn.ensemble import RandomForestClassifier

print(__doc__)

# Code source: Jaques Grobler
# License: BSD 3 clause


import pandas as pd

csv_path = "/Users/huang/share/data/gp_data/data.20181124.to_train.ckpt_180.csv"
iris = pd.read_csv(csv_path)

label = "label"
diabetes_y_train = iris[label].values
diabetes_X_train = iris.drop([label], axis=1).values
import pydash


def map_func(value):
    if value > 0.01:
        return 1
    else:
        return 0


diabetes_y_train = pydash.map_(diabetes_y_train, map_func)

X = diabetes_X_train
y = diabetes_y_train

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.33, random_state=42)

clf = RandomForestClassifier(n_estimators=100, max_depth=2,
                             random_state=0)
clf.fit(X_train, y_train)

# print(clf.feature_importances_)

from sklearn.metrics import classification_report

y_pred = clf.predict(X_test)

print(classification_report(y_test, y_pred))
