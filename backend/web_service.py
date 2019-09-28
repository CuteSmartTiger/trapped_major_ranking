#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2019/9/28 11:17
# @Author  : liuhu
# @Site    : 
# @File    : web_service.py
# @Software: PyCharm
# @github  :https://github.com/Max-Liuhu


from flask import Flask
from flask_restful import Api, Resource
from flask import request

from backend.const.major_name_map import get_ch_major_name_by_en

app = Flask(__name__)
api = Api(app)

from backend.config import rdb


def get_redis_pool_name(name):
    """
    if the name is rank,the key is major,the value is index,
    if the name is detail,the key is major,values are majors' detail
    if name is sorted:set,key is major,the value is index
    return redis pool name for hash key
    """
    return "major:{}".format(name)


class Major(Resource):
    def get(self):
        return 'test'

    def post(self):
        major_list = get_ch_major_name_by_en.keys()
        name = get_redis_pool_name('rank:sorted:set')
        # name = get_redis_pool_name('rank')
        for major in major_list:
            rdb.zadd(name, {major: 0})
        res = rdb.zrange(name, 0, 10)
        print(res)

    def post_test(self):
        """init major index"""
        major_list = get_ch_major_name_by_en.keys()
        name = get_redis_pool_name('rank')
        pipe = rdb.pipeline()
        for major in major_list:
            pipe.hset(name, major, 0)
        res = pipe.execute()
        print(res)
        return 'success'

    def put(self):
        return

    def delete(self):
        return


class MajorRanking(Resource):
    def get(self):
        name = get_redis_pool_name('rank:sorted:set')
        res = rdb.zrange(name, 0, 10, desc=True, withscores=True)
        print(res)
        result = {}
        for key, value in res:
            result[key.decode("utf-8")] = value
        return result

    # def get_test(self):
    #     name = get_redis_pool_name('rank')
    #     res = rdb.hgetall(name)
    #     print(type(res))
    #     print(res)

    def post(self):
        key = request.args['major']
        major_list = get_ch_major_name_by_en.keys()
        if key not in major_list:
            return '没有这个专业'
        name = get_redis_pool_name('rank:sorted:set')
        res = rdb.zincrby(name, 1, key)
        # index = rdb.hget(name, key)
        # return index.decode("utf-8"), '201 index'
        print(res)
        return '201 index'

    def put_test(self):
        major_list = get_ch_major_name_by_en.keys()
        key = request.args['major']
        if key not in major_list:
            return '没有这个专业'
        name = get_redis_pool_name('rank')
        rdb.hincrby(name, key, amount=1)
        index = rdb.hget(name, key)
        return index.decode("utf-8"), '201 index'


api.add_resource(Major, '/major/', endpoint='major')
api.add_resource(MajorRanking, '/major_ranking/', endpoint='major_ranking')

if __name__ == '__main__':
    app.run(debug=True)
