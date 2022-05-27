# -*- coding: utf-8 -*-
"""
Created on Thu May  5 02:07:30 2022

@author: longj
"""

import math
import numpy as np
import os

a = math.log(1 - 21 / (51 - 5)) / (-28114)
# print(a)

# 读取 bin 所有点坐标(longitude, elevation)
# 读取 ATL03_3and4 的所有点 coordinate 和 attribute
path = './'
dirs = os.listdir(path)
for dir in dirs:
    if dir[-12:] == "d_time_h.txt":
        p_xyz = np.genfromtxt(dir,delimiter = ",")
length = len(p_xyz)
Window = 5 + 46 * (1 - math.exp( -1 * a * length))
# print(Window)

arry = np.zeros(2)
arry[0] = a
arry[1] = Window
print(arry)

np.savetxt("./2_Window.txt", arry, delimiter=",")