#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2022/11/6 0006 23:35
# @Author  : LKM

import requests
import time
from multiprocessing.dummy import Pool as ThreadPool
from multiprocessing import Pool

tpool = ThreadPool()
ppool = Pool()

data = [10000] * 10


def get_jiecheng(num):
    res = 1
    for i in range(num):
        res *= (i + 1)


time_7 = time.time()
for i in data:
    get_jiecheng(i)
time_8 = time.time()
print("计算密集型：for 循环使用时间", time_8 - time_7)

time_9 = time.time()
tpool.map(get_jiecheng, data)
time_10 = time.time()
print("计算密集型：多线程使用时间", time_10 - time_9)

time_11 = time.time()
ppool.map(get_jiecheng, data)
time_12 = time.time()
print("计算密集型：多进程使用时间", time_12 - time_11)

time_13 = time.time()
ppool.map_async(get_jiecheng, data)
time_14 = time.time()
print("计算密集型：多进程异步使用时间", time_14 - time_13)
