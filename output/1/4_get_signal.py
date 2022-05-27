# -*- coding: utf-8 -*-
"""
Created on Tue May  3 00:13:06 2022

@author: longj
"""
import numpy as np
import csv
import os
import shutil
'''
 --------------- function ---------------
'''

def extract_p_Id(extract_len, threshold):
    ls_signal = []
    for i in range(extract_len):
        if tuple_id_pnum[i][1] > threshold:
            ls_signal.append(tuple_id_pnum[i])
    # 存 list
    with open('./Signal_Id_pnum.txt','w') as out:
        csv_out=csv.writer(out)
        # csv_out.writerow(['Id','pnum_in_r'])
        for row in ls_signal:
            csv_out.writerow(row)
    return ls_signal


'''
 --------------- 选出 PNumInRadius 大于 threshold 的点 ID ---------------
'''
# 读取 r(P=20)_pnum 即第一列id，第二列PNumInRadius的txt
#id_pnum = np.genfromtxt("./output/r(P=20)_pnum.txt",delimiter = ",")
id_pnum = np.genfromtxt("./id_r.txt",delimiter = ",")
extract_len = len(id_pnum)

# 创建元组list
tuple_id_pnum = [tuple(x) for x in id_pnum.tolist()]
# print("len tuple_id_pnuml",len(tuple_id_pnum))

# 提取符合要求的 isolated 点 Id
threshold = np.genfromtxt("./parameters.txt",delimiter = ",")[6]
ls_signal = extract_p_Id(extract_len, threshold)
# print("len ls_signal",len(ls_signal))

# 按 Id_ 排序
sorted_ls_signal = sorted(ls_signal)
# for i in range(4):
#     print(sorted_ls_signal[i])

'''
----------------- 根据唯一标识 Id_ 提取相应点的 xyz differencial 坐标 --------------------
'''
work_dir = os.getcwd()
path = work_dir
dirs = os.listdir(path)
# 查找 [-12:] 为 d_time_h.txt 的文件，取得dir
for dir in dirs:
    if dir[-12:] == "d_time_h.txt":
        # 根据确定为 signal 点的 Id_ 提取 signal 点的 xyz differencial 坐标        
        p_d_th = np.genfromtxt(dir,delimiter = ",")
    if dir[-9:] == '3and4.txt':
        # 读取 1个 bin 的点 Id_ 和其对应的 xyz
        p_xyz = list(np.genfromtxt(dir,delimiter = ","))

# print("len(p_xyz)",len(p_xyz))

# 根据确定为 signal 点的 Id_ 提取 signal 点的 coordinate 坐标以及其他属性信息
extracted_Id = 0
ls_xyz = []
ls_d_th = []
stop_extract = len(ls_signal)
for i in range(len(p_xyz)):
    Id_ = sorted_ls_signal[extracted_Id][0]
    if i == Id_ and i < stop_extract:
        ls_xyz.append(p_xyz[i])
        ls_d_th.append(p_d_th[i])
        extracted_Id = extracted_Id + 1

# 输出 coordinate 坐标以及其他属性信息
#with open("./Signal_p_xyz_" + str(threshold) + ".txt",'w') as out:
with open("./Signal_p_xyz.txt",'w') as out:
    csv_out=csv.writer(out)
    # 1st col:'longitude', 2nd col:'latitude', 3rd col:'height',
    # 4th col:'photon signal confidence', 5th col:'along-track distance'
    for row in ls_xyz:
        csv_out.writerow(row)


#with open("./Signal_normalized_" + str(threshold) + ".txt",'w') as out:
with open("./Signal_normalized.txt",'w') as out:
    csv_out=csv.writer(out)
    # 1st col:'normalized_delts_time', 2nd col:'normalized_height'
    for row in ls_d_th:
        csv_out.writerow(row)