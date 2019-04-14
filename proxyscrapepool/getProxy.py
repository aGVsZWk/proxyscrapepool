# -*- coding: utf-8 -*-
# author: Luke
import grequests
import requests
from multiprocessing.dummy import Pool
import time
import hashlib
from proxyscrapepool import redis_store
from proxyscrapepool.settings import PROXY_QUEUE, FILTER_COLLECTOR, PROXY_HASH_MAP


class ProxyPool():
    def __init__(self):
        self.ok_proxies = []

    def get_proxies(self, type):
        file_url = {
            "socks5": "https://api.proxyscrape.com?request=getproxies&proxytype=socks5&timeout=500&country=all&uptime=0",
            "socks4": "https://api.proxyscrape.com?request=getproxies&proxytype=socks4&timeout=200&country=all&uptime=0",
            "http": "https://api.proxyscrape.com?request=getproxies&proxytype=http&timeout=200&country=all&ssl=all&anonymity=all&uptime=0"      # 可手动调节timeout获取不同延迟ip
        }
        try:
            response = requests.get(file_url[type])
        except Exception as e:
            response = None
        proxy_list = [{"type":type, "ip_port":proxy} for proxy in response.text.split('\r\n')[:-1]]
        return proxy_list

    def valite_proxies(self, to_validate_proxies):
        my_headers = {
            'User-Agent': 'Mozilla/5.0(iPhone;U;CPUiPhoneOS4_3_3likeMacOSX;en-us)AppleWebKit/533.17.9(KHTML,likeGecko)Version/5.0.2Mobile/8J2Safari/6533.18.5'
        }
        protocol_type = {
            "socks5": {"http": "socks5://", "https": "socks5://"},
            "socks4": {"http": "socks4://", "https": "socks4://"},
            "http": {"http": "http://", "https": "https://"}
        }
        my_proxies_list = [
            {key: value + proxy['ip_port'] for key, value in protocol_type[proxy['type']].items()} for proxy in to_validate_proxies
        ]
        do_validate_requests = [
            grequests.get('https://www.baidu.com/', proxies=my_proxies, headers=my_headers, timeout=3) for my_proxies in my_proxies_list
        ]
        response_result = grequests.map(do_validate_requests, size=80)
        ok_response = [i for i,v in enumerate(response_result) if v]
        nok_response = [i for i,v in enumerate(response_result) if v is None]
        ok_validated_proxies = [to_validate_proxies[i] for i in ok_response]    # 可用代理
        nok_validated_proxies = [to_validate_proxies[i] for i in nok_response]    # 可用代理
        return ok_validated_proxies, nok_validated_proxies


    def filter_proxies(self, to_filter_proxies):
        to_generate_figer = [{"protocol_type": proxy['type'], "ip": proxy['ip_port'][:proxy['ip_port'].rfind(":")], "port": proxy['ip_port'][proxy['ip_port'].rfind(":")+1:], "delay":0, "is_outwall":True} for proxy in to_filter_proxies]
        figer_print_list = redis_store.smembers(FILTER_COLLECTOR)
        to_add_collector = []
        to_add_queue = []
        to_add_hashmap = []
        for proxy in to_generate_figer:
            sha1 = hashlib.sha1()
            sha1.update(str(proxy).encode())
            proxy_figer_print = sha1.hexdigest()
            if proxy_figer_print not in figer_print_list:
                to_add_collector.append(proxy_figer_print)
                to_add_queue.append(proxy_figer_print)
                to_add_hashmap.append({"figer": proxy_figer_print,"proxy": proxy})
        if to_add_collector:
            redis_store.sadd(FILTER_COLLECTOR, *to_add_collector)
            redis_store.lpush(PROXY_QUEUE, *to_add_queue)
            for add_hash_map in to_add_hashmap:
                redis_store.hset(PROXY_HASH_MAP, add_hash_map['figer'], add_hash_map['proxy'])
        return len(to_add_hashmap)

    def type_run(self, type):
        proxies = self.get_proxies(type)
        retry_times = 0
        retry_proxies = []
        if retry_times == 0:
            temp_ok_proxies, retry_proxies = self.valite_proxies(proxies)
            self.ok_proxies.extend(temp_ok_proxies)
            retry_times += 1
        while retry_times < 3:
            # print(type, retry_times)
            temp_ok_proxies, retry_proxies = self.valite_proxies(retry_proxies)
            self.ok_proxies.extend(temp_ok_proxies)
            retry_times += 1

    def process_run(self):
        start_time = time.time()
        pool = Pool(processes=10)
        for protocol_type in ["socks5","socks4", "http"]:
        # for protocol_type in ["socks5"]:
            pool.apply_async(self.type_run, (protocol_type,))
        print("程序已经启动")
        pool.close()
        pool.join()     # 等待子进程结束
        add_proxy_nums = self.filter_proxies(self.ok_proxies)
        end_time = time.time()
        print("程序已经运行完毕，消耗时间为:%f，增加的代理数量为%d" % (end_time - start_time, add_proxy_nums))

if __name__ == '__main__':
    pp = ProxyPool()
    pp.process_run()
