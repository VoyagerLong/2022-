# -*- coding: utf-8 -*-
"""
Created on Mon May 23 17:24:08 2022

@author: longj
"""

import numpy as np
import matplotlib.pyplot as plt
import csv
from filter_function import median_filter_with_empty_7col ,average_filter_with_empty_7col,average_filter_with_offset_7col
from compare_height_function import compare_2_layers_7col
import matplotlib
matplotlib.rcParams['font.sans-serif'] = ['SimHei']
matplotlib.rcParams['axes.unicode_minus'] =False


# --------------------- 参数 -------------------------------------------------
# 读取 window_size
window_size = int(list(np.genfromtxt("./2_Window.txt",delimiter = ","))[1])

# medianSpan 必须为奇数，因为滤算子波需要奇数长度
if window_size % 2 == 0:
    window_size = window_size + 1

medianSpan = int(window_size * 2 / 3)

# medianSpan 必须为奇数，因为滤算子波需要奇数长度
if medianSpan % 2 == 0:
    medianSpan = medianSpan + 1
    
    
# --------------------- 5.1 cutOff -------------------------------------------------
# 读取 4_potential_ground 的所有点 XYH 和 along-track_dist
top = np.genfromtxt("./15_potential_ground.txt",delimiter = ",")
len_top = len(top)

print('-------- Finding top points -----------------------')
print("len_top",len_top)
print("medianSpan",medianSpan)

# 进行 3 次 中值滤波 + 均值滤波
original_begin_index = 0
for i in range(3):
    print(i+1,"轮")
    # new_ground = extract_dist_ph(ground)
    # cutOff = medianfilter(ground), medianSpan
    cutOff_1 = median_filter_with_empty_7col(top,medianSpan)
    original_begin_index = original_begin_index + int((medianSpan - 1)/2)
    print("> len(cutOff_1)", len(cutOff_1))
    print(">> original_begin_index",original_begin_index)
    # cutOff = smoothfilter(cutOff), Window 
    cutOff_2 = average_filter_with_empty_7col(cutOff_1 , window_size)
    original_begin_index = original_begin_index + int((window_size - 1)/2)
    print("> len(cutOff_2)", len(cutOff_2))
    print(">> original_begin_index",original_begin_index,'\n')
    del cutOff_1
    top = compare_2_layers_7col(top, cutOff_2, 1)[0]
    del cutOff_2


print("结束 initially ground photons 提取")
print("len_ground",len(top),'\n')
print('-------- Finding lowerbound -----------------------')


# 存储
with open('./16_top.txt','w') as out:
        csv_out=csv.writer(out)
        # csv_out.writerow(['X','Y'])
        for row in top:
            csv_out.writerow(row)

# ------------------------ 5.2 lowerbound ----------------------------------
# 函数输入格式
new_top = top
original_begin_index = 0
# Median
upperbound = median_filter_with_empty_7col(new_top, medianSpan)
original_begin_index = original_begin_index + int((medianSpan - 1)/2)
print(i,"> len(upperbound)", len(upperbound))
print(">> original_begin_index",original_begin_index)

# Smooth
upperbound_final = average_filter_with_offset_7col(upperbound, window_size, 1)
print(i,"> len(upperbound)", len(upperbound_final))
print(">> original_begin_index",original_begin_index)

# 存储
with open('./16_upperbound.txt','w') as out:
        csv_out=csv.writer(out)
        # csv_out.writerow(['X','Y'])
        for row in upperbound_final:
            csv_out.writerow(row)