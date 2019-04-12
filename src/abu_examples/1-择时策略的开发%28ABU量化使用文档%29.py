
# coding: utf-8

# # ABU量化系统使用文档 
# 
# <center>
#         <img src="./image/abu_logo.png" alt="" style="vertical-align:middle;padding:10px 20px;"><font size="6" color="black"><b>第1节 择时策略的开发</b></font>
# </center>
# 
# -----------------
# 
# 作者: 阿布
# 
# 阿布量化版权所有 未经允许 禁止转载
# 
# [abu量化系统github地址](https://github.com/bbfamily/abu) (欢迎+star)
# 
# [本节ipython notebook](https://github.com/bbfamily/abu/tree/master/abupy_lecture)
# 
# [本节界面操作教程视频播放地址](https://v.qq.com/x/page/g0555b9k6ge.html)
# 
# 
# 首先导入abupy中本节使用的模块：

# In[1]:

# 基础库导入，注意第一次运行时会比较慢，要做数据的解压等处理操作
from __future__ import print_function
from __future__ import division

import warnings
warnings.filterwarnings('ignore')
warnings.simplefilter('ignore')
    
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
# get_ipython().magic('matplotlib inline')
import os
import sys
# 使用insert 0即只使用github，避免交叉使用了pip安装的abupy，导致的版本不一致问题
sys.path.insert(0, os.path.abspath('../'))
import abupy


# In[2]:

# 使用沙盒数据，目的是和书中一样的数据环境
abupy.env.enable_example_env_ipython()


# abupy.env.enable_example_env_ipython()的目的是使用abupy中内置的测试金融时间序列数据，即不从网络获取数据，
# 只从本地获取数据，优点是所有人在任何时间运行代码的结果都是一致的，因为数据是一致，在编写使用文档的使用，为了所有人在所有时间点可以运行出一致的结果，本教程中大多数示例都使用abupy中内置的测试金融时间序列数据
# 
# abupy中内置的k线数据有
# 
# #### A股市场：
# 
# * 科大讯飞(002230)
# * 乐视网(300104)
# * 东方财富(300059)
# * 中国中车(601766)
# * 同仁堂(600085),
# * 招商银行(600036)
# * 山西汾酒(600809)
# * 万科A(000002)
# * 比亚迪(002594)
# * 万达电影(002739)
# * 上证指数(sh000001)
# 
# #### 美股市场：
# 
# * 苹果(usAAPL)
# * google(usGOOG)
# * facebook(usFB)
# * 特斯拉电动车(usTSLA)
# * 百度(usBIDU)
# * 诺亚财富(usNOAH)
# * 搜房(usSFUN)
# * 唯品会(usVIPS)
# * 58同城(usWUBA)
# * 纳斯达克指数(us.IXIC)
# 
# #### 币类市场：
# 
# * 比特币(btc)
# * 莱特币(ltc)
# 
# #### 国内期货市场：
# 
# V0(PVC)
# P0(棕榈)
# M0(豆粕)
# I0(铁矿石)
# JD0(鸡蛋)
# L0(塑料)
# PP0(PP)
# FB0(纤维板)
# BB0(胶合板)
# Y0(豆油)
# C0(玉米)
# A0(豆一)
# B0(豆二)
# J0(焦炭)
# JM0(焦煤)
# CS0(玉米淀粉)
# TA0(PTA)
# OI0(菜油)
# RS0(菜籽)
# RM0(菜粕)
# ZC0(动力煤)
# WH0(强麦)
# JR0(粳稻)
# SR0(白糖)
# CF0(棉花)
# RI0(早籼稻)
# MA0(郑醇)
# FG0(玻璃)
# LR0(晚籼稻)
# SF0(硅铁)
# SM0(锰硅)
# FU0(燃油)
# AL0(沪铝)
# RU0(橡胶)
# ZN0(沪锌)
# CU0(沪铜)
# AU0(黄金)
# RB0(螺纹钢)
# WR0(线材)
# PB0(沪铅)
# AG0(白银)
# BU0(沥青)
# HC0(热轧卷板)
# SN0(沪锡)
# NI0(沪镍)
# 
# #### 国际期货市场：
# 
# NID(伦敦镍)
# PBD(伦敦铅)
# SND(伦敦锡)
# ZSD(伦敦锌)
# AHD(伦敦铝)
# CAD(伦敦铜)
# XAU(伦敦金)
# XAG(伦敦银)
# XPT(伦敦铂金)
# S(美黄豆)
# W(美小麦)
# C(美玉米)
# BO(美豆油)
# SM(美豆粕)
# HG(纽约铜)
# SI(纽约白银)
# GC(纽约黄金)
# CL(纽约原油)
# NG(纽约天然气)
# 
# #### 港股市场：
# 
# * 中国恒大(hk03333)
# * 腾讯控股(hk00700)
# * 长城汽车(hk02333)
# * 中国信达(hk01359)
# * 复星国际(hk00656)
# * 金山软件(hk03888)
# * 中国平安(hk02318)
# * 恒生指数(hkHSI)

# enable_example_env_ipython的情况下，当请求不在内置数据中的数据时，也不会从网络去获取数据，只会返回空
# 
# eg: 使用ABuSymbolPd请求不在内置数据中的京东(usJD)

# In[3]:

from abupy import ABuSymbolPd
ABuSymbolPd.make_kl_df('usJD') is None


# 使用abupy.env.disable_example_env_ipython关闭沙盒数据后，即可以使用正常的数据获取模式，非本地沙盒数据
# 
# eg: 使用ABuSymbolPd请求不在内置数据中的京东(usJD)

# In[4]:

abupy.env.disable_example_env_ipython()
us_jd = ABuSymbolPd.make_kl_df('usJD')
# 再次开启沙盒环境，本节的示例都是在沙盒数据环境下运行
abupy.env.enable_example_env_ipython()
tail = None
if us_jd is not None:
    tail = us_jd.tail()
tail


# 备注：关于abupy更多环境配置，数据源切换，市场切换，存贮方式等切换等在后续章节会讲解

# 量化系统一般分为回测模块、实盘模块。
# 
# * 回测模块：首先交易者编写实现一个交易策略，它基于一段历史的交易数据，根据交易策略进行模拟买入卖出，策略中可以涉及买入规则、卖出规则、选股规则、仓位控制及滑点策略等等，回测的目的是验证交易策略是否可行。
# * 实盘模块：将回测通过的策略应用于每天的实时交易数据，根据策略发出买入信号、卖出信号，进行实际的买入、卖出操作。

# 回测模块最重要的组成部份是择时、选股：
# 
# * 择时（什么时候投资）
# * 选股（投资什么股票）
# 
# 只有在对的时间买入对的股票才能获利，就像下面张小娴的名言一样，可以把‘股票’ 代替 ‘人’完全合乎逻辑。
# 
# >在对的时间，遇见对的人(股票)，是一种幸福 
# >
# >在对的时间，遇见错的人(股票)，是一种悲伤 
# >
# >在错的时间，遇见对的人(股票)，是一声叹息 
# >
# >在错的时间，遇见错的人(股票)，是一种无奈 
# 
# 本节首先讲解择时(什么时候投资), 后面的小节将讲解选股

# ### 1. 买入择时因子的编写
# 
# 海龟交易法则是量化经典书籍中的经典作品，它里面介绍过一种趋势跟踪策略：N日趋势突破策略
# 
# 趋势突破定义为当天收盘价格超过N天内的最高价或最低价，超过最高价格作为买入信号买入股票持有，超过最低价格作为卖出信号。
# 
# 下面将用abupy来实现海龟交易法则作为一个买入因子的实现代码，向经典致敬：

# In[5]:

from abupy import AbuFactorBuyXD, BuyCallMixin

class AbuFactorBuyBreak(AbuFactorBuyXD, BuyCallMixin):
    """示例继承AbuFactorBuyXD完成正向突破买入择时类, 混入BuyCallMixin，即向上突破触发买入event"""
    def fit_day(self, today):
        """
        针对每一个交易日拟合买入交易策略，寻找向上突破买入机会
        :param today: 当前驱动的交易日金融时间序列数据
        :return:
        """
        # 今天的收盘价格达到xd天内最高价格则符合买入条件
        if today.close == self.xd_kl.close.max():
            # 生成买入订单, 由于使用了今天的收盘价格做为策略信号判断，所以信号发出后，只能明天买
            return self.buy_tomorrow()
        return None


# 上AbuFactorBuyBreak即是完成了海龟突破策略的代码实现：
# 
# 1. 买入因子需要继承AbuFactorBuyXD或者更复杂的策略继承AbuFactorBuyBase
# 2. 买入因子混入BuyCallMixin，即做为正向策略，股票相关的策略全部是正向策略，即买涨，后续章节示例期货，期权会使用BuyPutMixin
# 3. 买入因子需要实现fit_day，即每一个交易日如何执行交易策略，当符合买入条件后，使用buy_tomorrow或者buy_today生成订单
# 
# 更多买入因子实现代码请阅读AbuFactorBuyBase

# ### 2. 分解模式一步一步对策略进行回测

# 本节首先通过分解流程方式一步一步实现使用AbuFactorBuyBreak进行回测，目的是为了更清晰的说明内部操作流程，
# 编码过程会显的有些复杂臃肿，但实际上在编写完成一个策略后只需要使用一行代码即可以完成回测，在后面的小节中会进行讲解。
# 
# 通过字典形式初始化买入buy_factors，首先实现针对一支股票的择时操作:
# 
# * benchmark的意义为基准参考，基准默认使用回测股票对应市场的大盘指数
# * 默认参数下回测过去两年的交易数据，传递AbuBenchmark(n_folds=2)参数修改回测周期
# * AbuCapital为资金主类，参数需要初始资金设定，这里初始设定1000000（100万），另一个参数为刚刚介绍过的benchmark（基准参考）对象
# * buy_factors由两个买入因子组成，进行择时的时候两个因子同时并行生效

# In[6]:

from abupy import AbuBenchmark
from abupy import AbuCapital

# buy_factors 60日向上突破，42日向上突破两个因子
buy_factors = [{'xd': 60, 'class': AbuFactorBuyBreak}, 
               {'xd': 42, 'class': AbuFactorBuyBreak}]
benchmark = AbuBenchmark()
capital = AbuCapital(1000000, benchmark)


# 择时ABuPickTimeExecute主要驱动方式为时间驱动，即通过时间序列一天一天递进，通过买入因子卖出因子的fit来查询是否有事件生成（买入卖出行为），另外也有框架使用事件驱动，它们分别有各自的优点，原始的abu框架就是时间驱动＋事件驱动的，它最大的优点是执行效率比时间驱动高，但是灵活性及扩展性要比时间驱动差。
# 
# 下面使用ABuPickTimeExecute开始进行择时交易回测，ABuPickTimeExecute实际上不是最简洁的回测接口，更简单的接口可以使用abu.run_loop_back()函数，在后面的章节将会示例使用，本节目的是为了更清晰的说明内部操作流程。
# 
# 由回测结果图可看出由于AbuPickTimeWorker没有设置sell_factors，所以所有的交易单子都一直保留没有卖出：
# 
# * orders_pd：所有交易的相关数据（之后会有内容展示）
# * action_pd：所有交易的行为数据（之后会有内容展示）

# In[7]:

from abupy import ABuPickTimeExecute
orders_pd, action_pd, _ = ABuPickTimeExecute.do_symbols_with_same_factors(['usTSLA'],
                                                                            benchmark,
                                                                            buy_factors,
                                                                            None,
                                                                            capital, show=True)


# ### 3. 卖出择时因子的实现
# 
# 上面所有单子都没有成交的原因是没有卖出因子，下面首先实现类似买入策略的N日趋势突破策略AbuFactorSellBreak，当股价向下突破N日最低价格时卖出股票，即当天收盘价格低于N天内最低价格作为卖出信号，认为下跌趋势成立卖出股票：

# In[8]:

from abupy import AbuFactorSellXD, ESupportDirection

class AbuFactorSellBreak(AbuFactorSellXD):
    """示例继承AbuFactorBuyXD, 向下突破卖出择时因子"""
    def support_direction(self):
        """支持的方向，只支持正向"""
        return [ESupportDirection.DIRECTION_CAll.value]

    def fit_day(self, today, orders):
        """
        寻找向下突破作为策略卖出驱动event
        :param today: 当前驱动的交易日金融时间序列数据
        :param orders: 买入择时策略中生成的订单序列
        """
        # 今天的收盘价格达到xd天内最低价格则符合条件
        if today.close == self.xd_kl.close.min():
            for order in orders:
                self.sell_tomorrow(order)


# 上AbuFactorSellBreak即是完成了卖出突破策略的代码实现：
# 
# 1. 卖出因子需要继承AbuFactorSellXD或者更复杂的策略继承AbuFactorSellBase
# 2. 卖出因子需要实现support_direction方法，确定策略支持的买入策略方向，本例中[ESupportDirection.DIRECTION_CAll.value]即只支持正向买入策略，即买涨
# 3. 卖出因子需要实现fit_day，看有没有符合卖出条件的交易单子
# 
# 更多具体卖出因子实现代码请阅读AbuFactorSellBase
# 
# 备注：之后章节的期货示例讲讲解如何使用ESupportDirection做反向交易，buy put

# #### 3.2 买入因子和卖出因子在回测中同时生效

# 同理使用字典组装卖出因子：

# In[9]:

# 使用120天向下突破为卖出信号
sell_factor1 = {'xd': 120, 'class': AbuFactorSellBreak}

# buy_factors 60日向上突破，42日向上突破两个因子
buy_factors = [{'xd': 60, 'class': AbuFactorBuyBreak}, 
               {'xd': 42, 'class': AbuFactorBuyBreak}]

# 只使用120天向下突破为卖出因子
sell_factors = [sell_factor1]
capital = AbuCapital(1000000, benchmark)
orders_pd, action_pd, _ = ABuPickTimeExecute.do_symbols_with_same_factors(['usTSLA'],
                                                                            benchmark,
                                                                            buy_factors,
                                                                            sell_factors,
                                                                            capital, show=True)


# 从上图可以看到，大多数的交易卖出因子都生效了，但效果很不好, 下一节将继续通过增加多个卖出因子同时作用于策略上来提高策略的效果。
# 
# #### abu量化文档目录章节
# 
# 1. [择时策略的开发](http://www.abuquant.com/lecture/lecture_1.html)
# 2. [择时策略的优化](http://www.abuquant.com/lecture/lecture_2.html)
# 3. [滑点策略与交易手续费](http://www.abuquant.com/lecture/lecture_3.html)
# 4. [多支股票择时回测与仓位管理](http://www.abuquant.com/lecture/lecture_4.html)
# 5. [选股策略的开发](http://www.abuquant.com/lecture/lecture_5.html)
# 6. [回测结果的度量](http://www.abuquant.com/lecture/lecture_6.html)
# 7. [寻找策略最优参数和评分](http://www.abuquant.com/lecture/lecture_7.html)
# 8. [A股市场的回测](http://www.abuquant.com/lecture/lecture_8.html)
# 9. [港股市场的回测](http://www.abuquant.com/lecture/lecture_9.html)
# 10. [比特币，莱特币的回测](http://www.abuquant.com/lecture/lecture_10.html)
# 11. [期货市场的回测](http://www.abuquant.com/lecture/lecture_11.html)
# 12. [机器学习与比特币示例](http://www.abuquant.com/lecture/lecture_12.html)
# 13. [量化技术分析应用](http://www.abuquant.com/lecture/lecture_13.html)
# 14. [量化相关性分析应用](http://www.abuquant.com/lecture/lecture_14.html)
# 15. [量化交易和搜索引擎](http://www.abuquant.com/lecture/lecture_15.html)
# 16. [UMP主裁交易决策](http://www.abuquant.com/lecture/lecture_16.html)
# 17. [UMP边裁交易决策](http://www.abuquant.com/lecture/lecture_17.html)
# 18. [自定义裁判决策交易](http://www.abuquant.com/lecture/lecture_18.html)
# 19. [数据源](http://www.abuquant.com/lecture/lecture_19.html)
# 20. [A股全市场回测](http://www.abuquant.com/lecture/lecture_20.html)
# 21. [A股UMP决策](http://www.abuquant.com/lecture/lecture_21.html)
# 22. [美股全市场回测](http://www.abuquant.com/lecture/lecture_22.html)
# 23. [美股UMP决策](http://www.abuquant.com/lecture/lecture_23.html)
# 
# [更多阿布量化量化技术文章](http://www.abuquant.com/article)
# 
# abu量化系统文档教程持续更新中，请关注公众号中的更新提醒。
# 
# #### 《量化交易之路》目录章节及随书代码地址
# 
# 1. [第二章 量化语言——Python](https://github.com/bbfamily/abu/tree/master/ipython/第二章-量化语言——Python.ipynb)
# 2. [第三章 量化工具——NumPy](https://github.com/bbfamily/abu/tree/master/ipython/第三章-量化工具——NumPy.ipynb)
# 3. [第四章 量化工具——pandas](https://github.com/bbfamily/abu/tree/master/ipython/第四章-量化工具——pandas.ipynb)
# 4. [第五章 量化工具——可视化](https://github.com/bbfamily/abu/tree/master/ipython/第五章-量化工具——可视化.ipynb)
# 5. [第六章 量化工具——数学：你一生的追求到底能带来多少幸福](https://github.com/bbfamily/abu/tree/master/ipython/第六章-量化工具——数学.ipynb)
# 6. [第七章 量化系统——入门：三只小猪股票投资的故事](https://github.com/bbfamily/abu/tree/master/ipython/第七章-量化系统——入门.ipynb)
# 7. [第八章 量化系统——开发](https://github.com/bbfamily/abu/tree/master/ipython/第八章-量化系统——开发.ipynb)
# 8. [第九章 量化系统——度量与优化](https://github.com/bbfamily/abu/tree/master/ipython/第九章-量化系统——度量与优化.ipynb)
# 9. [第十章 量化系统——机器学习•猪老三](https://github.com/bbfamily/abu/tree/master/ipython/第十章-量化系统——机器学习•猪老三.ipynb)
# 10. [第十一章 量化系统——机器学习•ABU](https://github.com/bbfamily/abu/tree/master/ipython/第十一章-量化系统——机器学习•ABU.ipynb)
# 11. [附录A 量化环境部署](https://github.com/bbfamily/abu/tree/master/ipython/附录A-量化环境部署.ipynb)
# 12. [附录B 量化相关性分析](https://github.com/bbfamily/abu/tree/master/ipython/附录B-量化相关性分析.ipynb)
# 13. [附录C 量化统计分析及指标应用](https://github.com/bbfamily/abu/tree/master/ipython/附录C-量化统计分析及指标应用.ipynb)
# 
# 更多关于量化交易相关请阅读[《量化交易之路》](http://www.abuquant.com/books/quantify-trading-road.html)
# 
# 更多关于量化交易与机器学习相关请阅读[《机器学习之路》](http://www.abuquant.com/books/machine-learning-road.html)
# 
# 更多关于abu量化系统请关注微信公众号: abu_quant
# 
# ![](./image/qrcode.jpg)
