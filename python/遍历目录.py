#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

# Python 获取目录下的文件和目录名称

import os

dir = "h"

result = os.listdir(dir)

# result 是一个包含名称的列表

for n in result:
    if os.path.exists(dir+"\\"+n):
        if os.path.isfile(dir+"\\"+n):
            print(n, "file")
        if os.path.isdir(dir+"\\"+n):
            print(n, "dir")