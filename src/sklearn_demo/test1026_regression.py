from sklearn.cross_validation import train_test_split
from sklearn.ensemble import RandomForestClassifier

print(__doc__)

# Code source: Jaques Grobler
# License: BSD 3 clause


import matplotlib.pyplot as plt
import numpy as np
from sklearn import datasets, linear_model
from sklearn.metrics import mean_squared_error, r2_score

import pandas as pd

csv_path = "/Users/huang/workjayin/jayin-python-app/src/sklearn_demo/data.18.20181117.to_train.csv"
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
exit()
# Create linear regression object
regr = linear_model.LinearRegression()

# Train the model using the training sets
regr.fit(diabetes_X_train, diabetes_y_train)

# Make predictions using the testing set
diabetes_y_pred = regr.predict(diabetes_X_train)

# The coefficients
print('Coefficients: \n', regr.coef_)
# The mean squared error


print("XXX", diabetes_y_pred.shape)
print("Mean squared error: %.2f"
      % mean_squared_error(diabetes_y_train, diabetes_y_pred))
# Explained variance score: 1 is perfect prediction
print('Variance score: %.2f' % r2_score(diabetes_y_train, diabetes_y_pred))

# Plot outputs
# plt.scatter(diabetes_X_test, diabetes_y_train, color='black')
# plt.plot(diabetes_X_test, diabetes_y_pred, color='blue', linewidth=3)
#
# plt.xticks(())
# plt.yticks(())
#
# plt.show()
