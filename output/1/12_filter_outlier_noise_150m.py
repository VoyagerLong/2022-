# -*- coding: utf-8 -*-
"""
Created on Thu May 19 11:12:15 2022

@author: longj
"""
'''
 ************** 4.7 从 signal 去除 noise ***************
 1. 去除 signal 中超过 Asmooth 150 m 的光子
 2. 如果 detrended signal 的标准差大于 10m
    从 signal dataset 去除任何【低于 Asmooth】 【2倍 detrennd signal 标准差】的 signal value
3. 使用剩余的 signal photons 用 pchip 插值计算 1 个新 Asmooth surface，
   然后使用 Window_size 进行 median 滤波，
   再使用 SmoothSize 进行 【median fliter + average filter】 10 次。
4. De-trend 信号光子操作：
   从 Asmooth 表面高度值中减去信号高度值来去除信号光子的趋势。
   使用【去趋势】的高度进行 surface finding。
'''

'''
# 去除上界(Asmooth + 150m)外 signal photons 的方法

  Asmooth
  
  interp_Asmooth
  x 轴 interp_Asmooth_surface_along-track_distance
  y 轴_1 interp_Asmooth_surface_height
  y 轴_2 interp_Asmooth_surface_height + 150 m
  
  signal photons
  x 轴_1 signal_along-track_distance
  x 轴_2 round(signal_along-track_distance) # 原因：与 interp_Asmooth 的 unit 统一
  y 轴 signal_height
  
  去除上界外 signal photons 即相同 x 比较 y_2
'''
import numpy as np
import csv
from compare_height_function import compare_2_layers_


# 读取 Asmooth surface
Asmooth_2 = np.genfromtxt("./7_Asmooth_2.txt",delimiter = ",")
len_Asmooth_2 = len(Asmooth_2)
# Asmooth surface 可使用的最远 dist
#As_2_min_dist = 40500000
#As_2_max_dist = 41750000

# 读取 All_signal_p
signal = list(np.genfromtxt("./1_coord_projed_allP.txt",delimiter = ","))
len_signal = len(signal)
print("len_signal",len_signal)

'''
# 这一函数不仅会比较两个 layer 的 height， 
# 而且是取的当 all_point 数据集中每个单元多个光子 中最低值height 与surface height 比较
'''
within_150m_signal = compare_2_layers_(signal, Asmooth_2, 150)[0]


with open('./8_within_150m_signal.txt','w') as out:
        csv_out=csv.writer(out)
        # csv_out.writerow(['X','Y'])
        for row in within_150m_signal:
            csv_out.writerow(row)