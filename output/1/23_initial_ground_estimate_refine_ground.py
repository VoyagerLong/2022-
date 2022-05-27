# -*- coding: utf-8 -*-
"""
Created on Mon May 23 19:26:10 2022

@author: longj
"""


import numpy as np
import matplotlib.pyplot as plt
import csv
from filter_function import median_filter_with_empty_7col ,average_filter_with_empty_7col, average_filter_with_offset_7col
from compare_height_function import compare_2_layers_7col
import matplotlib
matplotlib.rcParams['font.sans-serif'] = ['SimHei']
matplotlib.rcParams['axes.unicode_minus'] =False
import scipy.signal


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
ground = np.genfromtxt("./17_ground.txt",delimiter = ",")
len_ground = len(ground)

print('-------- Refine ground points -----------------------')
print("len_ground",len_ground)
print("medianSpan",medianSpan)

# 进行 2 次 中值滤波 + 均值滤波
original_begin_index = 0
for i in range(2):
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
    print("> len(cutOff_2)", len(cutOff_2))
    print(">> original_begin_index",original_begin_index,'\n')
    del cutOff_1
    ground = compare_2_layers_7col(ground, cutOff_2, 1)[0]
    del cutOff_2
    
print("结束 initially ground photons 提取")
print("len_ground",len(ground),'\n')

# 存储
with open('./18_refined_ground.txt','w') as out:
        csv_out=csv.writer(out)
        # csv_out.writerow(['X','Y'])
        for row in ground:
            csv_out.writerow(row)
print('-------- Finished Refine -----------------------\n\n')

ground = np.genfromtxt("./18_refined_ground.txt",delimiter = ",")
def Savizky_Golay_smooth(original_surface,SmoothSize):
    print("len(original_surface)",len(original_surface))
    height = []
    along_dist = []
    
    for idx in range(len(original_surface)):
        height.append(original_surface[idx][2])
        along_dist.append(original_surface[idx][3])
        
    print("> len(along_dist)",len(along_dist))
    print("> len(height)",len(height))

    new_height = scipy.signal.savgol_filter(height,window_length=SmoothSize,polyorder=3)
    
    smoothed_surface = []
    for i in range(len(new_height)):
        smoothed_surface.append((along_dist[i],new_height[i]))
    
    print(">> len(smoothed_surface)",len(smoothed_surface))
    
    return smoothed_surface
    
print('-------- Savizky-Golay Smooth -----------------------')
# 函数输入格式
refined_ground = ground
original_begin_index = 0
# Median
refined_ground = median_filter_with_empty_7col(refined_ground, medianSpan)
original_begin_index = original_begin_index + int((medianSpan - 1)/2)
print("> len(refined_ground)", len(refined_ground))
print(">> original_begin_index",original_begin_index)

# Savizky-Golay Smooth
ground_final = Savizky_Golay_smooth(refined_ground, window_size)
print("> len(ground_final)", len(ground_final))
print(">> original_begin_index",original_begin_index)


# print(ground_final[0:100])

# 存储
with open('./18_ground_final.txt','w') as out:
        csv_out=csv.writer(out)
        # csv_out.writerow(['X','Y'])
        for row in ground_final:
            csv_out.writerow(row)
