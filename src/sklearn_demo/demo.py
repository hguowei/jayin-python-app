
import numpy as np
from numpy import *


nums = [2,2,1,7,3,1,1,9,1,4,5,8,6,7,3]


# 均值
np.mean(nums)
# 中位数
np.median(nums)

counts = np.bincount(nums)
# 返回众数
np.argmax(counts)

# 所有四分位数
print(np.percentile(nums, (25, 50, 75), interpolation='midpoint')

print('方差：', var(nums))
