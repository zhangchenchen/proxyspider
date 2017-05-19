#!/usr/bin/env python
# -*- coding: utf-8 -*-

import requests
import Queue
import re
from random import choice
import threading


from config import (
    PROXY_SITES, OUTPUT_FILE, USER_AGENT_LIST, RETRY_NUM, TIME_OUT, TEST_URL, PROXY_REGX
)   


class ProxySpider(object):
    """docstring for Fetcher"""
    def __init__(self):
        
        self.fetch_finish = False
        self.proxy_queue = Queue.Queue()


    def in_proxy_queue(self):
        for site in PROXY_SITES:
            resp  = self._fetch(site)
            if resp is not None and resp.status_code == 200:
                proxy_list = self._extract(resp)
                for proxy in proxy_list:
                    print "Get proxy %s and get into queue" % (proxy)
                    self.proxy_queue.put(proxy)
        print "Success! get all proxy in queue!"
        self.fetch_finish = True

    def out_proxy_queue(self):
        while self.fetch_finish == False or not self.proxy_queue.empty():
            print "Begin to get proxy from queue"
            proxy = self.proxy_queue.get()
            check_proxy = self._fetch(TEST_URL, proxy)
            if check_proxy is not None and check_proxy.status_code == 200:
                self._output_proxy(proxy)


    def _fetch(self, url, proxy=None):
        kwargs = {
            "headers": {
                "User-Agent": choice(USER_AGENT_LIST),
            }, 
            "timeout": TIME_OUT        
        }
        resp = None
        for i in range(RETRY_NUM):
            try:
                if proxy is not None:
                    kwargs["proxies"] = {
                            "http": proxy}
                resp = requests.get(url, **kwargs)
                break
            except Exception as e:
                print "fetch %s  failed!\n%s , retry %d" % (url, str(e), i)
                continue
        return resp


    def _extract(self, resp):
        proxy_list = []
        if resp is not None:
            proxy_list = re.findall(PROXY_REGX, resp.text)
        return proxy_list


    def _output_proxy(self, proxy):
        if not proxy:
            return 
        with open(OUTPUT_FILE, "a") as proxy_file:
            print "Success,write to proxy_list"
            proxy_file.write("%s\n" % proxy)
   

    def run(self):
        
        threads = []
        in_proxy_queue_thread = threading.Thread(target = self.in_proxy_queue)
        #in_proxy_queue_thread.start()

        out_proxy_queue_threads = [threading.Thread(target = self.out_proxy_queue) for i in range(100)]
        #out_proxy_queue_thread = threading.Thread(target = self.out_proxy_queue)
        threads.append(in_proxy_queue_thread)
        threads.extend(out_proxy_queue_threads)
        [thread.start() for thread in threads]
        [thread.join() for thread in threads]



def main():
    spider = ProxySpider()
    spider.run()


if __name__ == "__main__":
    main()