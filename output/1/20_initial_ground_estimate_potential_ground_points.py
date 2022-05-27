# -*- coding: utf-8 -*-
"""
Created on Mon May 23 12:22:52 2022

@author: longj
"""
import numpy as np
import matplotlib.pyplot as plt
import csv
from interp_function import interp_linear_dist_ph,save_df
from compare_height_function import compare_2_layers_7col_
import matplotlib
matplotlib.rcParams['font.sans-serif'] = ['SimHei']
matplotlib.rcParams['axes.unicode_minus'] =False


'''
# ---------------- linear 插值 -------------------
'''
# 读取 within_150m_signal 的所有点 XYH 和 along-track_dist
lowerbound = np.genfromtxt("./14_lowerbound.txt",delimiter = ",")
along_dist = []
lb_Z = []

for i in range(len(lowerbound)):
    along_dist.append(lowerbound[i][3])
    lb_Z.append(lowerbound[i][2])


dist_lowerbound = int(along_dist[-1] - along_dist[0])
interp_surface = interp_linear_dist_ph(dist_lowerbound, lb_Z, along_dist)


# 存储
save_df(interp_surface,'./15_linear_interp_surface.txt')

'''
--------------- 提取 linear interp surface 上方 photons ----------
'''
surface = np.genfromtxt("./15_linear_interp_surface.txt",delimiter = ",")
#np.genfromtxt('',delimiter = ",")
signal = np.genfromtxt("./14_ground.txt",delimiter = ",")
#potential_ground = compare_2_layers_2col(detrended, interp_surface, 0)[1]
surface_0 = surface[0][0]
surface__1 = surface[-1][0]
#print(surface_0,"********************")

for i in range(len(signal)):
    #print(i,slice_signal[i][0],surface_0)
    if signal[i][3]>surface_0:
        print(">> ",i,signal[i][3],surface_0)
        s_overlay_begin_idx = i
        break

for i in range(1,len(signal)):
    if signal[-i][3]<surface__1:
        print(">> ",len(signal)-i,signal[-i][3],surface__1)
        #print(len(signal)-i+1,signal[-i+1][0],surface__1)
        s_overlay_end_idx = len(signal)- i
        break

signal = signal[s_overlay_begin_idx:s_overlay_end_idx]
"""
dist= []
height = []
for i in range(len(signal)):
    dist.append(signal[i][0])
    height.append(signal[i][1])

plt.plot(dist,height,'.')


"""
result = compare_2_layers_7col_(signal,surface,0)
lower_set = result[1]
# upper_set = result[1]

plt.xlabel('沿轨距离 (m)')
plt.ylabel('高程 (m)')

dist= []
height = []
for i in range(len(lower_set)):
    dist.append(lower_set[i][3])
    height.append(lower_set[i][2])

plt.plot(dist,height,'.',label = 'De-trended 信号光子')

surface_x= []
surface_y = []
for i in range(len(surface)):
    surface_x.append(surface[i][0])
    surface_y.append(surface[i][1])
plt.plot(surface_x,surface_y,'r',label = 'lowerbound 线性插值平面')


# 存储
with open('./15_potential_ground.txt','w') as out:
        csv_out=csv.writer(out)
        # csv_out.writerow(['X','Y'])
        for row in lower_set:
            csv_out.writerow(row)
'''  
# 存储
with open('./output/result_upper_set.txt','w') as out:
        csv_out=csv.writer(out)
        # csv_out.writerow(['X','Y'])
        for row in upper_set:
            csv_out.writerow(row)
'''
