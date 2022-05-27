# -*- coding: utf-8 -*-
"""
Created on Tue May 10 01:53:13 2022

@author: longj
"""

import numpy as np
import pandas as pd
import scipy
from scipy import interpolate
import matplotlib.pyplot as plt
from interp_function import interp_2D_XYH,save_df

'''
************ 3.5 去除超出 ref_dem_limit 阈值的 Asmooth ************
# 使用的插值方法是 pchip 形状保存分段立方隐含插值多项式
'''

# （非必须） 计算 window_size
window_size =  list(np.genfromtxt("./2_Window.txt",delimiter = ","))[1]
window_size = round(window_size)
if window_size % 2 == 0:
    window_size = window_size + 1

# （非必须） 计算 SmoothSize
#SmoothSize = int(2 * 1000 * window_size)
SmoothSize = int(2 * 100 * window_size)
   
# 读取 1_Asmooth 中各项属性
Asmooth = list(np.genfromtxt("./4_Asmooth_1.txt",delimiter = ","))
Asmooth_len = len(Asmooth)

height_original = []
dist_original = []

for i in range(1,Asmooth_len):
    '''
    if round(Asmooth[i][0],3) == round(Asmooth[i-1][0],3):
        # 取 height 低的 signal 点
        if Asmooth[i-1][2]>Asmooth[i][2] or Asmooth[i-1][2] == Asmooth[i][2]:
            continue
    #X_original.append(Asmooth[i][0])
    #Y_original.append(Asmooth[i][1])
    '''
    height_original.append(Asmooth[i][1])
    dist_original.append(Asmooth[i][0])
'''
# 进行 pchip 插值，可选：
# 窗口大小多次处理
# 一次处理完所有点
'''
print("开始进行 pchip 插值")
coord_interp = interp_2D_XYH(Asmooth_len, Asmooth_len, height_original, dist_original)
save_df(coord_interp,'./5_pchip_interpolated.txt')

'''
已完成第 0 段，范围 0 90000
已完成第 1 段，范围 90000 180000
已完成第 2 段，范围 180000 270000
已完成第 3 段，范围 270000 360000
已完成第 4 段，范围 360000 450000
已完成第 5 段，范围 450000 540000
已完成第 6 段，范围 540000 630000
已完成第 7 段，范围 630000 720000
已完成第 8 段，范围 720000 810000
已完成第 9 段，范围 810000 900000
已完成第 10 段，范围 900000 990000
已完成第 11 段，范围 990000 1080000
已完成第 12 段，范围 1080000 1170000
已完成第 13 段，范围 1170000 1260000
已完成第 14 段，范围 1260000 1350000
已完成第 15 段，范围 1350000 1440000
已完成第 16 段，范围 1440000 1530000
已完成第 17 段，范围 1530000 1620000
已完成第 18 段，范围 1620000 1710000
已完成小尾巴部分，范围 1710000 1779564
Asmooth 长度： 1779564
X_interp 长度： 1779564
*****************************
Asmooth 前10个记录：
[array([6.32362045e+05, 4.78289371e+06, 3.29900000e+02, 2.30000000e+01]), array([6.32362041e+05, 4.78289374e+06, 3.29900000e+02, 2.40000000e+01]), array([6.32362037e+05, 4.78289378e+06, 3.29900000e+02, 2.50000000e+01]), array([6.32362033e+05, 4.78289381e+06, 3.29900000e+02, 2.60000000e+01]), array([6.32362029e+05, 4.78289385e+06, 3.29900000e+02, 2.70000000e+01]), array([6.32362025e+05, 4.78289388e+06, 3.29900000e+02, 2.80000000e+01]), array([6.32362021e+05, 4.78289392e+06, 3.29900000e+02, 2.90000000e+01]), array([6.32362018e+05, 4.78289395e+06, 3.29900000e+02, 3.00000000e+01]), array([6.32362014e+05, 4.78289399e+06, 3.29900000e+02, 3.10000000e+01]), array([6.32362010e+05, 4.78289402e+06, 3.29900000e+02, 3.20000000e+01])]
-----------------------------
X_interp 前10个记录：
[632362.0382252822, 632362.0316136912, 632362.0250015891, 632362.0183889789, 632362.0117758618, 632362.00516224, 632361.9985481163, 632361.9919334917, 632361.9853183687, 632361.9787027492]

'''