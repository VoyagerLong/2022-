# -*- coding: utf-8 -*-
"""
Created on Mon May 23 23:19:03 2022

@author: longj
"""

def mkdir(path):
    import os
    # 去除首位空格
    path=path.strip()
    # 去除尾部 \ 符号
    path=path.rstrip("\\")
    # 判断路径是否存在
    isExists=os.path.exists(path)
    if not isExists:
        # 如果不存在则创建目录
        os.makedirs(path)
        return True
    else:
        # 如果目录存在则不创建
        return False


mkpath = './output'
# 调用函数

mkdir(mkpath)