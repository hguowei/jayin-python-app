from pandas import Series

from matplotlib import pyplot

from statsmodels.graphics.tsaplots import plot_acf

#series = Series.from_csv('daily-minimum-temperatures.csv', header=0)
series = Series.from_csv('daily-rainfall-in-melbourne-aust.csv', header=0)

plot_acf(series)

pyplot.show()
