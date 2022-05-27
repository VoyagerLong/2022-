# -*- coding: utf-8 -*-
"""
Created on Tue May 10 23:12:37 2022

@author: longj
"""

import numpy as np
import csv
from filter_function import average_filter_with_empty,median_filter_with_empty

'''
------------------------------------------
***** 中值滤波 + 移动平均窗口滤波 10次 *****
****************** Main ******************
------------------------------------------
'''

# 读取 window_size
window_size = list(np.genfromtxt("./2_Window.txt",delimiter = ","))[1]

# 读取 relief
height_5and95 = list(np.genfromtxt("./6_relief.txt",delimiter = ","))
relief = height_5and95[3] - height_5and95[2]

# 计算 SmoothSize
SmoothSize = 2 * window_size
if relief > 200 and (relief < 400 or relief == 400):
    SmoothSize = int(SmoothSize / 2)
elif relief > 400 and (relief < 900 or relief == 900):
    SmoothSize = int(SmoothSize / 3)
elif relief > 900:
    SmoothSize = int(SmoothSize / 4)
else:
    SmoothSize = int(SmoothSize)
# SmoothSize 必须为奇数，因为滤算子波需要奇数长度
if SmoothSize % 2 == 0:
    SmoothSize = SmoothSize + 1
'''
# 读取 p_height_5to95 的所有点 XYH 和 along-track_dist
Asmooth_1 = list(np.genfromtxt("./output/6_p_height_5to95.txt",delimiter = ","))
# 提取 (along-track_dist,height) 成为一个单独数组，对其进行中值滤波和均值滤波


print("len(Asmooth_1)",len(Asmooth_1))
print("SmoothSize",SmoothSize)
# 进行10次 中值滤波 + 均值滤波

'''    
# 读取 p_height_5to95 的所有点 XYH 和 along-track_dist
Asmooth_1_ = list(np.genfromtxt("./6_p_height_5to95.txt",delimiter = ","))
# 提取 (along-track_dist,height) 成为一个单独数组，对其进行中值滤波和均值滤波

Asmooth_1 = []
for i in range(len(Asmooth_1_)):
    Asmooth_1.append((Asmooth_1_[i][0],Asmooth_1_[i][1]))

print("len(Asmooth_1)",len(Asmooth_1))
print("SmoothSize",SmoothSize)
# 进行10次 中值滤波 + 均值滤波

average_filtered_surface = Asmooth_1
for i in range(10):
    median_filtered_surface = median_filter_with_empty(average_filtered_surface,SmoothSize)
    average_filtered_surface = average_filter_with_empty(median_filtered_surface,SmoothSize)
# 输出
Asmooth_2 = average_filtered_surface
print("len(Asmooth_2)",len(Asmooth_2))

# 存储 Asmooth_2
with open('./7_Asmooth_2.txt','w') as out:
        csv_out=csv.writer(out)
        # csv_out.writerow(['X','Y'])
        for row in Asmooth_2:
            csv_out.writerow(row)
