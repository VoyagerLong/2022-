# -*- coding: utf-8 -*-
"""
Created on Tue May  3 15:27:03 2022

@author: longj
"""

import numpy as np
import csv
import matplotlib.pyplot as plt
from filter_function import median_filter_with_empty_7col ,average_filter_with_empty_7col,average_filter_with_offset_7col
from compare_height_function import compare_2_layers_7col
'''
def extract_dist_ph(signal):
    dist_ph = []
    for i in range(len(signal)):
        dist_ph.append((signal[i][3],signal[i][2]))
    return dist_ph
'''
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
    
# ---------------------- 4.1 cutOff ----------------------------------------
# 读取 within_150m_signal 的所有点 XYH 和 along-track_dist
ground = np.genfromtxt("./13_detrended.txt",delimiter = ",")
len_ground = len(ground)

dz = []
distan = []
for i in range(len(ground)):
    dz.append(ground[i][2])
    distan.append(ground[i][3])


print('-------- Finding ground points -----------------------')
print("len_ground",len_ground)
print("medianSpan",medianSpan)

# 进行 5 次 中值滤波 + 均值滤波
original_begin_index = 0
for i in range(5):
    print(i+1,"轮")
    # new_ground = extract_dist_ph(ground)
    # cutOff = medianfilter(ground), medianSpan
    cutOff_1 = median_filter_with_empty_7col(ground,medianSpan)
    original_begin_index = original_begin_index + int((medianSpan - 1)/2)
    print("> len(cutOff_1)", len(cutOff_1))
    print(">> original_begin_index",original_begin_index)
    # cutOff = smoothfilter(cutOff), Window 
    cutOff_2 = average_filter_with_empty_7col(cutOff_1 , window_size)
    original_begin_index = original_begin_index + int((window_size - 1)/2)
    print("> len(cutOff_2)", len(cutOff_1))
    print(">> original_begin_index",original_begin_index,'\n')
    del cutOff_1
    
    ground = compare_2_layers_7col(ground, cutOff_2, 1)[0]
    del cutOff_2


print("结束 initially ground photons 提取")
print("len_ground",len(ground),'\n')

print('-------- Finding lowerbound -----------------------')

# 存储
with open('./14_ground.txt','w') as out:
        csv_out=csv.writer(out)
        # csv_out.writerow(['X','Y'])
        for row in ground:
            csv_out.writerow(row)

# ------------------------ 4.2 lowerbound ----------------------------------
# 函数输入格式
new_ground = ground
original_begin_index = 0
# Median
lowerbound = median_filter_with_empty_7col(new_ground, medianSpan * 3)
original_begin_index = original_begin_index + int((medianSpan * 3 - 1)/2)
print(i,"> len(lowerbound)", len(lowerbound))
print(">> original_begin_index",original_begin_index)
# Smooth
middlebound = average_filter_with_empty_7col(lowerbound , window_size)
original_begin_index = original_begin_index + int((window_size - 1)/2)
print(i,"> len(middlebound)", len(middlebound))
print(">> original_begin_index",original_begin_index)
# Smooth
lowerbound_final = average_filter_with_offset_7col(lowerbound, window_size, -4)
print(i,"> len(lowerbound)", len(lowerbound_final))
print(">> original_begin_index",original_begin_index)

# 存储
with open('./14_lowerbound.txt','w') as out:
        csv_out=csv.writer(out)
        # csv_out.writerow(['X','Y'])
        for row in lowerbound_final:
            csv_out.writerow(row)

'''   
a = []
b = []
for i in range(len(cutOff_2)):
    a.append(cutOff_2[i][2])
    b.append(cutOff_2[i][3])
plt.plot(distan,dz,'b.',label='detrended points')
plt.plot(b,a,'r.',label='cutOff_2')
'''
