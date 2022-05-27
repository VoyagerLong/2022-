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


# 读取 De_trend
De_trend = list(np.genfromtxt("./9_De_trend.txt",delimiter = ","))
len_De_trend = len(De_trend)

# 取出 height
detrend_ph = []
for i in range(len_De_trend):
    detrend_ph.append(De_trend[i][2])

#print(list(detrend_ph)[0:20])
# 求 height 的 std
detrend_ph_std = np.std(detrend_ph, ddof=1)

arry = np.zeros(2)
arry[0] = detrend_ph_std
arry[1] = len_De_trend
print("Detrend_signal_photons的标准方差(std)=",arry[0])

if arry[0]<10:
    print("标准方差小于 10 m，本步骤无需从 signal photons 中去除 outlier noise")

np.savetxt("./9_detrend_ph_std.txt", arry, delimiter=",")
