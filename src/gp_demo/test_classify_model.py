import joblib
import pandas as pd
from sklearn.cross_validation import train_test_split
from sklearn.metrics import classification_report

csv_path = "/Users/huang/share/data/data_to_train/data.20181124.to_train.ckpt_840.csv"
model_path = "%s.model_rf.pkl" % csv_path
csv_path = "/Users/huang/share/data/data_to_train/data.20181124.to_train.ckpt_810.csv"

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

loaded_clf = joblib.load(model_path)

y_pred = loaded_clf.predict(X_test)

print(classification_report(y_test, y_pred))
