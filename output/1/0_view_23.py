# -*- coding: utf-8 -*-
"""
Created on Thu May 12 09:37:42 2022

@author: longj
"""

'''
 ************** 查看 De-trend 平面 ***************

'''
import numpy as np
import matplotlib.pyplot as plt
from pylab import *
matplotlib.rcParams['font.sans-serif'] = ['SimHei']
matplotlib.rcParams['axes.unicode_minus'] =False
'''
************************************************************
'''

# 读取 De-trend_p
Asmooth_2 = np.genfromtxt("./18_ground_final.txt",delimiter = ",")
len_Asmooth_2 = len(Asmooth_2)

# d_X = np.zeros(len_Asmooth_2)
# d_Y = np.zeros(len_Asmooth_2)
d_height = np.zeros(len_Asmooth_2)
d_dist_along = np.zeros(len_Asmooth_2)


for i in range(len_Asmooth_2):
    d_height[i] = Asmooth_2[i][1]
    d_dist_along[i] = Asmooth_2[i][0]# - Asmooth_2[0][3]


'''
************************************************************
'''
signal = np.genfromtxt("./18_refined_ground.txt",delimiter = ",")
len_signal = len(signal)

s_height = np.zeros(len_signal)
s_dist_along = np.zeros(len_signal)


for i in range(len_signal):
    s_height[i] = signal[i][2]
    s_dist_along[i] = signal[i][3]# - signal[0][3]


'''
************************************************************
'''

signal_ = np.genfromtxt("./13_detrended.txt",delimiter = ",")
len_signal_ = len(signal_)

f_height = np.zeros(len_signal_)
f_dist_along = np.zeros(len_signal_)

for i in range(len_signal_):
    f_height[i] = signal_[i][2]
    f_dist_along[i] = signal_[i][3]# - signal[0][3]

'''

************************************************************
'''
#用subplot()方法绘制多幅图形
#plt.figure(figsize=(6,10),dpi=80)
plt.figure(figsize=(18,6),dpi=80)

plt.title("title")
plt.xlabel("沿轨道距离 (m)")
plt.ylabel("高程 (m)")
plt.scatter(f_dist_along, f_height, color = 'silver',marker = '.', label='De-trended 信号光子')
plt.plot(s_dist_along, s_height, 'bo', label='地面点')
plt.plot(d_dist_along, d_height, 'r-', label='精细化的地面')
plt.legend()


plt.savefig('地面点平滑表面.png')