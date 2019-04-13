# -*- coding: utf-8 -*-
# author: Luke
# redis并发测试
import hashlib
import time
from redis import Redis
from multiprocessing.dummy import Pool
from proxyscrapepool import redis_store

from proxyscrapepool.settings import PROXY_QUEUE, FILTER_COLLECTOR
import os
# redis_store = Redis(host="localhost", port=6379, db=0)
redis_store = redis_store
class Test():
    def test(self):
        list = []
        a = 0
        while a < 100:
            list.append(a)
            a += 1
        redis_store.lpush("htest", *list)

        print("finish", os.getpid())

    def run(self):
        pool = Pool(processes=3)
        for i in range(10):
            pool.apply_async(self.test)
        pool.close()
        pool.join()

if __name__ == '__main__':
    t = Test()
    t.run()