# -*- coding: utf-8 -*-
"""
Created on Thu May 19 17:30:06 2022

@author: longj
"""

import numpy as np
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
signal = list(np.genfromtxt("./8_within_150m_signal.txt",delimiter = ","))
signal_len = len(signal)

height_original = []
dist_original = []

for i in range(1,signal_len):
    if round(signal[i][0],3) == round(signal[i-1][0],3):
        # 取 height 低的 signal 点
        if signal[i-1][2]>signal[i][2] or signal[i-1][2] == signal[i][2]:
            continue
    #X_original.append(Asmooth[i][0])
    #Y_original.append(Asmooth[i][1])
    height_original.append(signal[i][2])
    dist_original.append(signal[i][3])
'''
# 进行 pchip 插值，可选：
# 窗口大小多次处理
# 一次处理完所有点
'''
coord_interp = interp_2D_XYH(signal_len,signal_len,height_original,dist_original)
save_df(coord_interp,'./10_Asmooth_3_pchip_interp(Asmooth_0).txt')
