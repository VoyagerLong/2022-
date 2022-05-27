# -*- coding: utf-8 -*-
"""
Created on Fri May 20 20:53:56 2022

@author: longj
"""

import numpy as np
import csv


# 适合没有空缺 且 1个 unit 中没有重复点的普通情况
def median_filter_good(original_surface,SmoothSize):
    print("len(original_surface)",len(original_surface))
    height = []
    along_dist = []
    
    for idx in range(len(original_surface)):
        height.append(original_surface[idx][1])
        along_dist.append(original_surface[idx][0])
        
    print("> len(along_dist)",len(along_dist))
    print("> len(height)",len(height))
    
    
    surface_len = len(height)
    print("surface_len", surface_len)
    # 滤波的方向为 along_dist，而每个 unique_dist 对应的 value 值为 height
    new_surface = []
    
    # 设 surface_len = 300 m
    # surface_len = 1000
    
    original_begin_index = int((SmoothSize - 1)/2)
    # i 是 filtered 的 along_dist 的 index
    result_theorical_len = surface_len-(SmoothSize-1)
    for i in range(result_theorical_len):
        median_filtered = 0
        # [i:i+SmoothSize] 为 算子 与 Asmooth_original surface 重叠的部分的 index
        overlay_h = []
        for j in range(SmoothSize):
            if height[i+j] != -100:
                overlay_h.append(height[i+j])
        len_overlay_h = len(overlay_h)
        # 考虑 pattern 对应的段全为【无值】，设置为异常值
        if len_overlay_h == 0:
            median_filtered = -100
        # 考虑 pattern 对应段值为【偶数】，中位数是 sorted 后中间两个数的平均值
        elif len_overlay_h%2 == 0:
            sorted_overlay_h = sorted(overlay_h)
            median_filtered = int(0.5 * (sorted_overlay_h[int(len_overlay_h/2-1)]+sorted_overlay_h[int(len_overlay_h/2)]))
        else:
            median_idx = int((len_overlay_h-1)/2)
            median_filtered = round(sorted(overlay_h)[median_idx],3)
        new_surface.append((along_dist[original_begin_index+i],median_filtered))
        #print((along_dist[original_begin_index+i],median_filtered))
    
    
    #original_end_index = surface_len - 1 - original_begin_index
    # new_along_dist = along_dist[original_begin_index:original_end_index]
    
    print(">> len(new_surface)",len(new_surface))
    
    # 存储 0_Asmooth (由 interp_A 进行 1 次中值滤波获得的 surface)
    with open('./latest_median_surface.txt','w') as out:
        csv_out=csv.writer(out)
        # csv_out.writerow(['X','Y'])
        for row in new_surface:
            csv_out.writerow(row)
        
    # 提取出非异常值的 photons
    new_surface_sub = []
    for i in new_surface:
        if i[1] != -100:
            new_surface_sub.append(i)
    
    print(">>> len(new_surface_sub)",len(new_surface_sub))
    
    return new_surface_sub
    
# 适合没有空缺 且 1个 unit 中没有重复点的普通情况
def average_filter_good(original_surface,SmoothSize):
    print("len(original_surface)",len(original_surface))
    height = []
    along_dist = []
    
    for idx in range(len(original_surface)):
        height.append(original_surface[idx][1])
        along_dist.append(original_surface[idx][0])
        
    print("> len(along_dist)",len(along_dist))
    print("> len(height)",len(height))
    
    
    surface_len = len(height)
    print("surface_len", surface_len)
    # 滤波的方向为 along_dist，而每个 unique_dist 对应的 value 值为 height
    new_surface = []
    
    # 设 surface_len = 300 m
    # surface_len = 1000
    
    original_begin_index = int((SmoothSize - 1)/2)
    # i 是 filtered 的 along_dist 的 index
    result_theorical_len = surface_len-(SmoothSize-1)
    for i in range(result_theorical_len):
        average_filtered = 0
        # [i:i+SmoothSize] 为 算子 与 Asmooth_original surface 重叠的部分的 index
        overlay_h = []
        for j in range(SmoothSize):
            if height[i+j] != -100:
                overlay_h.append(height[i+j])
        len_overlay_h = len(overlay_h)
        # 考虑 pattern 对应的段全为【无值】，设置为异常值
        if len_overlay_h == 0:
            average_filtered = -100
        # 求 pattern 平均值
        else:
            average_filtered = np.mean(overlay_h)
        new_surface.append((along_dist[original_begin_index+i],average_filtered))
    
    
    #original_end_index = surface_len - 1 - original_begin_index
    # new_along_dist = along_dist[original_begin_index:original_end_index]
    
    print(">> len(new_surface)",len(new_surface))
    
    # 存储 0_Asmooth (由 interp_A 进行 1 次中值滤波获得的 surface)
    with open('./latest_median_surface.txt','w') as out:
        csv_out=csv.writer(out)
        # csv_out.writerow(['X','Y'])
        for row in new_surface:
            csv_out.writerow(row)
        
    # 提取出非异常值的 photons
    new_surface_sub = []
    for i in new_surface:
        if i[1] != -100:
            new_surface_sub.append(i)
    
    print(">>> len(new_surface_sub)",len(new_surface_sub))
    
    return new_surface_sub
    
# **************************** 继承 **********************************************
# 适用于 1个 1m unit 中可能存在多个光子的情况
def median_filter(original_surface,SmoothSize):
    # 输入 list 长度为 len_original_surface; 输出更长,为 surface_len = (max_dist - min_dist)
    print("len(original_surface)",len(original_surface))
    # surface_len = (max_dist - min_dist)
    surface_len = int(original_surface[len(original_surface)-1][0] - original_surface[0][0])
    print("surface_len", surface_len,"= int(",original_surface[len(original_surface)-1][0],"-",original_surface[0][0],")")
    height = []
    along_dist = []
    # 遍历 min_dist ~ max_dist, 将有 height 值的 delts_dist 对应 value 设为 height；将无 height 对应的 value 设为 -100
    # 完成以下循环过程后 height 和 dist 长度都应为 (max_dist - min_dist)
    idx = 0
    # 判断 along_dist 对应这段有无 height
    for i in range(surface_len):
        # 当 idx 超出 original_surface 长度
        if idx > len(original_surface)-1:
            height.append(-100)
            # 存入 along_dist
            along_dist.append(original_surface[0][0]+i)
            continue
        
        # 研究的该 1 m unit 内有光子
        if int(original_surface[idx][0]) == int(original_surface[0][0]+i):
            # 有 2 种情况 ① 1 m unit 内只有唯一一个光子；② 1 m unit 内有 多 个相同的光子
            # ② 判断 1 m unit 内有 是否有 多 个相同的光子.初始假定 否
            #judge = False
            # 研究的 1 m unit 中相同光子的个数， num 已为 1（至少有1个）
            num = 1
            # 假设 1m unit 内至多只有 6 个光子。我需要判断在 研究区 im 内 idx~idx+6 范围内是否还有j个光子(num=j+1)
            for j in range(1,6):
                if idx < len(original_surface)-j and int(original_surface[idx+j][0]) == int(original_surface[0][0]+i):
                    #
                    # print(idx,i,int(original_surface[idx][0]),original_surface[idx][1])
                    # 更新相同的光子num
                    num = j+1
                    # 是 有多个相同的光子
                    #judge = True
            # 是 有多个相同的光子
            #if judge is True:
            height.append(original_surface[idx][1])
            idx = idx + num
            # 存入 along_dist
            along_dist.append(original_surface[0][0]+i)
            continue
            '''
            else:
            # ① 1 m unit 内只有唯一一个光子；
            height.append(original_surface[idx][1])
            # print(idx,i,int(original_surface[idx][0]),original_surface[idx][1])
            idx = idx + num
            # 存入 along_dist
            along_dist.append(original_surface[0][0]+i)
            continue
            '''
        # 不属于上述 2 种情况
        height.append(-100)
        # 存入 along_dist
        along_dist.append(original_surface[0][0]+i)
        
        
    print("> len(along_dist)",len(along_dist))
    print("> len(height)",len(height))
    
    # 滤波的方向为 along_dist，而每个 unique_dist 对应的 value 值为 height
    new_surface = []
    
    # 设 surface_len = 300 m
    # surface_len = 1000
    
    original_begin_index = int((SmoothSize - 1)/2)
    # i 是 filtered 的 along_dist 的 index
    result_theorical_len = surface_len-(SmoothSize-1)
    for i in range(result_theorical_len):
        median_filtered = 0
        # [i:i+SmoothSize] 为 算子 与 Asmooth_original surface 重叠的部分的 index
        overlay_h = []
        for j in range(SmoothSize):
            if height[i+j] != -100:
                overlay_h.append(height[i+j])
        len_overlay_h = len(overlay_h)
        # 考虑 pattern 对应的段全为【无值】，设置为异常值
        if len_overlay_h == 0:
            median_filtered = -100
        # 考虑 pattern 对应段值为【偶数】，中位数是 sorted 后中间两个数的平均值
        elif len_overlay_h%2 == 0:
            sorted_overlay_h = sorted(overlay_h)
            median_filtered = int(0.5 * (sorted_overlay_h[int(len_overlay_h/2-1)]+sorted_overlay_h[int(len_overlay_h/2)]))
        else:
            median_idx = int((len_overlay_h-1)/2)
            median_filtered = round(sorted(overlay_h)[median_idx],3)
        new_surface.append((along_dist[original_begin_index+i],median_filtered))
        #print((along_dist[original_begin_index+i],median_filtered))
    
    
    #original_end_index = surface_len - 1 - original_begin_index
    # new_along_dist = along_dist[original_begin_index:original_end_index]
    
    print(">> len(new_surface)",len(new_surface))
    '''
    # 存储 0_Asmooth (由 interp_A 进行 1 次中值滤波获得的 surface)
    with open('./latest_median_surface.txt','w') as out:
        csv_out=csv.writer(out)
        # csv_out.writerow(['X','Y'])
        for row in new_surface:
            csv_out.writerow(row)
    '''    
    # 提取出非异常值的 photons
    new_surface_sub = []
    for i in new_surface:
        if i[1] != -100:
            new_surface_sub.append(i)
    
    print(">>> len(new_surface_sub)",len(new_surface_sub))
    
    return new_surface_sub


def average_filter(original_surface,SmoothSize):
    # 输入 list 长度为 len_original_surface; 输出更长,为 surface_len = (max_dist - min_dist)
    print("len(original_surface)",len(original_surface))
    # surface_len = (max_dist - min_dist)
    surface_len = int(original_surface[len(original_surface)-1][0] - original_surface[0][0])
    print("surface_len", surface_len,"= int(",original_surface[len(original_surface)-1][0],"-",original_surface[0][0],")")
    height = []
    along_dist = []
    # 遍历 min_dist ~ max_dist, 将有 height 值的 delts_dist 对应 value 设为 height；将无 height 对应的 value 设为 -100
    # 完成以下循环过程后 height 和 dist 长度都应为 (max_dist - min_dist)
    idx = 0
    # 判断 along_dist 对应这段有无 height
    for i in range(surface_len):
        # 当 idx 超出 original_surface 长度
        if idx > len(original_surface)-1:
            height.append(-100)
            # 存入 along_dist
            along_dist.append(original_surface[0][0]+i)
            continue
        
        # 研究的该 1 m unit 内有光子
        if int(original_surface[idx][0]) == int(original_surface[0][0]+i):
            # 有 2 种情况 ① 1 m unit 内只有唯一一个光子；② 1 m unit 内有 多 个相同的光子
            # ② 判断 1 m unit 内有 是否有 多 个相同的光子.初始假定 否
            #judge = False
            # 研究的 1 m unit 中相同光子的个数， num 已为 1（至少有1个）
            num = 1
            # 假设 1m unit 内至多只有 6 个光子。我需要判断在 研究区 im 内 idx~idx+6 范围内是否还有j个光子(num=j+1)
            for j in range(1,6):
                if idx < len(original_surface)-j and int(original_surface[idx+j][0]) == int(original_surface[0][0]+i):
                    #
                    # print(idx,i,int(original_surface[idx][0]),original_surface[idx][1])
                    # 更新相同的光子num
                    num = j+1
                    # 是 有多个相同的光子
                    #judge = True
            # 是 有多个相同的光子
            #if judge is True:
            height.append(original_surface[idx][1])
            idx = idx + num
            # 存入 along_dist
            along_dist.append(original_surface[0][0]+i)
            continue
            '''
            else:
            # ① 1 m unit 内只有唯一一个光子；
            height.append(original_surface[idx][1])
            # print(idx,i,int(original_surface[idx][0]),original_surface[idx][1])
            idx = idx + num
            # 存入 along_dist
            along_dist.append(original_surface[0][0]+i)
            continue
            '''
        # 不属于上述 2 种情况
        height.append(-100)
        # 存入 along_dist
        along_dist.append(original_surface[0][0]+i)
        
        
    print("> len(along_dist)",len(along_dist))
    print("> len(height)",len(height))
    
    # 滤波的方向为 along_dist，而每个 unique_dist 对应的 value 值为 height
    new_surface = []
    
    # 设 surface_len = 300 m
    # surface_len = 300
    
    original_begin_index = int((SmoothSize - 1)/2)
    # i 是 filtered 的 along_dist 的 index
    result_theorical_len = surface_len-(SmoothSize-1)
    for i in range(result_theorical_len):
        average_filtered = 0
        # [i:i+SmoothSize] 为 算子 与 Asmooth_original surface 重叠的部分的 index
        overlay_h = []
        for j in range(SmoothSize):
            if height[i+j] != -100:
                overlay_h.append(height[i+j])
        len_overlay_h = len(overlay_h)
        # 考虑 pattern 对应的段全为【无值】，设置为异常值
        if len_overlay_h == 0:
            average_filtered = -100
        # 求 pattern 平均值
        else:
            average_filtered = np.mean(overlay_h)
        new_surface.append((along_dist[original_begin_index+i],average_filtered))
    
    
    #original_end_index = surface_len - 1 - original_begin_index
    # new_along_dist = along_dist[original_begin_index:original_end_index]
    
    print(">> len(new_surface)",len(new_surface))
    # 存储 0_Asmooth (由 interp_A 进行 1 次中值滤波获得的 surface)
    '''
    with open('./latest_average_surface.txt','w') as out:
        csv_out=csv.writer(out)
        # csv_out.writerow(['X','Y'])
        for row in new_surface:
            csv_out.writerow(row)
    '''
    # 提取出非异常值的 photons
    new_surface_sub = []
    for i in new_surface:
        if i[1] != -100:
            new_surface_sub.append(i)
            
    print(">>> len(new_surface_sub)",len(new_surface_sub))
    
    return new_surface_sub


def median_filter_with_XY(original_surface,SmoothSize,XY):
    # 输入 list 长度为 len_original_surface; 输出更长,为 surface_len = (max_dist - min_dist)
    print("len(original_surface)",len(original_surface))
    # surface_len = (max_dist - min_dist)
    surface_len = int(original_surface[len(original_surface)-1][0] - original_surface[0][0])
    print("surface_len", surface_len,"= int(",original_surface[len(original_surface)-1][0],"-",original_surface[0][0],")")
    height = []
    along_dist = []
    remain_XY = []
    # 遍历 min_dist ~ max_dist, 将有 height 值的 delts_dist 对应 value 设为 height；将无 height 对应的 value 设为 -100
    # 完成以下循环过程后 height 和 dist 长度都应为 (max_dist - min_dist)
    idx = 0
    # 判断 along_dist 对应这段有无 height
    for i in range(surface_len):
        # 当 idx 超出 original_surface 长度
        if idx > len(original_surface)-1:
            break
        
        # 研究的该 1 m unit 内有光子
        if int(original_surface[idx][0]) == int(original_surface[0][0]+i):
            # 有 2 种情况 ① 1 m unit 内只有唯一一个光子；② 1 m unit 内有 多 个相同的光子
            # ② 判断 1 m unit 内有 是否有 多 个相同的光子.初始假定 否
            #judge = False
            # 研究的 1 m unit 中相同光子的个数， num 已为 1（至少有1个）
            num = 1
            # 假设 1m unit 内至多只有 6 个光子。我需要判断在 研究区 im 内 idx~idx+6 范围内是否还有j个光子(num=j+1)
            for j in range(1,6):
                if idx < len(original_surface)-j and int(original_surface[idx+j][0]) == int(original_surface[0][0]+i):
                    #
                    # print(idx,i,int(original_surface[idx][0]),original_surface[idx][1])
                    # 更新相同的光子num
                    num = j+1
                    # 是 有多个相同的光子
                    #judge = True
            # 是 有多个相同的光子
            #if judge is True:
            height.append(original_surface[idx][1])
            remain_XY.append(XY[idx])
            idx = idx + num
            # 存入 along_dist
            along_dist.append(original_surface[0][0]+i)
            continue
            '''
            else:
            # ① 1 m unit 内只有唯一一个光子；
            height.append(original_surface[idx][1])
            # print(idx,i,int(original_surface[idx][0]),original_surface[idx][1])
            idx = idx + num
            # 存入 along_dist
            along_dist.append(original_surface[0][0]+i)
            continue
            '''
        # 不属于上述 2 种情况
        height.append(-100)
        remain_XY.append((-100,-100))
        # 存入 along_dist
        along_dist.append(original_surface[0][0]+i)
        
        
    print("> len(along_dist)",len(along_dist))
    print("> len(height)",len(height))
    print("> len(remain_XY)",len(remain_XY))
    
    # 滤波的方向为 along_dist，而每个 unique_dist 对应的 value 值为 height
    new_surface = []
    
    # 设 surface_len = 300 m
    # surface_len = 1000
    
    original_begin_index = int((SmoothSize - 1)/2)
    # i 是 filtered 的 along_dist 的 index
    result_theorical_len = surface_len-(SmoothSize-1)
    for i in range(result_theorical_len):
        median_filtered = 0
        # [i:i+SmoothSize] 为 算子 与 Asmooth_original surface 重叠的部分的 index
        overlay_h = []
        for j in range(SmoothSize):
            if height[i+j] != -100:
                overlay_h.append(height[i+j])
        len_overlay_h = len(overlay_h)
        # 考虑 pattern 对应的段全为【无值】，设置为异常值
        if len_overlay_h == 0:
            median_filtered = -100
        # 考虑 pattern 对应段值为【偶数】，中位数是 sorted 后中间两个数的平均值
        elif len_overlay_h%2 == 0:
            sorted_overlay_h = sorted(overlay_h)
            median_filtered = int(0.5 * (sorted_overlay_h[int(len_overlay_h/2-1)]+sorted_overlay_h[int(len_overlay_h/2)]))
        else:
            median_idx = int((len_overlay_h-1)/2)
            median_filtered = round(sorted(overlay_h)[median_idx],3)
        new_surface.append((along_dist[original_begin_index+i],median_filtered,remain_XY[original_begin_index+i][0],remain_XY[original_begin_index+i][1]))
        #print((along_dist[original_begin_index+i],median_filtered))
    
    
    #original_end_index = surface_len - 1 - original_begin_index
    # new_along_dist = along_dist[original_begin_index:original_end_index]
    
    print("  >> len(new_surface)",len(new_surface))
    '''
    # 存储 0_Asmooth (由 interp_A 进行 1 次中值滤波获得的 surface)
    with open('./output/new_surface.txt','w') as out:
        csv_out=csv.writer(out)
        # csv_out.writerow(['X','Y'])
        for row in new_surface:
            csv_out.writerow(row)
    '''       
    # 提取出非异常值的 photons
    new_surface_sub = []
    for i in new_surface:
        if i[1] != -100:
            new_surface_sub.append(i)
    
    print("    >>> len(new_surface_sub)",len(new_surface_sub))
    
    return new_surface_sub

def average_filter_with_empty(original_surface,SmoothSize):
    # 输入 list 长度为 len_original_surface; 输出更长,为 surface_len = (max_dist - min_dist)
    print("len(original_surface)",len(original_surface))
    #dist_max = original_surface[len(original_surface)-1][0]
    
    along_dist = []
    height = []
    dist = original_surface[0][0]
    for idx in range(len(original_surface)):
            unique_int_dist = original_surface[idx][0]
            #unique_int_dist = int(original_surface[idx][0])
            # 找 Asmooth 对应的 dist
            while dist<unique_int_dist:
                along_dist.append(dist)
                dist = dist + 1
                height.append(-100)
            height.append(original_surface[idx][1])
            along_dist.append(dist)
            dist = dist + 1
                
    print("> len(along_dist)",len(along_dist))
    print("> len(height)",len(height))
    
    surface_len = len(height)
    print("surface_len", surface_len)
    
    # 滤波的方向为 along_dist，而每个 unique_dist 对应的 value 值为 height
    new_surface = []
    
    # 设 surface_len = 300 m
    # surface_len = 300
    
    original_begin_index = int((SmoothSize - 1)/2)
    # i 是 filtered 的 along_dist 的 index
    result_theorical_len = surface_len-(SmoothSize-1)
    for i in range(result_theorical_len):
        average_filtered = 0
        # [i:i+SmoothSize] 为 算子 与 Asmooth_original surface 重叠的部分的 index
        overlay_h = []
        for j in range(SmoothSize):
            if height[i+j] != -100:
                overlay_h.append(height[i+j])
        len_overlay_h = len(overlay_h)
        # 考虑 pattern 对应的段全为【无值】，设置为异常值
        if len_overlay_h == 0:
            average_filtered = -100
        # 求 pattern 平均值
        else:
            average_filtered = np.mean(overlay_h)
        new_surface.append((along_dist[original_begin_index+i],average_filtered))
    
    
    #original_end_index = surface_len - 1 - original_begin_index
    # new_along_dist = along_dist[original_begin_index:original_end_index]
    
    print(">> len(new_surface)",len(new_surface))
    
    # 存储 0_Asmooth (由 interp_A 进行 1 次中值滤波获得的 surface)
    with open('./latest_median_surface.txt','w') as out:
        csv_out=csv.writer(out)
        # csv_out.writerow(['X','Y'])
        for row in new_surface:
            csv_out.writerow(row)
        
    # 提取出非异常值的 photons
    new_surface_sub = []
    for i in new_surface:
        if i[1] != -100:
            new_surface_sub.append(i)
    
    print(">>> len(new_surface_sub)",len(new_surface_sub))
    
    return new_surface_sub
  
def median_filter_with_empty(original_surface,SmoothSize):
    # 输入 list 长度为 len_original_surface; 输出更长,为 surface_len = (max_dist - min_dist)
    print("len(original_surface)",len(original_surface))
    #dist_max = original_surface[len(original_surface)-1][0]
    
    along_dist = []
    height = []
    dist = original_surface[0][0]
    for idx in range(len(original_surface)):
            unique_int_dist = original_surface[idx][0]
            #unique_int_dist = int(original_surface[idx][0])
            # 找 Asmooth 对应的 dist
            while dist<unique_int_dist:
                along_dist.append(dist)
                dist = dist + 1
                height.append(-100)
            height.append(original_surface[idx][1])
            along_dist.append(dist)
            dist = dist + 1
                
    print("> len(along_dist)",len(along_dist))
    print("> len(height)",len(height))
    
    surface_len = len(height)
    print("surface_len", surface_len)
    
    # 滤波的方向为 along_dist，而每个 unique_dist 对应的 value 值为 height
    new_surface = []
    
    # 设 surface_len = 300 m
    # surface_len = 300
    
    original_begin_index = int((SmoothSize - 1)/2)
    # i 是 filtered 的 along_dist 的 index
    result_theorical_len = surface_len-(SmoothSize-1)
    for i in range(result_theorical_len):
        median_filtered = 0
        # [i:i+SmoothSize] 为 算子 与 Asmooth_original surface 重叠的部分的 index
        overlay_h = []
        for j in range(SmoothSize):
            if height[i+j] != -100:
                overlay_h.append(height[i+j])
        len_overlay_h = len(overlay_h)
        # 考虑 pattern 对应的段全为【无值】，设置为异常值
        if len_overlay_h == 0:
            median_filtered = -100
        # 考虑 pattern 对应段值为【偶数】，中位数是 sorted 后中间两个数的平均值
        elif len_overlay_h%2 == 0:
            sorted_overlay_h = sorted(overlay_h)
            median_filtered = int(0.5 * (sorted_overlay_h[int(len_overlay_h/2-1)]+sorted_overlay_h[int(len_overlay_h/2)]))
        else:
            median_idx = int((len_overlay_h-1)/2)
            median_filtered = round(sorted(overlay_h)[median_idx],3)
        new_surface.append((along_dist[original_begin_index+i],median_filtered))
    
    
    #original_end_index = surface_len - 1 - original_begin_index
    # new_along_dist = along_dist[original_begin_index:original_end_index]
    
    print(">> len(new_surface)",len(new_surface))
    
    # 存储 0_Asmooth (由 interp_A 进行 1 次中值滤波获得的 surface)
    with open('./latest_median_surface.txt','w') as out:
        csv_out=csv.writer(out)
        # csv_out.writerow(['X','Y'])
        for row in new_surface:
            csv_out.writerow(row)
        
    # 提取出非异常值的 photons
    new_surface_sub = []
    for i in new_surface:
        if i[1] != -100:
            new_surface_sub.append(i)
    
    print(">>> len(new_surface_sub)",len(new_surface_sub))
    
    return new_surface_sub
  
  
# 适合没有空缺 且 1个 unit 中没有重复点的普通情况
def average_filter_with_offset(original_surface,SmoothSize,offset):
    print("len(original_surface)",len(original_surface))
    height = []
    along_dist = []
    
    for idx in range(len(original_surface)):
        height.append(original_surface[idx][1])
        along_dist.append(original_surface[idx][0])
        
    print("> len(along_dist)",len(along_dist))
    print("> len(height)",len(height))
    
    
    surface_len = len(height)
    print("surface_len", surface_len)
    # 滤波的方向为 along_dist，而每个 unique_dist 对应的 value 值为 height
    new_surface = []
    
    # 设 surface_len = 300 m
    # surface_len = 1000
    
    original_begin_index = int((SmoothSize - 1)/2)
    # i 是 filtered 的 along_dist 的 index
    result_theorical_len = surface_len-(SmoothSize-1)
    for i in range(result_theorical_len):
        average_filtered = 0
        # [i:i+SmoothSize] 为 算子 与 Asmooth_original surface 重叠的部分的 index
        overlay_h = []
        for j in range(SmoothSize):
            if height[i+j] != -100:
                overlay_h.append(height[i+j])
        len_overlay_h = len(overlay_h)
        # 考虑 pattern 对应的段全为【无值】，设置为异常值
        if len_overlay_h == 0:
            average_filtered = -100
        # 求 pattern 平均值
        else:
            average_filtered = np.mean(overlay_h)+offset
        new_surface.append((along_dist[original_begin_index+i],average_filtered))
    
    
    #original_end_index = surface_len - 1 - original_begin_index
    # new_along_dist = along_dist[original_begin_index:original_end_index]
    
    print(">> len(new_surface)",len(new_surface))
    
    # 存储 0_Asmooth (由 interp_A 进行 1 次中值滤波获得的 surface)
    with open('./latest_median_surface.txt','w') as out:
        csv_out=csv.writer(out)
        # csv_out.writerow(['X','Y'])
        for row in new_surface:
            csv_out.writerow(row)
        
    # 提取出非异常值的 photons
    new_surface_sub = []
    for i in new_surface:
        if i[1] != -100:
            new_surface_sub.append(i)
    
    print(">>> len(new_surface_sub)",len(new_surface_sub))
    
    return new_surface_sub

'''
# ********************* 继承 **********************
'''
def average_filter_with_empty_7col(original_surface,SmoothSize):
    # 输入 list 长度为 len_original_surface; 输出更长,为 surface_len = (max_dist - min_dist)
    print("len(original_surface)",len(original_surface))
    #dist_max = original_surface[len(original_surface)-1][0]
    
    along_dist = []
    height = []
    attr = []
    dist = original_surface[0][3]
    for idx in range(len(original_surface)):
            unique_int_dist = original_surface[idx][3]
            #unique_int_dist = int(original_surface[idx][0])
            # 找 Asmooth 对应的 dist
            while dist<unique_int_dist:
                along_dist.append(dist)
                dist = dist + 1
                height.append(-100)
                attr.append((-100,-100,-100,-100,-100))
            height.append(original_surface[idx][2])
            along_dist.append(dist)
            attr.append((original_surface[idx][0],original_surface[idx][1],original_surface[idx][4],original_surface[idx][5],original_surface[idx][6]))
            dist = dist + 1
                
    print("> len(along_dist)",len(along_dist))
    print("> len(height)",len(height))
    
    surface_len = len(height)
    print("surface_len", surface_len)
    
    # 滤波的方向为 along_dist，而每个 unique_dist 对应的 value 值为 height
    new_surface = []
    
    # 设 surface_len = 300 m
    # surface_len = 300
    
    original_begin_index = int((SmoothSize - 1)/2)
    # i 是 filtered 的 along_dist 的 index
    result_theorical_len = surface_len-(SmoothSize-1)
    for i in range(result_theorical_len):
        average_filtered = 0
        # [i:i+SmoothSize] 为 算子 与 Asmooth_original surface 重叠的部分的 index
        overlay_h = []
        for j in range(SmoothSize):
            if height[i+j] != -100:
                overlay_h.append(height[i+j])
        len_overlay_h = len(overlay_h)
        # 考虑 pattern 对应的段全为【无值】，设置为异常值
        if len_overlay_h == 0:
            average_filtered = -100
        # 求 pattern 平均值
        else:
            average_filtered = np.mean(overlay_h)
        new_surface.append((attr[original_begin_index+i][0],attr[original_begin_index+i][1],average_filtered,along_dist[original_begin_index+i],attr[original_begin_index+i][2],attr[original_begin_index+i][3]))
    
    
    #original_end_index = surface_len - 1 - original_begin_index
    # new_along_dist = along_dist[original_begin_index:original_end_index]
    
    print(">> len(new_surface)",len(new_surface))
    '''
    # 存储 0_Asmooth (由 interp_A 进行 1 次中值滤波获得的 surface)
    with open('./latest_median_surface.txt','w') as out:
        csv_out=csv.writer(out)
        # csv_out.writerow(['X','Y'])
        for row in new_surface:
            csv_out.writerow(row)
    '''    
    # 提取出非异常值的 photons
    new_surface_sub = []
    for i in new_surface:
        if i[2] != -100:
            new_surface_sub.append(i)
    
    print(">>> len(new_surface_sub)",len(new_surface_sub))
    
    return new_surface_sub

def median_filter_with_empty_7col(original_surface,SmoothSize):
    # 输入 list 长度为 len_original_surface; 输出更长,为 surface_len = (max_dist - min_dist)
    print("len(original_surface)",len(original_surface))
    #dist_max = original_surface[len(original_surface)-1][0]
    
    along_dist = []
    height = []
    attr = []
    dist = original_surface[0][3]
    for idx in range(len(original_surface)):
            unique_int_dist = original_surface[idx][3]
            #unique_int_dist = int(original_surface[idx][0])
            # 找 Asmooth 对应的 dist
            while dist<unique_int_dist:
                along_dist.append(dist)
                dist = dist + 1
                height.append(-100)
                attr.append((-100,-100,-100,-100,-100))
            height.append(original_surface[idx][2])
            along_dist.append(dist)
            attr.append((original_surface[idx][0],original_surface[idx][1],original_surface[idx][4],original_surface[idx][5],original_surface[idx][6]))
            dist = dist + 1
                
    print("> len(along_dist)",len(along_dist))
    print("> len(height)",len(height))
    
    surface_len = len(height)
    print("surface_len", surface_len)
    
    # 滤波的方向为 along_dist，而每个 unique_dist 对应的 value 值为 height
    new_surface = []
    
    # 设 surface_len = 300 m
    # surface_len = 300
    
    original_begin_index = int((SmoothSize - 1)/2)
    # i 是 filtered 的 along_dist 的 index
    result_theorical_len = surface_len-(SmoothSize-1)
    for i in range(result_theorical_len):
        median_filtered = 0
        # [i:i+SmoothSize] 为 算子 与 Asmooth_original surface 重叠的部分的 index
        overlay_h = []
        for j in range(SmoothSize):
            if height[i+j] != -100:
                overlay_h.append(height[i+j])
        len_overlay_h = len(overlay_h)
        # 考虑 pattern 对应的段全为【无值】，设置为异常值
        if len_overlay_h == 0:
            median_filtered = -100
        # 考虑 pattern 对应段值为【偶数】，中位数是 sorted 后中间两个数的平均值
        elif len_overlay_h%2 == 0:
            sorted_overlay_h = sorted(overlay_h)
            median_filtered = int(0.5 * (sorted_overlay_h[int(len_overlay_h/2-1)]+sorted_overlay_h[int(len_overlay_h/2)]))
        else:
            median_idx = int((len_overlay_h-1)/2)
            median_filtered = round(sorted(overlay_h)[median_idx],3)
        new_surface.append((attr[original_begin_index+i][0],attr[original_begin_index+i][1],median_filtered,along_dist[original_begin_index+i],attr[original_begin_index+i][2],attr[original_begin_index+i][3],attr[original_begin_index+i][4]))
    
    
    #original_end_index = surface_len - 1 - original_begin_index
    # new_along_dist = along_dist[original_begin_index:original_end_index]
    
    print(">> len(new_surface)",len(new_surface))
    '''
    # 存储 0_Asmooth (由 interp_A 进行 1 次中值滤波获得的 surface)
    with open('./latest_median_surface.txt','w') as out:
        csv_out=csv.writer(out)
        # csv_out.writerow(['X','Y'])
        for row in new_surface:
            csv_out.writerow(row)
    '''    
    # 提取出非异常值的 photons
    new_surface_sub = []
    for i in new_surface:
        if i[2] != -100:
            new_surface_sub.append(i)
    
    print(">>> len(new_surface_sub)",len(new_surface_sub))
    
    return new_surface_sub



# 适合没有空缺 且 1个 unit 中没有重复点的普通情况
def average_filter_with_offset_7col(original_surface,SmoothSize,offset):
    print("len(original_surface)",len(original_surface))
    height = []
    along_dist = []
    
    for idx in range(len(original_surface)):
        height.append(original_surface[idx][2])
        along_dist.append(original_surface[idx][3])
        
    print("> len(along_dist)",len(along_dist))
    print("> len(height)",len(height))
    
    
    surface_len = len(height)
    print("surface_len", surface_len)
    # 滤波的方向为 along_dist，而每个 unique_dist 对应的 value 值为 height
    new_surface = []
    
    # 设 surface_len = 300 m
    # surface_len = 1000
    
    original_begin_index = int((SmoothSize - 1)/2)
    # i 是 filtered 的 along_dist 的 index
    result_theorical_len = surface_len-(SmoothSize-1)
    for i in range(result_theorical_len):
        average_filtered = 0
        # [i:i+SmoothSize] 为 算子 与 Asmooth_original surface 重叠的部分的 index
        overlay_h = []
        for j in range(SmoothSize):
            if height[i+j] != -100:
                overlay_h.append(height[i+j])
        len_overlay_h = len(overlay_h)
        # 考虑 pattern 对应的段全为【无值】，设置为异常值
        if len_overlay_h == 0:
            average_filtered = -100
        # 求 pattern 平均值
        else:
            average_filtered = np.mean(overlay_h)+offset
        new_surface.append((original_surface[original_begin_index+i][0],original_surface[original_begin_index+i][1],average_filtered,along_dist[original_begin_index+i],original_surface[original_begin_index+i][4],original_surface[original_begin_index+i][5],original_surface[original_begin_index+i][6]))
    
    
    #original_end_index = surface_len - 1 - original_begin_index
    # new_along_dist = along_dist[original_begin_index:original_end_index]
    
    print(">> len(new_surface)",len(new_surface))
    
    # 存储 0_Asmooth (由 interp_A 进行 1 次中值滤波获得的 surface)
    with open('./latest_median_surface.txt','w') as out:
        csv_out=csv.writer(out)
        # csv_out.writerow(['X','Y'])
        for row in new_surface:
            csv_out.writerow(row)
        
    # 提取出非异常值的 photons
    new_surface_sub = []
    for i in new_surface:
        if i[1] != -100:
            new_surface_sub.append(i)
    
    print(">>> len(new_surface_sub)",len(new_surface_sub))
    
    return new_surface_sub