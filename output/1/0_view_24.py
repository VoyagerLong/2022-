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
Asmooth_1 = np.genfromtxt("./19_ground_points.txt",delimiter = ",")
len_Asmooth_1 = len(Asmooth_1)

m_height = np.zeros(len_Asmooth_1)
m_dist_along = np.zeros(len_Asmooth_1)
m_ph = np.zeros(len_Asmooth_1)

for i in range(len_Asmooth_1):
    m_height[i] = Asmooth_1[i][2]
    m_dist_along[i] = Asmooth_1[i][3]# - Asmooth_2[0][3]
    m_ph[i] = Asmooth_1[i][6]

'''
************************************************************
'''

# 读取 De-trend_p
Asmooth_2 = np.genfromtxt("./17_ground.txt",delimiter = ",")
len_Asmooth_2 = len(Asmooth_2)

d_height = np.zeros(len_Asmooth_2)
d_dist_along = np.zeros(len_Asmooth_2)

for i in range(len_Asmooth_2):
    d_height[i] = Asmooth_2[i][2]
    d_dist_along[i] = Asmooth_2[i][3]# - Asmooth_2[0][3]
    

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
signal = np.genfromtxt("./8_within_150m_signal.txt",delimiter = ",")
len_signal = len(signal_)

s_height = np.zeros(len_signal)
s_dist_along = np.zeros(len_signal)

for i in range(len_signal):
    s_height[i] = signal[i][2]
    s_dist_along[i] = signal[i][3]# - signal[0][3]

'''

************************************************************
'''
signal1 = np.genfromtxt("./20200830_gt1l_coord_attribute.txt",delimiter = ",")
len_signal1 = len(signal1)

n_height = np.zeros(len_signal1)
n_dist_along = np.zeros(len_signal1)

for i in range(len_signal1):
    n_height[i] = signal1[i][2]
    n_dist_along[i] = signal1[i][3]# - signal[0][3]

'''

************************************************************
'''
#用subplot()方法绘制多幅图形
#plt.figure(figsize=(6,10),dpi=80)
plt.figure(figsize=(18,14),dpi=80)
plt.figure(1)
ax1 = plt.subplot(311)
plt.title("title")
plt.xlabel("沿轨道距离 (m)")
plt.ylabel("高程 (m)")
plt.scatter(n_dist_along, n_height, color = 'silver',marker = '.', label='所有光子')
plt.scatter(s_dist_along, s_height, color = 'blue',marker = '.', label='信号光子')
plt.plot(m_dist_along, m_ph, 'r.', label='最终地表面点')
plt.legend()

ax1 = plt.subplot(312)
plt.title("title")
plt.xlabel("沿轨道距离 (m)")
plt.ylabel("高程 (m)")
plt.scatter(f_dist_along, f_height, color = 'blue',marker = '.', label='De-trended 信号光子')
#plt.plot(d_dist_along, d_height, 'b.', label='地面点')
plt.plot(m_dist_along, m_height, 'r.', label='最终地表面点')
plt.legend()


plt.savefig('最终地表面点.png')