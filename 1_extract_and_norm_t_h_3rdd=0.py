# -*- coding: utf-8 -*-
"""
Created on Fri Apr 15 19:19:31 2022

@author: longj
"""

import h5py
import os
import numpy as np

min_elem = 0
max_elem = 0

# 将一个 segement 的点 delta_time 平均分成间隔为 spacing_time 的 list
def av_spacing_t(delta_time_ls):
    # 创建一个 list 用于存每个点的新的 spaced 的时间
    av_delta_time_ls = []
    
    # 计算 average spacing time
    point_num = len(delta_time_ls)
    begin_deltatime = delta_time_ls[0]
    end_deltatime = delta_time_ls[point_num - 1]
    spacing_time = (end_deltatime - begin_deltatime) / (point_num - 1)
    
    # 将新的 spaced 的时间存进新数组
    for i in range(0, point_num):
        av_delta_time_ls.append(begin_deltatime + spacing_time * i)
    return av_delta_time_ls

# 对每个 element 做 differential
def func(x):
    try:
        elem_norm = (x - min_elem)/(max_elem - min_elem)
    except Exception as e:
        print('Python message: %s\n' % e)
    return elem_norm

# 对数组中所有元素做 differential
def differential(ls):
    global min_elem
    global max_elem
    try:
        min_elem = min(ls)
        max_elem = max(ls)
    except Exception as e:
        print('Python message: %s\n' % e)
    return list(map(func,ls))

# 以 latitude 为 bound 裁切出梨树县区域的 ATL03数据
def clipATL03_heights(in_file03, label):
    dataOut = []
    with h5py.File(in_file03, 'r') as f:
        dsname=''.join([label, "/heights/lat_ph"])
        dataOut = np.array(f[dsname])
        c_edge = [0,0]
        # latitude edge
        for i in range(0, len(dataOut)):
            if dataOut[i] > 43.165 and dataOut[i] < 43.17:
                c_edge[0] = i      
                continue
            elif dataOut[i] > 43.785 and dataOut[i] < 43.79:
                c_edge[1] = i
                continue
        c_edge.sort()
        print("clip取前后索引",c_edge)
    return c_edge

# 读取 ATL03.h5 文件
def readAtl08H5(in_file03, fieldName, label, c_edge):
    # Initialize output
    dataOut = []
    dataOut_slice = []
    if not os.path.isfile(in_file03):
      print('ATL03 file does not exist')
    try:
      with h5py.File(in_file03, 'r') as f:
          dsname=''.join([label, fieldName])
          if dsname in f:
              dataOut = np.array(f[dsname])
              dataOut_slice = dataOut[c_edge[0]:c_edge[1]]
              # print("True")
          else:
              dataOut_slice = []
              print("False")
    except Exception as e:
        print('Python message: %s\n' % e)
    #print(len(dataOut_slice))
    return dataOut_slice

def readAtl08H5_(in_file03, fieldName, label):
    # Initialize output
    dataOut = []
    if not os.path.isfile(in_file03):
      print('ATL03 file does not exist')
    try:
      with h5py.File(in_file03, 'r') as f:
          dsname=''.join([label, fieldName])
          if dsname in f:
              dataOut = np.array(f[dsname])
              # print("True")
          else:
              dataOut = []
              print("False")
    except Exception as e:
        print('Python message: %s\n' % e)
    #print(len(dataOut_slice))
    return dataOut

# 读取所有属性信息并输出为1个txt
def out_attribute(file_path):
    #label_ls = ["gt1l","gt1r","gt2l","gt2r","gt3l","gt3r"]
    label_ls = ["gt1l","gt2l","gt3l"]
    date = file_path[6:14]
    try:
        for i in label_ls:
            # 提示信息
            print(file_path[6:14],i)
            
            # latitude 为裁切边界
            c_edge = clipATL03_heights(file_path, i)
            
            # 提取裁切边界内的 ATL03 属性数据：latitude、longitude、height、deltatime
            lat_ph = list(readAtl08H5_(file_path, "/heights/lat_ph", i))[c_edge[0]:c_edge[1]]
            lon_ph = list(readAtl08H5_(file_path, "/heights/lon_ph", i))[c_edge[0]:c_edge[1]]
            h_ph = list(readAtl08H5_(file_path, "/heights/h_ph", i))[c_edge[0]:c_edge[1]]
            # GPS elapsed time
            delta_time = list(readAtl08H5_(file_path, "/heights/delta_time", i))[c_edge[0]:c_edge[1]]
            # photon channel confidence
            #arry = readAtl08H5_(file_path, "/heights/signal_conf_ph", i)
            signal_conf_ph = list(readAtl08H5_(file_path, "/heights/signal_conf_ph", i))[c_edge[0]:c_edge[1]]
            #list(arry)[c_edge[0]:c_edge[1]]
            # along-track distance    
            dist_ph_along = list(readAtl08H5_(file_path, "/heights/dist_ph_along", i))
            # cumulative  (ralate to 1st photon in research area) along-track distance
            final_along_track_dist = []
            # segment_dist_x 是从这条轨道最开始点到该segment的累计距离，与delta_time相关
            # segment_dist_x = list(readAtl08H5_(file_path, "/geolocation/segment_dist_x", i))
            # 给定segment中第一个光子的索引
            ph_index_beg = list(readAtl08H5_(file_path, "/geolocation/ph_index_beg", i))
            # 在给定segment中的光子数量
            segment_ph_cnt = list(readAtl08H5_(file_path, "/geolocation/segment_ph_cnt", i))
            # 给定segment的长度
            segment_length = list(readAtl08H5_(file_path, "/geolocation/segment_length", i))
            '''
            sum_pnum = 0
            for m in range(len(segment_ph_cnt)):
                sum_pnum = sum_pnum + segment_ph_cnt[m]
            print("定segment中的光子数量之和：",sum_pnum)
            '''
            # 计算每个光子的累计沿轨长度
            k = 0
            cu_segment_length = 0
            final_along_track_dist  = [] 
            for m in range(len(segment_ph_cnt)):
                if(segment_ph_cnt[m]==0):
                    cu_segment_length = cu_segment_length + segment_length[m]           
                else: 
                    try:
                        for j in range(segment_ph_cnt[m]):
                            k = m + j
                            #final_along_track_dist.append((ph_index_beg[m]+j,segment_ph_cnt[m],dist_ph_along[k],cu_segment_length + dist_ph_along[k]))
                            final_along_track_dist.append(cu_segment_length + dist_ph_along[k])
                            cu_segment_length = cu_segment_length + segment_length[m]
                    except:
                        break
            cut_final_along_track_dist = final_along_track_dist[c_edge[0]:c_edge[1]]
            '''
            print("length:h_ph",len(h_ph))
            print("length:segment_ph_cnt",len(segment_ph_cnt))
            # print("length:along_track_dist",len(along_track_dist))
            print("length:final_along_track_dist",len(final_along_track_dist))
            print("length:cut_final_along_track_dist",len(cut_final_along_track_dist))
            '''
            
            # 存储归一化 (relative_average_spacing_delta_time)-(height) 二维坐标
            # 将用于 DRAGANN 滤波获得 signal photons
            d_delta_time = differential(delta_time)
            d_h_ph = differential(h_ph)
            # 由于 3 对 bins 是同时扫描的，因此连接 6 个 bins 为 1 个 list 不适用
            arr_0 = np.zeros(len(d_delta_time))
            
            # 输出未根据 photon signal confidence 筛选的光子
            # output(date,i,"coord_attribute",lon_ph,lat_ph,h_ph,signal_conf_ph,dist_ph_along)
            output(date,i,"coord_attribute",lon_ph,lat_ph,h_ph,cut_final_along_track_dist)
            output(date,i,"d_time_h",d_delta_time,d_h_ph,arr_0,arr_0)

            '''
            # 记下 photon signal confidence 在 land 不等于 3-4 光子的 Id
            
            signal_conf_ph (photon signal confidence) 为 5xN 的数组
            5 列分别表示信号点从下述表面类型(land, ocean, sea ice, land ice and inland water)获得的可能性
            需要提取的是 land 地表类型 flag = 3 和 4 的光子。
            作为第二遍 DRAGANN 滤波的其中一个输入数据集（另一个输入是第一遍 GRAGANN 滤波结果集）
            '''
            
            Id_del_by_config = []
            for j in range(len(signal_conf_ph)):
                if signal_conf_ph[j][0]==3 or signal_conf_ph[j][0]==4:
                    Id_del_by_config.append(j)
            # print(Id_del_by_config)
            # 选出 land 分类等于 3-4 的光子
            lat_3and4 = []
            lon_3and4 = []
            h_3and4 = []
            # signal_conf_3and4 = []
            dist_3and4_along = []
            for k in Id_del_by_config:
                lat_3and4.append(lat_ph[k])
                lon_3and4.append(lon_ph[k])
                h_3and4.append(h_ph[k])
                # signal_conf_3and4.append(signal_conf_ph[k])
                dist_3and4_along.append(cut_final_along_track_dist[k])
            # 输出 photon signal confidence 筛选后的光子
            # output(date,i,"coord_attribute_3and4",lon_3and4,lat_3and4,h_3and4,signal_conf_3and4,dist_3and4_along)
            output(date,i,"coord_attribute_3and4",lon_3and4,lat_3and4,h_3and4,dist_3and4_along)
            
    except Exception as e:
        print('Python message: %s\n' % e)
    return


# 所有label输出为一个txt
def output(date,label,attribute_name,attribute1 = [],attribute2 = [],attribute3 = [],attribute4 = []):
    ls = []
    string = '\n'
    for i in range(0,len(attribute1)):
        str1 = ""
        str1 = str(attribute1[i])+","+str(attribute2[i])+","+str(attribute3[i])+","+str(attribute4[i])
        ls.append(str1)
    f=open("./output/"+date+"_"+label+"_"+attribute_name+".txt","w")
    f.write(string.join(ls))
    f.close()
    return


path = './'
dirs = os.listdir(path)
for dir in dirs:
    if dir[-2:] == "h5":
        out_attribute(dir)