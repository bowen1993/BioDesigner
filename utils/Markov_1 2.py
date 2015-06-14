# -*- coding: cp936 -*-
# 实现一阶马尔科夫模型

import numpy as np
import os
import django
import sys

pro_dir = os.getcwd()
sys.path.append(pro_dir)
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "BioDesigner.settings")

from design.models import parts



def markov(data_set):
    """
      实现1阶马尔科夫模型的参数训练，
      返回转移概率矩阵（二维数组）和元素元组
      
      data_set：用于训练的数据集（二维列表）
    """
    elements = set()
    for data in data_set:
        tmp = set(data)
        elements |= tmp
    elements = tuple(elements)

    n = len(elements)
    A = np.zeros((n, n))
    count = np.zeros((n, 1))
    # 计算状态转移概率
    for data in data_set:
        for i in range(len(data)-1):
            a = elements.index(data[i])
            b = elements.index(data[i+1])
            A[a][b] +=1
            count[a] += 1
    for i in range(n):
        if count[i][0] == 0:
            count[i][0] += 1.0      # 防止下面出现除0错误
    A = A / count
    
    return A, elements


def initial(m, n):
    """
    初始化概率数组和路径数组

    :param m: 行数
    :param n: 列数
    :return: 初始化后的dp数组和path数组
    """
    dp = np.tile(-1.0, (m+1, n))    # (m+1，n)，-1代表概率尚未计算
    path = np.tile(-1.0, (m+1, n))  # (m+1，n)，-1代表到达路径结尾

    for i in range(n):
        dp[m][i] = 1       # 如果一次性预测整条链，可以用结束概率作为dp初始化的值
    return dp, path


def print_path(elements, s, path):
    """
    输出预测序列

    :param elements: 元素元组
    :param s: 路径开始的索引
    :param path: 存储路径信息的二维数组
    :return: None
    """
    for step in path:
        t = int(step[s])
        print elements[t],
        s = t
    print


def predict(m, s, A, elements):
    """
      实现对序列s的预测，时间复杂度O(n^2*m)

      m：需要预测的数量
      s：已给出的观测序列
      A：状态转移矩阵
      elements：元素元组
    """
    # 初始化dp数组和路径数组
    n = len(elements)
    dp, path = initial(m, n)
    
    # 递推计算dp数组
    for i in range(m-1, 0, -1):          # dp数组的第0行单独计算，因为只需计算一个
        for j in range(n):
            for k in range(n):
                if dp[i][j] < A[j][k]*dp[i+1][k]:
                    dp[i][j] = A[j][k]*dp[i+1][k]
                    path[i][j] = k

    # 对第0行进行计算
    c = elements.index(s)
    for k in range(n):
        if dp[0][c] < A[c][k]*dp[1][k]:
            dp[0][c] = A[c][k]*dp[1][k]
            path[0][c] = k

    if dp[0][c] == 0:
        print u"无法进行预测！"
        return False
    else:
        print_path(elements, c, path)
        return True

def getDataSet():
    partList = list()
    partInList = parts.objects.all()[:5000]
    for p in partInList:
        subStr = p.deep_u_list
        if not subStr or len(subStr) == 0:
            continue
        if subStr.startswith('_'):
            subStr = subStr[1:]
        if subStr.endswith('_'):
            subStr = subStr[:-1]
        subList = subStr.split('_')
        partList.append(subList)
    return partList

if __name__ == "__main__":
    django.setup()
    data_set = getDataSet()
    A, elements = markov(data_set)
    print 'a get'
    predict(2, '151', A, elements)    
    
