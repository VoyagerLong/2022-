# -*- coding: utf-8 -*-
"""
Created on Thu May 19 11:12:15 2022

@author: longj
"""
'''
 2. 如果 detrended signal 的标准差大于 10m
    从 signal dataset 去除任何【低于 Asmooth】 【2倍 detrennd signal 标准差】的 signal value
'''

import numpy as np
import csv
from compare_height_function import de_trend_signal_with_XYH
from interp_function import save_df

# 读取 within_150m_signal
signal = np.genfromtxt("./8_within_150m_signal.txt",delimiter = ",")
len_signal = len(signal)

# 读取 Asmooth_2
Asmooth_2 = np.genfromtxt("./7_Asmooth_2.txt",delimiter = ",")
len_signal = len(Asmooth_2)

# DE-trend signal dataset
De_trend = de_trend_signal_with_XYH(signal, Asmooth_2)


print("De_trend",len(De_trend))


# 存储
#save_df(De_trend,'./2_De_trend.txt')

with open('./9_De_trend.txt','w') as out:
        csv_out=csv.writer(out)
        # csv_out.writerow(['X','Y'])
        for row in De_trend:
            csv_out.writerow(row)