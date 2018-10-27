"""
An example for the usage of SMAC within Python.
We optimize a simple SVM on the IRIS-benchmark.

Note: SMAC-documentation uses linenumbers to generate docs from this file.
"""

import logging
import numpy as np
from sklearn import svm, datasets
from sklearn.model_selection import cross_val_score

# Import ConfigSpace and different types of parameters
from smac.configspace import ConfigurationSpace
from ConfigSpace.hyperparameters import CategoricalHyperparameter, \
    UniformFloatHyperparameter, UniformIntegerHyperparameter
from ConfigSpace.conditions import InCondition
import pydash
# Import SMAC-utilities
from smac.tae.execute_func import ExecuteTAFuncDict
from smac.scenario.scenario import Scenario
from smac.facade.smac_facade import SMAC

import warnings
import itertools
import pandas as pd
import numpy as np
import statsmodels.api as sm
import matplotlib.pyplot as plt
# 基础库导入

import warnings

warnings.filterwarnings('ignore')
warnings.simplefilter('ignore')

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

import os
import sys

# 使用insert 0即只使用github，避免交叉使用了pip安装的abupy，导致的版本不一致问题
sys.path.insert(0, os.path.abspath('../'))
import abupy

plt.style.use('fivethirtyeight')

# We load the iris-dataset (a widely used benchmark)


# df = pd.read_csv("../../data/monthly-milk-production-pounds-p.csv", index_col='Month')
# print("df", df.head())
# print(df.columns)
# y = df
abupy.env.disable_example_env_ipython()
from abupy import abu, ml, nd, tl, pd_resample, AbuML, AbuMLPd, AbuMetricsBase
from abupy import ABuSymbolPd, ABuScalerUtil, get_price, ABuMarketDrawing, ABuKLUtil

# btc是比特币symbol代号
btc = ABuSymbolPd.make_kl_df('sh000001', start='2000-01-01', end='2018-10-12')
# close	high	low	p_change	open	pre_close	volume	date	date_week	atr21	atr14	key
y = btc.close


def svm_from_cfg(cfg):
    print("cfg", cfg)
    p = pydash.get(cfg, "p", 0)
    d = pydash.get(cfg, "d", 0)
    q = pydash.get(cfg, "q", 0)
    order = (p, d, q)

    P = pydash.get(cfg, "P", 0)
    D = pydash.get(cfg, "D", 0)
    Q = pydash.get(cfg, "Q", 0)
    s = pydash.get(cfg, "s", 0)
    seasonal_order = (P, D, Q, s)

    mod = sm.tsa.statespace.SARIMAX(y,
                                    order=order,
                                    seasonal_order=seasonal_order,
                                    enforce_stationarity=False,
                                    enforce_invertibility=False)

    results = mod.fit()

    print('ARIMA{}x{}12 - AIC:{}'.format(order, seasonal_order, results.aic))

    return results.aic


# logger = logging.getLogger("SVMExample")
logging.basicConfig(level=logging.INFO)  # logging.DEBUG for debug output

# Build Configuration Space which defines all parameters and their ranges
cs = ConfigurationSpace()

p = UniformIntegerHyperparameter("p", 0, 5, default_value=0)
cs.add_hyperparameter(p)
d = UniformIntegerHyperparameter("d", 0, 5, default_value=0)
cs.add_hyperparameter(d)
q = UniformIntegerHyperparameter("q", 0, 5, default_value=0)
cs.add_hyperparameter(q)

P = UniformIntegerHyperparameter("P", 0, 5, default_value=0)
cs.add_hyperparameter(P)
D = UniformIntegerHyperparameter("D", 0, 5, default_value=0)
cs.add_hyperparameter(D)
Q = UniformIntegerHyperparameter("Q", 0, 5, default_value=0)
cs.add_hyperparameter(Q)
s = UniformIntegerHyperparameter("s", 0, 5, default_value=0)
cs.add_hyperparameter(s)

# kernel = CategoricalHyperparameter("kernel", ["linear", "rbf", "poly", "sigmoid"], default_value="poly")
# cs.add_hyperparameter(kernel)
#
# C = UniformFloatHyperparameter("C", 0.001, 1000.0, default_value=1.0)
# shrinking = CategoricalHyperparameter("shrinking", ["true", "false"], default_value="true")
# cs.add_hyperparameters([C, shrinking])


# Scenario object
scenario = Scenario({"run_obj": "quality",  # we optimize quality (alternatively runtime)
                     "runcount-limit": 3,  # maximum function evaluations
                     "cs": cs,  # configuration space
                     "deterministic": "true"
                     })

# Example call of the function
# It returns: Status, Cost, Runtime, Additional Infos
def_value = svm_from_cfg(cs.get_default_configuration())
print("Default Value: %.2f" % (def_value))

# Optimize, using a SMAC-object
print("Optimizing! Depending on your machine, this might take a few minutes.")
smac = SMAC(scenario=scenario, rng=np.random.RandomState(42),
            tae_runner=svm_from_cfg)

incumbent = smac.optimize()

inc_value = svm_from_cfg(incumbent)

print("Optimized Value: %.2f" % (inc_value))

# ARIMA(1, 2, 4)x(3, 3, 1, 3)12 - AIC:56609.82210201341
# Optimized Value: 56609.82
