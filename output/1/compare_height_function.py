# -*- coding: utf-8 -*-
"""
Created on Sun May 22 07:21:07 2022

@author: longj
"""



# 函数功能，给 signal 数据 按 int_dist 切片
def slice_unique_int_dist(signal):
    len_signal = len(signal)
    signal_slice = []
    i = 0
    while i < len_signal-1:
        ls_temp=[]
        # unique_hp = signal[i][2]
        ls_temp.append(signal[i])
        unique_int_dist=int(signal[i][3])
        if int(signal[i][3]-signal[i+1][3])==0:
            #print("_",end=", ")
            ls_temp.append(signal[i+1])
            #print(">> ",ls_temp)
            signal_slice.append([unique_int_dist,ls_temp])
            i = i + 2
            continue
        signal_slice.append([unique_int_dist,ls_temp])
        i = i + 1
        #print("**************************************")

    #print("len_signal_slice",len(signal_slice))
    #print(signal_slice)
    return signal_slice


# *********************** 继承 **********************
# 函数功能，给 signal 数据 按 int_dist 切片
def slice_unique_int_dist_2col(signal):
    len_signal = len(signal)
    signal_slice = []
    i = 0
    while i < len_signal-1:
        ls_temp=[]
        # unique_hp = signal[i][2]
        ls_temp.append(signal[i])
        unique_int_dist=int(signal[i][0])
        if int(signal[i][0]-signal[i+1][0])==0:
            #print("_",end=", ")
            ls_temp.append(signal[i+1])
            #print(">> ",ls_temp)
            signal_slice.append([unique_int_dist,ls_temp])
            i = i + 2
            continue
        signal_slice.append([unique_int_dist,ls_temp])
        i = i + 1
        #print("**************************************")

    #print("len_signal_slice",len(signal_slice))
    #print(signal_slice)
    return signal_slice


# *********************** 继承 **********************



# 函数功能，对每片 int_dist, 与目标数据集比较 height 值
def compare_2_layers(signal, Asmooth_surface, delta):
    signal_slice = slice_unique_int_dist(signal)
    # 获取与 interp_Asmooth 重叠段 signal 光子
    result_set = []
    i = 0
    try:
        # 对每个 signal dist slice 去找对应的 Asmooth dist，比较高程
        for unique_slice in signal_slice:
            unique_int_dist = unique_slice[0]
            # 找 Asmooth 对应的 dist
            while Asmooth_surface[i][0]<unique_int_dist:
                i = i + 1
            for j in range(len(unique_slice[1])):
                # 比较 height
                if int(unique_slice[1][j][2]) < float(Asmooth_surface[i][1]) + delta:
                    result_set.append(unique_slice[1][j])
                
    except:
        print("len_result_set",len(result_set))
    return result_set



# 函数功能，对每片 int_dist, 与目标数据集比较 height 值
def compare_2_layers_(signal, Asmooth_surface, delta):
    signal_slice = slice_unique_int_dist(signal)
    print('len_signal_slice',len(signal_slice))
    # 获取与 interp_Asmooth 重叠段 signal 光子
    result_set = []
    inverse_result_set = []
    i = 0
    try:
        # 对每个 signal dist slice 去找对应的 Asmooth dist，比较高程
        for unique_slice in signal_slice:
            unique_int_dist = unique_slice[0]
            # 找 Asmooth 对应的 dist
            while Asmooth_surface[i][0]<unique_int_dist:
                i = i + 1
            for j in range(len(unique_slice[1])):
                # 比较 height
                if int(unique_slice[1][j][2]) < float(Asmooth_surface[i][1]) + delta:
                    result_set.append(unique_slice[1][j])
                else:
                    inverse_result_set.append(unique_slice[1][j])
                
    except:
        print("len_result_set",len(result_set))
    return [result_set,inverse_result_set]
    
# 函数功能，对每片 int_dist, 与目标数据集比较 height 值

def compare_2_layers_7col(signal, Asmooth_surface, delta):
    signal_slice = slice_unique_int_dist(signal)
    print('len_signal_slice',len(signal_slice))
    # 获取与 interp_Asmooth 重叠段 signal 光子
    result_set = []
    inverse_result_set = []
    i = 0
    # 对每个 signal dist slice 去找对应的 Asmooth dist，比较高程
    for unique_slice in signal_slice:
        unique_int_dist = unique_slice[0]
        # 找 Asmooth 对应的 dist
        while Asmooth_surface[i][3]<unique_int_dist:
            i = i + 1
            if i > len(Asmooth_surface)-2:
                 break
        for j in range(len(unique_slice[1])):
            # 比较 height
            if int(unique_slice[1][j][2]) < float(Asmooth_surface[i][2]) + delta:
                result_set.append(unique_slice[1][j])
            else:
                inverse_result_set.append(unique_slice[1][j])
        if i > len(Asmooth_surface)-2:
                 break
    return [result_set,inverse_result_set]

def compare_2_layers_7col_(signal, Asmooth_surface, delta):
    signal_slice = slice_unique_int_dist(signal)
    print('len_signal_slice',len(signal_slice))
    # 获取与 interp_Asmooth 重叠段 signal 光子
    result_set = []
    inverse_result_set = []
    i = 0
    # 对每个 signal dist slice 去找对应的 Asmooth dist，比较高程
    for unique_slice in signal_slice:
        unique_int_dist = unique_slice[0]
        # 找 Asmooth 对应的 dist
        while Asmooth_surface[i][0]<unique_int_dist:
            i = i + 1
            if i > len(Asmooth_surface)-2:
                 break
        for j in range(len(unique_slice[1])):
            # 比较 height
            if int(unique_slice[1][j][2]) < float(Asmooth_surface[i][1]) + delta:
                result_set.append(unique_slice[1][j])
            else:
                inverse_result_set.append(unique_slice[1][j])
    return [result_set,inverse_result_set]

def compare_2_layers_2col(signal, Asmooth_surface, delta):
    signal_slice = slice_unique_int_dist_2col(signal)
    # 获取与 interp_Asmooth 重叠段 signal 光子
    result_set = []
    inverse_result_set = []
    i = 0
    try:
        # 对每个 signal dist slice 去找对应的 Asmooth dist，比较高程
        for unique_slice in signal_slice:
            unique_int_dist = unique_slice[0]
            # 找 Asmooth 对应的 dist
            while Asmooth_surface[i][0]<unique_int_dist:
                i = i + 1
            
            for j in range(len(unique_slice[1])):
                # 比较 height
                if int(unique_slice[1][j][1]) < float(Asmooth_surface[i][1]) + delta:
                    result_set.append(unique_slice[1][j])
                else:
                    inverse_result_set.append(unique_slice[1][j])
            
    except:
        print("len_result_set",len(result_set))
    return [result_set,inverse_result_set]
    
'''
************* 继承 compare_2_layers **************

# 函数功能，对每片 int_dist, 与目标数据集比较 height 值
def compare_2_layers_2col(signal, Asmooth_surface, delta):
    #signal_slice = slice_unique_int_dist(signal)
    # 获取与 interp_Asmooth 重叠段 signal 光子
    result_set = []
    inverse_result_set = []
    i = 0
    #try:
    # 对每个 signal dist 去找对应的 Asmooth dist，比较高程
    for idx in range(len(signal)):
        unique_int_dist = signal[idx][0]
        # 找 Asmooth 对应的 dist
        while Asmooth_surface[i][0]<unique_int_dist and i<len(Asmooth_surface)-1:
            i = i + 1
        if int(signal[idx][1]) < float(Asmooth_surface[i][1]):
            result_set.append(signal[idx])
        else:
            inverse_result_set.append(signal[idx])
    #except:
    #    print("len_result_set",len(result_set))
    return [result_set,inverse_result_set]

************* 继承 compare_2_layers **************
'''



# 函数功能：Asmooth(height) - signal(height) 即所谓的 De-trend surface
def de_trend_signal(signal, Asmooth_surface):
    signal_slice = slice_unique_int_dist(signal)
    # 获取与 interp_Asmooth 重叠段 signal 光子
    result_set = []
    i = 0
    try:
        # 对每个 signal dist slice 去找对应的 Asmooth dist，比较高程
        for unique_slice in signal_slice:
            unique_int_dist = unique_slice[0]
            # 找 Asmooth 对应的 dist
            while Asmooth_surface[i][0]<unique_int_dist:
                i = i + 1
            for j in range(len(unique_slice[1])):
                # Asmooth(height) - signal(height)
                result_set.append((unique_slice[1][j][3], Asmooth_surface[i][1]-unique_slice[1][j][2]))
    except:
        print("len_result_set",len(result_set))
    
    return result_set


# 函数功能：Asmooth(height) - signal(height) 即所谓的 De-trend surface
def de_trend_signal_with_XYH(signal, Asmooth_surface):
    signal_slice = slice_unique_int_dist(signal)
    # 获取与 interp_Asmooth 重叠段 signal 光子
    result_set = []
    i = 0
    try:
        # 对每个 signal dist slice 去找对应的 Asmooth dist，比较高程
        for unique_slice in signal_slice:
            unique_int_dist = unique_slice[0]
            # 找 Asmooth 对应的 dist
            while Asmooth_surface[i][0]<unique_int_dist:
                i = i + 1
            for j in range(len(unique_slice[1])):
                # Asmooth(height) - signal(height)
                result_set.append((unique_slice[1][j][0],unique_slice[1][j][1],Asmooth_surface[i][1]-unique_slice[1][j][2],unique_slice[1][j][3],unique_slice[1][j][4],unique_slice[1][j][5],unique_slice[1][j][2]))
    except:
        print("len_result_set",len(result_set))
    
    return result_set

    
# 函数功能：添加列 dist 形成完整的 surface
def add_dist_col(filtered_ph,original_points,original_begin_index,offset):
    filtered_surface = []
    filtered_index = 0
    # 计算输出 filtered list 在原有 list 的 begin index
    for i in range(original_begin_index,len(original_points)-original_begin_index):
        filtered_surface.append((original_points[i][3],filtered_ph[filtered_index] + offset))
        filtered_index = filtered_index + 1
    return filtered_surface