# -*- coding: utf-8 -*-
"""
Created on Mon May  2 09:39:02 2022

@author: longj
"""

import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
import matplotlib
matplotlib.rcParams['font.sans-serif'] = ['SimHei']
matplotlib.rcParams['axes.unicode_minus'] =False

'''
*********** r(P=20)_poccurence 散点图的高斯拟合 ********************
*********** 定义 DRAGANN 的高斯拟合函数（自定义函数） ***************
'''
def Gauss(x, Parameter1_amp, Parameter2_cent):
    # Parameter1_amp 为 拟合出的高斯曲线的 peak 强度（高度）
    # Parameter2_cent 为 拟合出的高斯曲线的 peak 中线（平均值μ）
    # Parameter3_std 为 Xdata list 的 Std
    Parameter3_std =np.std(x) 
    y = Parameter1_amp * np.exp((-1 * ((x - Parameter2_cent)**2)) / 2 / Parameter3_std**2)
    return y

'''
********************** 平移纵坐标 **********************
'''
def substract_move(x):
    return x - 800
'''
********************** 求 y1、y2 交点 **********************
'''
def y1(x,arry):
    y1 = arry[0] * np.exp((-1 * ((x - arry[1])**2)) / 2 / arry[2]**2)
    return y1

def y2(x,arry):
    y2 = arry[3] * np.exp((-1 * ((x - arry[4])**2)) / 2 / arry[5]**2)
    return y2

def Y1Y2_intersect(arry_len,arry):
    x = list(range(0, arry_len, 1))
    for i in x:
        if abs(y1(i,arry) - y2(i,arry)) < 0.01:
            break
    return i

'''
*********** 读取数据，并排序 ***********************
'''
id_pnum = np.genfromtxt("./r_poccurence.txt",delimiter = ",")
arry_len = len(id_pnum)

tuple_id_pnum = [tuple(x) for x in id_pnum.tolist()]

# 在进行高斯曲线拟合前需对 Xdata & 对应的 Ydata 进行排序，
# 否则会生成非常奇怪的拟合曲线
sort_id_pnum = sorted(tuple_id_pnum)


pnum_in_r = np.zeros(arry_len)
occurence = np.zeros(arry_len)
for i in range(arry_len):
    pnum_in_r[i] = sort_id_pnum[i][0]
    occurence[i] = sort_id_pnum[i][1]

'''
*********** 手动分段，进行高斯拟合 ***************
------------ Noise Peak 拟合 ----------------
'''
# 输出参数
arry = np.zeros(7)

fig=plt.figure(figsize=(10,6))
ax=fig.add_axes([0.1,0.2,0.8,0.7])
# 点统计图绘制
#plt.xlabel("P = 20 时的搜索半径")
plt.ylabel("搜索半径统计频次 (次)")
plt.ylim(-20, 250)
plt.plot(pnum_in_r, occurence, 'c.', label='ATL03 光子')

# 分段
xdata1 = pnum_in_r[450:770]
ydata1 = occurence[450:770]
plt.plot(xdata1, ydata1, 'b.', label='Noise 峰')

# 对散点拟合曲线，获得参数fit_A，fit_B
parameters, covariance = curve_fit(Gauss, xdata1, ydata1)

fit_A1 = parameters[0]
fit_B1 = parameters[1]
arry[0] = round(fit_A1,2)
arry[1] = round(fit_B1,2)
arry[2] = round(np.std(xdata1),2)

# 计算出参数后，画拟合曲线
fit_y1 = Gauss(xdata1, fit_A1, fit_B1)
# plt.plot(xdata1, fit_y1, 'r--', label='NoisePeak_fit')
plt.plot(xdata1, fit_y1, 'r--', label='Noise 峰拟合')
plt.legend()

# 插入公式 text
plt.text(300, 200,r"occurences = $ae^{\frac{-(x-b)^2}{2c^2}}$",fontsize=16)
#plt.text(0, 200, str(round(fit_A1,2)) + r'$\Gamma(z) = \int_0^\infty t^{z-1}e^{-t}dt\,.$', fontsize=10)
'''
-------------- Signal Peak 拟合 --------------
'''

# 分段
xdata2 = pnum_in_r[800:950]
xdata2_move = list(map(substract_move, pnum_in_r[800:950]))
ydata2 = occurence[800:950]
plt.plot(xdata2, ydata2, 'g.', label='Signal峰')

# 对散点拟合曲线，获得参数fit_A，fit_B
parameters, covariance = curve_fit(Gauss, xdata2_move, ydata2)

fit_A2 = parameters[0]
fit_B2 = parameters[1]
arry[3] = round(fit_A2,2)
arry[4] = round(fit_B2,2)
arry[5] = round(np.std(xdata2),2)

# 计算出参数后，画拟合曲线
fit_y2 = Gauss(xdata2_move, fit_A2, fit_B2)
plt.plot(xdata2, fit_y2, 'r-', label='Signal 峰拟合')
plt.legend()

threshold = Y1Y2_intersect(arry_len,arry)
arry[6] = (threshold)
# 插入公式 text
plt.xlabel("搜索邻域中的光子数量 (个)"+'\n\n其中 Noise 峰拟合系数 a ='+ str(round(fit_A1,2)) + "  b =" + str(round(fit_B1,2)) + "  c =" + str(round(np.std(xdata1),2))+'\n其中最高 Signal 峰拟合系数 a ='+ str(round(fit_A2,2)) + "  b =" + str(round(fit_B2,2)) + "  c =" + str(round(np.std(xdata2),2)))

plt.savefig('Gauss_fit.png')
np.savetxt('parameters.txt', arry)
