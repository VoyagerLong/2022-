# -*- coding: utf-8 -*-
"""
Created on Tue May 10 00:22:52 2022

@author: longj
"""

'''
************ 3.4 定义一个 reference DEM limit ************
# ref_dem_limit
# 使用 SRTM 90 m DEM, TBD = 120 m
'''
import sys
import numpy as np
import csv
from osgeo import gdal
from gdalconst import *

'''
 ****** 提取在 DEM 上下 120 m 内的点 *******
'''
# 函数功能：elevation 最邻近插值
def nearest_interp_elev(elev):
    new_elev = []
    for i in range(len(elev)):
        if elev[i] != -100:
            new_elev.append(elev[i])
        else:
            j_left = 0
            j_right = 0
            for j in range(1000):
                if elev[i-j_left] == -100:
                    j_left = j_left + 1
                else:
                    break
                if i<j_left:
                    j_left = -100
                    break
                #print(j_left)
            for j in range(1000):
                if elev[i+j_right] == -100:
                    j_right = j_right + 1
                else:
                    break
                if i + j_right > len(elev)-1:
                    j_right = -100
                    break
            if j_left != -100 and j_right != -100:
                new_elev.append((elev[i-j_left]+elev[i+j_right])/2)
            elif j_left == -100 and j_right != -100: 
                #print(i,j_right,len(new_elev))
                new_elev.append(elev[i+j_right])
            elif j_right == -100 and j_left != -100: 
                #print(i,j_left,len(new_elev))
                new_elev.append(elev[i-j_left])
        
        if i % 1000 == 0:
            print(">",end="")
    
    return new_elev


# 函数功能：point overlay raster， get elevation
def in_DEM_threshold(tif_path, xy_ls):
    #获取注册类
    gdal.AllRegister()
    
    #打开栅格数据
    ds = gdal.Open(tif_path)#, GA_ReadOnly)
    if ds is None:
        print('Could not open image')
        sys.exit(1)
    
    #获取仿射变换信息
    transform = ds.GetGeoTransform()
    xOrigin = transform[0]
    yOrigin = transform[3]
    pixelWidth = transform[1]
    pixelHeight = transform[5]
    # 提取(X, Y)处的 pixel_value, 即 DEM 高程
    #DEM_height = []
    #print("xOrigin,xOrigin,pixelWidth,pixelHeight",xOrigin,yOrigin,pixelWidth,pixelHeight)
    #print("range(len(xy_ls)),xy_ls[0][0:2],xy_ls[len(xy_ls)-1][0:2]")
    #print(range(len(xy_ls)),xy_ls[0][0:2],xy_ls[len(xy_ls)-1][0:2])
    elev = []
    for i in range(len(xy_ls)):
        x = xy_ls[i][2]
        y = xy_ls[i][3]
        if x != -100:
            # 获取 (X, Y) 所在的栅格的位置
            xOffset = int((x-xOrigin)/pixelWidth)
            yOffset = int((y-yOrigin)/pixelHeight)
            # 提取 pixel_velue
            data = ds.GetRasterBand(1).ReadAsArray(xOffset, yOffset,1,1)
            pixel_value = data[0,0]
            elev.append(pixel_value)
            '''
            if abs(xy_ls[i][2] - pixel_value)<120:
                pInThreshold.append(xy_ls[i])
            '''
        else:
            elev.append(-100)
    print("已完成从 DEM 的 elevation 提取")
    interped_elev = nearest_interp_elev(elev)
    print("已完成 elevation 最邻近插值")
    pInThreshold = []
    for i in range(len(interped_elev)):
        if abs(xy_ls[i][1] - interped_elev[i])<120:
            pInThreshold.append(xy_ls[i])

    return pInThreshold

# 读取 0_Asmooth 的所有点 X,Y,h 和 along-track_dist
xy_ls = list(np.genfromtxt("./3_Asmooth_0.txt",delimiter = ","))

# 获取 DEM/srtm_61_04_4550
pInThreshold = in_DEM_threshold("../srtm_61_04_4550.tif", xy_ls)
print("xy_ls 长度：",len(xy_ls))
print("pInTreshold 长度：",len(pInThreshold))

# 存储 pInThreshold
with open('./4_Asmooth_1.txt','w') as out:
        csv_out=csv.writer(out)
        # csv_out.writerow(['X','Y'])
        for row in pInThreshold:
            csv_out.writerow(row)

