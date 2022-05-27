# -*- coding: utf-8 -*-
"""
Created on Mon May 23 12:22:52 2022

@author: longj
"""
import numpy as np
import matplotlib.pyplot as plt
import csv
from interp_function import interp_linear_dist_ph,save_df_4col,interp_2D_XYH,interp_2D_XYH
from compare_height_function import de_trend_signal_with_XYH,compare_2_layers_7col_,slice_unique_int_dist
import matplotlib
matplotlib.rcParams['font.sans-serif'] = ['SimHei']
matplotlib.rcParams['axes.unicode_minus'] =False


'''
--------------- 提取 linear interp surface 上方 photons ----------
'''
ground = np.genfromtxt("./18_refined_ground.txt",delimiter = ",")
Z = []
dist = []
for i in range(len(ground)):
    Z.append(ground[i][2])
    dist.append(ground[i][3])
'''
plt.plot(dist,Z,'c.',label = 'ground points')
'''
surface_len = int(dist[-1]-dist[0])
surface = interp_linear_dist_ph(surface_len, Z, dist)
'''
e = surface_2[1]
f = surface_2[0]
print("height范围",min(e),max(e))
print("dist范围",min(f),max(f))

plt.plot(f,e,'y-',label = 'linear interplation')
'''
surface_ = []
# 转置 linear_interplote_surface
for i in range(len(surface[0])):
    surface_.append((surface[0][i],surface[1][i]))

ground_points = compare_2_layers_7col_(ground, surface_,0.5)[0]
ground_points = compare_2_layers_7col_(ground_points, surface_,-0.5)[1]

# 存储
with open('./19_ground_points.txt','w') as out:
        csv_out=csv.writer(out)
        # csv_out.writerow(['X','Y'])
        for row in ground_points:
            csv_out.writerow(row)

