# -*- coding: utf-8 -*-
# author: Luke
import pickle

import requests
import time

from proxyscrapepool import redis_store
from proxyscrapepool.settings import PROXY_QUEUE, INTERVAL_TIME


class AdvanceProxy():
    def __init__(self):
        self.headers = {
            'User-Agent': 'Mozilla/5.0(iPhone;U;CPUiPhoneOS4_3_3likeMacOSX;en-us)AppleWebKit/533.17.9(KHTML,likeGecko)Version/5.0.2Mobile/8J2Safari/6533.18.5'
        }
        self.url1 = 'https://www.baidu.com/'
        self.url2 = None

    def get_proxy(self):
        temp_proxy = redis_store.lpop(PROXY_QUEUE)
        proxy = pickle.loads(temp_proxy)
        print("get proxy", proxy)
        return proxy

    def proxy_is_ok(self, proxy):
        times = 0
        is_ok = False
        while times < 3 and not is_ok:
            try:
                response = requests.get(self.url1, headers=self.headers, proxies=proxy)
            except Exception as e:
                print("failure times", times+1, proxy)
                response = False
            if response:
                response.close()
                is_ok = True
            times += 1
            time.sleep(INTERVAL_TIME)
        print("is ok?", is_ok, proxy)
        return is_ok

    def update_queue(self, proxy):
        to_save_proxy = pickle.dumps(proxy)
        redis_store.rpush(PROXY_QUEUE, to_save_proxy)
        print("update ok", proxy)

    def run(self):
        while True:
            proxy = self.get_proxy()
            if self.proxy_is_ok(proxy):
                self.update_queue(proxy)
            time.sleep(INTERVAL_TIME)


if __name__ == '__main__':
    ap = AdvanceProxy()
    ap.run()