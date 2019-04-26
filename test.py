# -*- coding: utf-8 -*-
# author: Luke
# redis并发测试
import hashlib
import time

import requests
from redis import Redis
from multiprocessing.dummy import Pool
from proxyscrapepool import redis_store
from fake_useragent import UserAgent

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

class newTest(Test):
    def run(self):

        self.headers = {'User-Agent': UserAgent().random}
        print(self.headers)
        self.url1 = "https://www.google.com.hk/"
        self.url2 = "https://www.baidu.com"
        self.url3 = "https://www.facebook.com"
        self.url4 = "https://twitter.com/login?lang=zh-cn"
        try:
            response = requests.get(self.url3, proxies={'http': 'socks5://195.96.77.186:5555', 'https': 'socks5://195.96.77.186:5555'}, headers=self.headers)
            print(response.text)
        except Exception as e:
            print(e)



if __name__ == '__main__':
    t = newTest()
    t.run()