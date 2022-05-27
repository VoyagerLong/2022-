# -*- coding: utf-8 -*-
"""
Created on Sun May 22 09:53:13 2022

@author: longj
"""

import numpy as np
import pandas as pd
import scipy
from scipy import interpolate


'''
*******存储********
'''
def save_df(coord_interp,path):
    zip_coord_interp = list(map(list, zip(*coord_interp)))
    name=['along_track_dist','height_interp']
    #数据有两列
    df_coord_interp = pd.DataFrame(data = zip_coord_interp,columns = name)
    
    df_coord_interp.to_csv(path,sep=',', header=False, index=False)
    return True

def save_df_4col(coord_interp,path):
    zip_coord_interp = list(map(list, zip(*coord_interp)))
    name=['X','Y','along_track_dist','height_interp']
    #数据有四列
    df_coord_interp = pd.DataFrame(data = zip_coord_interp,columns = name)
    
    df_coord_interp.to_csv(path,sep=',', header=False, index=False)
    return True

def interp_2D_XYH(Asmooth_len,SmoothSize,height_original,dist_original):
    dist_interp = []
    height_interp = []
    # 将全长拆开为 2 * window_size m 的小段
    segment_num = round(Asmooth_len / SmoothSize)
    segment_last_len = Asmooth_len % SmoothSize
    
    
    tck = list(range(1,segment_num + 1))
    u = list(range(1,segment_num + 1))
    X_zero = [0 for i in range(len(height_original))]
    
    try:
        if Asmooth_len != SmoothSize:
            # 整段部分
            for i in range(1,segment_num):
                # coord_original 是 XYH 三维数组
                coord_original = [X_zero[SmoothSize*(i-1):SmoothSize*i],dist_original[SmoothSize*(i-1):SmoothSize*i],height_original[SmoothSize*(i-1):SmoothSize*i]]
                #now we get all the knots and info about the interpolated spline
                tck[i], u[i]= interpolate.splprep(coord_original)
                #here we generate the new interpolated dataset, 
                #increase the resolution by increasing the spacing, 500 in this example
                new = interpolate.splev(np.linspace(0,1,SmoothSize), tck[i])
                dist_interp.extend(list(new[1]))
                height_interp.extend(list(new[2]))
                #print("i - len(X_interp)",i,len(X_interp))
                print("已完成第",i,"段，范围",SmoothSize*(i-1),SmoothSize*i)
            # 小尾巴部分
            
            coord_original = [X_zero[Asmooth_len - segment_last_len:Asmooth_len],dist_original[Asmooth_len - segment_last_len:Asmooth_len],height_original[Asmooth_len - segment_last_len:Asmooth_len]]
            tck_final, u_final= interpolate.splprep(coord_original)
            #here we generate the new interpolated dataset, 
            #increase the resolution by increasing the spacing, 500 in this example
            new = interpolate.splev(np.linspace(0,1,segment_last_len), tck_final)
            dist_interp.extend(list(new[1]))
            height_interp.extend(list(new[2]))
            print("已完成小尾巴部分，范围",Asmooth_len - segment_last_len,Asmooth_len)
        
        # SmoothSize=len(X_original)
        else:
            coord_original = [X_zero,dist_original,height_original]
            tck_final, u_final= interpolate.splprep(coord_original)
            #here we generate the new interpolated dataset, 
            #increase the resolution by increasing the spacing, 500 in this example
            new = interpolate.splev(np.linspace(0,1,Asmooth_len), tck_final)
            #print(new)
            dist_interp.extend(list(new[1]))
            height_interp.extend(list(new[2]))
            print("已完成 pchip，范围",'0',Asmooth_len)
    except Exception as e:
        print('Python message: %s\n' % e)
    '''
    print("signal 长度：", len(signal))
    print("X_interp 长度：",len(height_interp))
    print("*****************************")
    print("signal 前10个记录：")
    print(signal[0:10])
    '''
    print("-----------------------------")
    print("X_interp 前10个记录：")
    print(height_interp[0:10])
    
    coord_interp = [dist_interp,height_interp]
    #save_df(coord_interp)
    return coord_interp




def interp_linear_dist_ph(Asmooth_len,height_original,dist_original):
    dist_interp = []
    height_interp = []
    #coord_original = [X_zero,dist_original,height_original]
    #tck_final, u_final= interpolate.splprep(coord_original)

    f = interpolate.interp1d(x=dist_original,y=height_original,kind='linear')
    dist_interp = np.linspace(start=dist_original[0],stop=dist_original[-1],num=Asmooth_len+1)
    height_interp = f(dist_interp)
    #interpolate.linear(, tck_final)
    #dist_interp.extend(list(new[1]))
    #height_interp.extend(list(new[2]))
    #height_interp = new
    print("已完成 linear 插值，范围",'0',Asmooth_len)

    print("-----------------------------")
    print("X_interp 前10个记录：")
    print(height_interp[0:10])
    coord_interp = [dist_interp,height_interp]
    #save_df(coord_interp)
    return coord_interp


def interp_3D_XYH(Asmooth_len,SmoothSize,X_original,Y_original,height_original,dist_original):
    X_interp = []
    Y_interp = []
    height_interp = []
    # 将全长拆开为 2 * window_size m 的小段
    segment_num = round(Asmooth_len / SmoothSize)
    segment_last_len = Asmooth_len % SmoothSize
    
    tck = list(range(1,segment_num + 1))
    u = list(range(1,segment_num + 1))
    
    if Asmooth_len != SmoothSize:
        # 整段部分
        for i in range(1,segment_num):
            # coord_original 是 XYH 三维数组
            coord_original = [list(X_original)[SmoothSize*(i-1):SmoothSize*i],list(Y_original)[SmoothSize*(i-1):SmoothSize*i],list(height_original)[SmoothSize*(i-1):SmoothSize*i]]
            #now we get all the knots and info about the interpolated spline
            tck[i], u[i]= interpolate.splprep(coord_original)
            #here we generate the new interpolated dataset, 
            #increase the resolution by increasing the spacing, 500 in this example
            new = interpolate.splev(np.linspace(0,1,SmoothSize), tck[i])
            X_interp.extend(list(new[0]))
            Y_interp.extend(list(new[1]))
            height_interp.extend(list(new[2]))
            #print("i - len(X_interp)",i,len(X_interp))
            print("已完成第",i,"段，范围",SmoothSize*(i-1),SmoothSize*i)
        # 小尾巴部分
        
        coord_original = [list(X_original)[Asmooth_len - segment_last_len:Asmooth_len],list(Y_original)[Asmooth_len - segment_last_len:Asmooth_len],list(height_original)[Asmooth_len - segment_last_len:Asmooth_len]]
        tck_final, u_final= interpolate.splprep(coord_original)
        #here we generate the new interpolated dataset, 
        #increase the resolution by increasing the spacing, 500 in this example
        new = interpolate.splev(np.linspace(0,1,segment_last_len), tck_final)
        X_interp.extend(list(new[0]))
        Y_interp.extend(list(new[1]))
        height_interp.extend(list(new[2]))
        print("已完成小尾巴部分，范围",Asmooth_len - segment_last_len,Asmooth_len)
    
    # SmoothSize=len(X_original)
    else:
        coord_original = [list(X_original),list(Y_original),list(height_original)]
        tck_final, u_final= interpolate.splprep(coord_original)
        #here we generate the new interpolated dataset, 
        #increase the resolution by increasing the spacing, 500 in this example
        new = interpolate.splev(np.linspace(0,1,Asmooth_len), tck_final)
        X_interp.extend(list(new[0]))
        Y_interp.extend(list(new[1]))
        height_interp.extend(list(new[2]))
        print("已完成 pchip，范围",'0',Asmooth_len)

    coord_interp = [X_interp,Y_interp,height_interp,list(dist_original)]
    #save_df(coord_interp)
    return coord_interp