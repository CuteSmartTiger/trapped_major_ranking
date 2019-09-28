#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2019/9/28 16:16
# @Author  : liuhu
# @Site    : 
# @File    : redis.py
# @Software: PyCharm
# @github  :https://github.com/Max-Liuhu
import redis

host = '192.168.17.133'
pool = redis.ConnectionPool(host=host, port=6379, db=0)
rdb = redis.Redis(connection_pool=pool)
# rdb.set('物理','分数',1)
# print(rdb.get('物理').decode('utf-8'))

