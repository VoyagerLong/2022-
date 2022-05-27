# -*- coding: utf-8 -*-
"""
Created on Fri Apr 15 19:19:31 2022

@author: longj
"""

import os
import open3d as o3d
import pandas as pd
import numpy as np
import sys
import csv
import math
from mkdir_function import mkdir
import shutil
'''
************* kd tree *************
kd-树是 k-dimention tree的缩写，是对数据点在k维空间中划分的一种数据结构，
主要应用于多维空间关键数据的搜索（如范围搜索和最近邻搜索）

kd tree 是一种空间划分树，把整个空间划分为特定的几个部分，然后在特定空间的部分内
进行相关搜索操作。
'''

# -----------------------------------------------------------
# *********************** function ****************************
# -----------------------------------------------------------



'''
************* k近邻搜索 ***************
Search_knn_vector_3d，返回查询点的k个最近邻索引列表，这些相邻的点存储在一个数组中。
'''

'''
************ 计算搜索半径 r ************
公式 P / Ntotal = V / Vtotal
其中 V = π * r^^2
Vtotal = 1
'''
def calculat_search_r(pcd_vector, P = 20, Ntotal = 1):
    r = math.sqrt(P / Ntotal / 3.1415926)
    return r

'''
************* 半径邻域搜索 *************
Search_radius_vector_3d，查询所有和查询点距离小于给定半径的点。
'''
def kd_search_radius(pcd_vector, P = 20, folder_name='default'):
    pcd_tree = o3d.geometry.KDTreeFlann(pcd_vector)
    id_ = list(range(len(pcd_vector.points)))
    Ntotal = len(pcd_vector.points)
    r = calculat_search_r(pcd_vector, P, Ntotal)
    num_in_r = []
    for i in range(Ntotal):
        #建立半径搜索
        [k2, idx2, _] = pcd_tree.search_radius_vector_3d(pcd_vector.points[i],r)
        num_in_r.append([k2, idx2, _][0])
    statistic_occurence(num_in_r,folder_name)
    
    # 输出 r(P=20)_pnum.txt 。第一列为 Id_，第二列为 pnum。
    dict_  = {'point_ID':id_, 'num_in_r':num_in_r}
    df = pd.DataFrame(dict_)
    df['num_in_r'].hist(bins=100)
    mkdir('./'+ folder_name)
    df.to_csv('./'+ folder_name +'/id_r.txt',index=False,header=False)
    return
    
'''
************* 记r(P=20)对应的频数 *************
使用 dict()
'''
def statistic_occurence(num_in_r,folder_name='default'):
    
    se = pd.Series(num_in_r)
    countDict = dict(se.value_counts())
    # print(countDict)
    
    # 输出 r(P=20)_poccurence.txt 。第一列为 r(P=20)，第二列为 pnum的Occurence。
    mkdir('./'+ folder_name)
    with open('./'+ folder_name +'/r_poccurence.txt',"w") as f:
        writer=csv.writer(f)
        for key,value in countDict.items():
            writer.writerow([key,value])
    
    return countDict
    
# -----------------------------------------------------------
# *********************** main() ****************************
# -----------------------------------------------------------

'''
************* 读取txt *************
Open3D不能直接读取txt点云，可以通过numpy读取点坐标(分隔符为","),
再转成三维向量进行可视化。
'''

# txt数据读取
path = './'
dirs = os.listdir(path)
i = 1
for dir in dirs:
    if dir[-12:] == "d_time_h.txt":
        # 挨个读取 bin 数据
        pcd = np.genfromtxt(dir,delimiter = ",")

        # 初始化open3d vector
        pcd_vector = o3d.geometry.PointCloud()

        # 加载点坐标
        pcd_vector.points = o3d.utility.Vector3dVector(pcd[:, : 3])

        # 输出点云个数
        #print(len(pcd_vector.points))

        # KD树邻域搜索 P= 20
        # kd_search_knn(pcd_vector, 20)

        # KD树半径搜索 r(P = 20)
        kd_search_radius(pcd_vector, 5,str(i))
        for dir_ in dirs:
            if dir_[0:12] == dir[0:12]:
                shutil.move(path + dir_, path + '/' + str(i)+'/'+dir_)
        #shutil.move(path + dir, path + '/' + str(i)+'/'+dir)
        i = i + 1
        