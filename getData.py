# -*- coding: utf-8 -*-
# author: Luke
import grequests
import requests
from multiprocessing import Pool
import time
from app import redis_store


class ProxyPool():
    def __init__(self):
        # self.con = redis_store()
        pass

    def get_proxies(self, type):
        file_url = {
            "socks5": "https://api.proxyscrape.com?request=getproxies&proxytype=socks5&timeout=300&country=all&uptime=0",
            "socks4": "https://api.proxyscrape.com?request=getproxies&proxytype=socks4&timeout=100&country=all&uptime=0",
            "http": "https://api.proxyscrape.com?request=getproxies&proxytype=http&timeout=100&country=all&ssl=all&anonymity=all&uptime=0"
        }

        try:
            response = requests.get(file_url[type])
        except Exception as e:
            response = None
        # file_name = time.strftime("%Y-%m-%d-%H-%M-%S-",time.localtime(time.time())) + type + ".txt"
        # f = open(file_name, "ab")
        # f.write(response.content)
        # return f
        proxy_list = response.text.split('\r\n')[:-1]
        return proxy_list

    def valite_proxies(self, to_validate_proxies, type):    # todo 增加回调，对失败的ip进行再次筛选
        my_headers = {
            'User-Agent': 'Mozilla/5.0(iPhone;U;CPUiPhoneOS4_3_3likeMacOSX;en-us)AppleWebKit/533.17.9(KHTML,likeGecko)Version/5.0.2Mobile/8J2Safari/6533.18.5'}
        protocol_type = {
            "socks5": {"http": "socks5://", "https": "socks5://"},
            "socks4": {"http": "socks4://", "https": "socks4://"},
            "http": {"http": "http://", "https": "https://"}
        }
        my_proxies_list = [{key: value + proxy for key, value in protocol_type[type].items()} for proxy in
                           to_validate_proxies]
        print("待验证代理数量:", len(my_proxies_list), "爬取的类型:", type)
        start_time = time.time()
        do_validate_requests = [
            # grequests.get('https://www.baidu.com/', proxies=my_proxies, timeout=10, headers=my_headers) for my_proxies
            grequests.get('https://www.baidu.com/', proxies=my_proxies, headers=my_headers, timeout=3) for my_proxies
            in my_proxies_list
        ]
        response_result = grequests.map(do_validate_requests, size=80)
        ok_response = [i for i,v in enumerate(response_result) if v]
        nok_response = [i for i,v in enumerate(response_result) if v is None]
        ok_validated_proxies = [to_validate_proxies[i] for i in ok_response]    # 可用代理
        nok_validated_proxies = [to_validate_proxies[i] for i in nok_response]    # 可用代理
        end_time = time.time()
        print("可用代理数量:",len(ok_validated_proxies), "爬取的类型:", type)
        print(ok_validated_proxies)
        print("耗费时间:", end_time - start_time)
        return ok_validated_proxies, nok_validated_proxies


    def filter_proxies(self, to_filter_proxies, type):    # todo 增加类型，速度
        try:
            proxies_set = redis_store.lrange("proxies", 0, -1)  # todo 去重改成redis的集合，存储改成hashmap，顺序改成列表
        except Exception:
            proxies_set = {}
        to_save_proxies = [proxy for proxy in to_filter_proxies if proxy not in proxies_set]
        if to_save_proxies:
            redis_store.lpush("proxies", *to_save_proxies)
        print("存储的代理数量:", len(to_save_proxies), "爬取的类型:", type)


    def type_run(self, type):
        proxies = self.get_proxies(type)
        ok_proxies, _ = self.valite_proxies(proxies, type)
        self.filter_proxies(ok_proxies, type)

    def process_run(self):
        pool = Pool(processes=3)
        for protocol_type in ["socks5", "socks4", "http"]:
            pool.apply_async(self.type_run, (protocol_type,))
        print("进程池已经启动")
        pool.close()
        pool.join()     # 等待子进程结束
        print("已经爬取完成")



