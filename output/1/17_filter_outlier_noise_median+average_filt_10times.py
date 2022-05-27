# -*- coding: utf-8 -*-
"""
Created on Thu May 19 17:56:02 2022

@author: longj
"""

import numpy as np
import csv
from filter_function import median_filter_good,average_filter_good

'''
************** 中值滤波 + 移动平均窗口滤波 10次 **************
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
    
    
# 读取 4_Asmooth_4 的所有点
Asmooth_1 = list(np.genfromtxt("./11_Asmooth_1.txt",delimiter = ","))

print("len(Asmooth_1)",len(Asmooth_1))
print("SmoothSize",SmoothSize)

average_filtered_surface = Asmooth_1
for i in range(10):
    median_filtered_surface = median_filter_good(average_filtered_surface,SmoothSize)
    average_filtered_surface = average_filter_good(median_filtered_surface , SmoothSize)

# 输出
Asmooth_5 = average_filtered_surface

print("len(Asmooth_5)",len(Asmooth_5))

# 存储 Asmooth_2
with open('./12_Asmooth_2.txt','w') as out:
        csv_out=csv.writer(out)
        # csv_out.writerow(['X','Y'])
        for row in Asmooth_5:
            csv_out.writerow(row)