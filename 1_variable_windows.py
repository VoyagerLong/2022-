# -*- coding: utf-8 -*-
"""
Created on Thu May  5 02:07:30 2022

@author: longj
"""

import math
import numpy as np

a = math.log(1 - 21 / (51 - 5)) / (-28114)
# print(a)

# 读取 bin 所有点坐标(longitude, elevation)
p_xyz = np.genfromtxt("20200925_gt1l_d_time_h.txt",delimiter = ",")
length = len(p_xyz)
Window = 5 + 46 * (1 - math.exp( -1 * a * length))
# print(Window)

arry = np.zeros(2)
arry[0] = a
arry[1] = Window
print(arry)

np.savetxt("./output/2_Window.txt", arry, delimiter=",")