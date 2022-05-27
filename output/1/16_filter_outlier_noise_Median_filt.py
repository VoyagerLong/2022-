# -*- coding: utf-8 -*-
"""
Created on Thu May 19 17:49:30 2022

@author: longj
"""

import numpy as np
import csv
from filter_function import median_filter_good
'''
************ 3.3 Median filter ************
# 运行 1 次 ws = Window Size 的中值滤波
# 输出surface: Asmooth


*************** 中值滤波 ***************
# 对 Asmooth_original surface 进行中值滤波, Asmooth_median 用于存储本轮滤波后的高程
# 将每一像素点的灰度值设置为该点某邻域窗口内的所有像素点灰度值的中值.
'''

# 读取 Asmooth_3 Surface 的所有点 
Asmooth_3 = list(np.genfromtxt("./10_Asmooth_3_pchip_interp(Asmooth_0).txt",delimiter = ","))
'''
interp_A_ph = []
for i in range(len(Asmooth_3)):
    interp_A_ph.append(interp_A_coord[i][1])
'''
# Window_size
window_size = np.genfromtxt("./2_Window.txt",delimiter = ",")[1]
window_size = round(window_size)
if window_size % 2 == 0:
    window_size = window_size + 1
#print(window_size)

Asmooth_4 = median_filter_good(Asmooth_3,window_size)
Asmooth_len = len(Asmooth_4)

"""
# 存储 0_Asmooth (由 interp_A 进行 1 次中值滤波获得的 surface)
p0_Asmooth = []
begin_index = int((window_size-1)/2)
#print(begin_index)

for i in range(Asmooth_len):
    '''
    输出为 (proj_X, proj_Y, median_filtered_height, along_distance)
    '''
    p0_Asmooth.append((interp_A_coord[begin_index + i][0],Asmooth[i]))
"""
with open('./11_Asmooth_1.txt','w') as out:
        csv_out=csv.writer(out)
        # csv_out.writerow(['X','Y'])
        for row in Asmooth_4:
            csv_out.writerow(row)
