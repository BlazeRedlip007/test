#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

# 图像数据绘制到三维坐标

from PIL import Image
import numpy
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

def getImageDataBlackWhite(fileName, resizex = None, resizey = None):
    """打开图片返回图片像素(黑白)"""
    image = Image.open(fileName)
    image = image.convert("L")
    if None != resizex and None != resizey:
        image = image.resize([resizex, resizey], Image.ANTIALIAS)
    return numpy.asarray(image)

def draw3DList(data):
    """3D的List按照位置绘制到3维坐标轴"""
    X = []
    Y = []
    Z = []
    for i in range(len(data)):
        for j in range(len(data[i])):
            X.append(i)
            Y.append(j)
            Z.append(data[i][j])
    fig = plt.figure()
    ax = fig.add_subplot(1, 1, 1, projection='3d')
    ax.plot_trisurf(X, Y, Z)
    plt.show()

imageFile = "15.jpg"
imageWidth = 100
imageHigh = 100

data = getImageDataBlackWhite(imageFile, imageWidth, imageHigh)
draw3DList(data)