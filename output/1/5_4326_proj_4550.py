# -*- coding: utf-8 -*-
"""
Created on Sun May  8 15:28:14 2022

@author: longj
"""

import numpy as np
import csv
from pyproj import Transformer
import os
'''
 *************** 坐标投影函数 ****************
 # 梨树县玉米分布 tiff 为 CGCS2000  / 3-degree Gauss-Kruger CM 123E 坐标系
 # 将 photons 的 (longitude, latitude) 投影为 CGCS2000 投影坐标系 (X, Y)
'''
def lonLat_to_CGCS2000_proj(lats_tu, lons_tu, from_epsg="epsg:4326", to_epsg="epsg:4550"):
    
    transformer = Transformer.from_crs(from_epsg, to_epsg)
    # process points at a time in a tuple
    x,y = transformer.transform(lats_tu, lons_tu)
    return x,y


'''
-----------------------------------------------------
************** Main() *************
-----------------------------------------------------
'''

'''
# 读取 bin 所有点坐标(longitude, latitude, elevation)
# p_xyz = np.genfromtxt("Signal_p_xyz_250.txt",delimiter = ",")
# arry_len = len(p_xyz)


# 用数组存 (longitude, latitude, elevation)
lon_arry = np.zeros(arry_len)
lat_arry = np.zeros(arry_len)

for i in range(arry_len):
    lon_arry[i] = p_xyz[i][0]
    lat_arry[i] = p_xyz[i][1]
'''

'''
************ 3.1 连接2个数据集作 input ************
# (1) DRAGANN 滤波获得的 signal 光子；(2) ATL03 signal_config_ph 为 3-4 的点
'''
# 读取 signal_DRAGANN 的所有点 coordinate 和 attribute
signal = list(np.genfromtxt("./Signal_p_xyz.txt",delimiter = ","))

# 读取 ATL03_3and4 的所有点 coordinate 和 attribute
path = './'
dirs = os.listdir(path)
for dir in dirs:
    if dir[-9:] == "3and4.txt":
        conf_3and4 = list(np.genfromtxt(dir,delimiter = ","))

signal.extend(conf_3and4)

# 获取列表的第二个元素
def takeForth(elem):
    return elem[3]

signal.sort(key=takeForth)
arry_len = len(signal)

# 用数组存 (longitude, latitude, elevation)
lon_arry = np.zeros(arry_len)
lat_arry = np.zeros(arry_len)

for i in range(arry_len):
    lon_arry[i] = signal[i][0]
    lat_arry[i] = signal[i][1]   
 
# 将 array 转化为 tuple
lon_tu = tuple(lon_arry)
lat_tu = tuple(lat_arry)

# 进行点地理坐标投影
Projected_XY = []
proj = lonLat_to_CGCS2000_proj(lat_tu, lon_tu)
for i in range(arry_len):
    Projected_XY.append((proj[1][i],proj[0][i]))
    
    
# 存储 X,Y,height,maize_flag
coord_projed = []
for i in range(arry_len):
    coord_projed.append((signal[i][0],signal[i][1],signal[i][2],signal[i][3],Projected_XY[i][0],Projected_XY[i][1]))
with open('./1_coord_projed_allP.txt','w') as out:
        csv_out=csv.writer(out)
        # csv_out.writerow(['X','Y'])
        for row in coord_projed:
            csv_out.writerow(row)
