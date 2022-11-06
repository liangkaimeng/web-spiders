#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2022/11/6 0006 22:08
# @Author  : LKM

# 导入库
import time
from multiprocessing import dummy


# 定义函数
def demo_func(num):
    for i in range(num):
        return i ** 2


if __name__ == "__main__":
    # 多处理demo函数
    start = time.time()
    processes = []
    lop_size = [10000000, 10000000, 10000000, 10000000, 10000000, 10000000, 10000000]
    p = dummy.Pool(4)
    p.map(demo_func, lop_size)
    p.close()
    p.join()
    end = time.time()
    print(end - start)
