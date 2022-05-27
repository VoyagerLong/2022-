# -*- coding: utf-8 -*-
"""
Created on Tue May 10 16:12:11 2022

@author: longj
"""

import numpy as np
import csv

'''
************ 3.6 保留百分位高度 5 - 95 的光子 ************
'''
p_xyz = np.genfromtxt("./5_pchip_interpolated.txt",delimiter = ",")
arry_len = len(p_xyz)
height = np.zeros(arry_len)
for i in range(arry_len):
    height[i] = p_xyz[i][1]

# height_5to95 存储 height threshold 上下界
height_5to95 = []
height_5to95.append(min(height))
height_5to95.append(max(height))
print("max_h, min_h\n",height_5to95)

height_5_value = height_5to95[0] + 0.05 *  (height_5to95[1] - height_5to95[0])
height_5to95.append(height_5_value)
height_95_value = height_5to95[1] - 0.05 *  (height_5to95[1] - height_5to95[0])
height_5to95.append(height_95_value)
print("max_h, min_h, 5%_h, 95%_h\n",height_5to95)

p_height_5to95 = []
for i in range(arry_len):
    if height[i]>height_5to95[2] and height[i]<height_5to95[3]:
        p_height_5to95.append(p_xyz[i])
    else:
        p_height_5to95.append((p_xyz[i][0],-100))

print("p_height_5to95",len(p_height_5to95))

# 存储 pInThreshold
with open('./6_p_height_5to95.txt','w') as out:
        csv_out=csv.writer(out)
        # csv_out.writerow(['X','Y'])
        for row in p_height_5to95:
            csv_out.writerow(row)

# 存储 地形
np.savetxt("./6_relief.txt",np.array(height_5to95),delimiter=',')