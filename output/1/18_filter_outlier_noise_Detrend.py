# -*- coding: utf-8 -*-
"""
Created on Thu May 19 18:56:48 2022

@author: longj
"""

import numpy as np
import csv
from compare_height_function import de_trend_signal_with_XYH

# 读取 Asmooth surface
Asmooth_2 = np.genfromtxt("./12_Asmooth_2.txt",delimiter = ",")
len_Asmooth_2 = len(Asmooth_2)

# 读取 within_150m_signal
signal = np.genfromtxt("./8_within_150m_signal.txt",delimiter = ",")
len_signal = len(signal)

# 获取 int_unique 的 dist 切片
# 形式为[int_unique_dist,array[signal_info],array[signal_info]]
detrended = de_trend_signal_with_XYH(signal, Asmooth_2)
print("len_detrended",len(detrended))

# 存储
with open('./13_detrended.txt','w') as out:
        csv_out=csv.writer(out)
        # csv_out.writerow(['X','Y'])
        for row in detrended:
            csv_out.writerow(row)