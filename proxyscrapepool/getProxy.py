# -*- coding: utf-8 -*-
# author: Luke
import grequests
import requests
from multiprocessing.dummy import Pool
import time
import hashlib
from proxyscrapepool import redis_store
from proxyscrapepool.settings import PROXY_QUEUE, PROXY_COLLECTOR, RETRY_TIMES
import pickle

class ProxyPool():
    def __init__(self):
        self.start_proxies = []
        self.retries_proxies = []
        self.ok_proxies = []

    def get_proxies(self, type):
        file_url = {
            "socks5": "https://api.proxyscrape.com?request=getproxies&proxytype=socks5&timeout=300&country=all&uptime=0",
            "socks4": "https://api.proxyscrape.com?request=getproxies&proxytype=socks4&timeout=100&country=all&uptime=0",
            "http": "https://api.proxyscrape.com?request=getproxies&proxytype=http&timeout=100&country=all&ssl=all&anonymity=all&uptime=0"      # 可手动调节timeout获取不同延迟ip
        }
        try:
            response = requests.get(file_url[type])
        except Exception as e:
            print("get nok", type)
            return

        proxy_list = [{"http":type + "://" + proxy, "https": type + "://" + proxy} for proxy in response.text.split(
    '\r\n')[:-1]]
        print("get ok", len(proxy_list), type)
        return proxy_list

    def error_handler(self, request, expection):
        proxy = request.kwargs.get('proxies')
        if proxy not in self.retries_proxies:
            self.retries_proxies.append(proxy)

    def valite_proxies(self, to_validate_proxies):
        print("ready to validate", len(to_validate_proxies))
        my_headers = {
            'User-Agent': 'Mozilla/5.0(iPhone;U;CPUiPhoneOS4_3_3likeMacOSX;en-us)AppleWebKit/533.17.9(KHTML,likeGecko)Version/5.0.2Mobile/8J2Safari/6533.18.5'
        }
        do_validate_requests = [
            grequests.get('https://www.baidu.com/', proxies=my_proxies, headers=my_headers, timeout=3) for my_proxies in to_validate_proxies
        ]
        response_result = grequests.map(do_validate_requests, size=80, exception_handler=self.error_handler)
        ok_response = [i for i,v in enumerate(response_result) if v]
        ok_validated_proxies = [to_validate_proxies[i] for i in ok_response]    # 可用代理
        for proxy in ok_validated_proxies:
            if proxy in self.retries_proxies:
                self.retries_proxies.remove(proxy)
        print("validate ok", len(ok_validated_proxies))
        return ok_validated_proxies

    def filter_proxies(self, to_filter_proxies):
        proxies = [pickle.dumps(proxy) for proxy in to_filter_proxies]
        existd_proxies = redis_store.smembers(PROXY_COLLECTOR)
        to_save_proxies = []
        for proxy in proxies:
            if proxy not in existd_proxies:
                to_save_proxies.append(proxy)
        print("filter ok", len(to_filter_proxies)-len(to_save_proxies))
        return to_save_proxies

    def save_proxies(self, to_save_proxies):
        try:
            pipe = redis_store.pipeline()
            pipe.sadd(PROXY_COLLECTOR, *to_save_proxies)
            pipe.lpush(PROXY_QUEUE, *to_save_proxies)
            pipe.execute()
        except Exception as e:
            print(e)
            print("save nok")
            return
        print('save ok', len(to_save_proxies))

    def type_run(self, type):
        proxies = self.get_proxies(type)
        self.start_proxies.extend(proxies)

    def process_run(self):
        start_time = time.time()
        print("程序已经启动")
        pool = Pool(processes=10)
        for protocol_type in ["socks5","socks4", "http"]:
        # for protocol_type in ["socks5"]:
            pool.apply_async(self.type_run, (protocol_type,))
        pool.close()
        pool.join()     # 等待子进程结束

        if self.start_proxies:
            ok_proxies = self.valite_proxies(self.start_proxies)
            self.ok_proxies.extend(ok_proxies)
        times = 0
        while times <= RETRY_TIMES and self.retries_proxies:
            ok_proxies = self.valite_proxies(self.retries_proxies)
            self.ok_proxies.extend(ok_proxies)
            times += 1
        if self.ok_proxies:
            to_save_proxies = self.filter_proxies(self.ok_proxies)
            if to_save_proxies:
                self.save_proxies(to_save_proxies)
        end_time = time.time()
        print("程序已经运行完毕，消耗时间为:%f" % (end_time - start_time))

if __name__ == '__main__':
    pp = ProxyPool()
    pp.process_run()