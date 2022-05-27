# -*- coding: utf-8 -*-
"""
Created on Tue May 10 00:22:31 2022

@author: longj
"""
import numpy as np
import csv
from filter_function import median_filter_with_XY
'''
************ 3.3 Median filter ************
# 运行 1 次 ws = Window Size 的中值滤波
# 输出surface: Asmooth


*************** 中值滤波 ***************
# 对 Asmooth_original surface 进行中值滤波, Asmooth_median 用于存储本轮滤波后的高程
# 将每一像素点的灰度值设置为该点某邻域窗口内的所有像素点灰度值的中值.
'''

# 读取 signal 所有点 coordinate 和 attribute
interp_A_coord = list(np.genfromtxt("./1_coord_projed_allP.txt",delimiter = ","))

# 输出的 surface 只保留 dist(横轴) 和 height(纵轴)
original_surface = []
XY = []
for i in range(len(interp_A_coord)):
    original_surface.append((interp_A_coord[i][3],interp_A_coord[i][2]))
    XY.append((interp_A_coord[i][4],interp_A_coord[i][5]))

# 读取计算的 window_size
window_size = np.genfromtxt("./2_Window.txt",delimiter = ",")[1]
window_size = round(window_size)
if window_size % 2 == 0:
    window_size = window_size + 1

Asmooth_0 = median_filter_with_XY(original_surface,window_size,XY)
# Asmooth_len = len(Asmooth)

# 存储 0_Asmooth (由 interp_A 进行 1 次中值滤波获得的 surface)
with open('./3_Asmooth_0.txt','w') as out:
        csv_out=csv.writer(out)
        # csv_out.writerow(['X','Y'])
        for row in Asmooth_0:
            csv_out.writerow(row)
