#!/usr/bin/env python
# -*- coding: utf-8 -*-
# -*- author by pekingzcc -*-
# -*- date : 2017-05-19 -*-



import requests
import Queue
import re
from random import choice
import threading
import qiniuupload


from config import (
    PROXY_SITES, OUTPUT_FILE, USER_AGENT_LIST, RETRY_NUM, TIME_OUT, TEST_URL, PROXY_REGX
)   


class ProxySpider(object):
    """代理IP 爬虫"""
    def __init__(self):
        
        self.fetch_finish = False
        self.proxy_queue = Queue.Queue()
        self.lock = threading.Lock()

    """
       起一个线程将采集到的所有代理IP写入一个queue中
    """
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

    """
        起多个线程取出queue中的代理IP 测试是否可用
    """
    def out_proxy_queue(self):
        while self.fetch_finish == False or not self.proxy_queue.empty():
            print "Begin to get proxy from queue"
            proxy = self.proxy_queue.get()
            check_proxy = self._fetch(TEST_URL, proxy)
            if check_proxy is not None and check_proxy.status_code == 200:
                self._output_proxy(proxy)

    """ 抓取代理网站函数"""
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

    """ 解析抓取到的内容，得到代理IP"""
    def _extract(self, resp):
        proxy_list = []
        if resp is not None:
            proxy_list = re.findall(PROXY_REGX, resp.text)
        return proxy_list

    """ 输出可用的代理IP """
    def _output_proxy(self, proxy):
        if not proxy:
            return
        with self.lock:     
            with open(OUTPUT_FILE, "a") as proxy_file:
                print "Success,write to proxy_list"
                proxy_file.write("%s\n" % proxy)
   
    """一个线程用于抓取，多个线程用于测试"""
    def run(self):
        
        threads = []
        in_proxy_queue_thread = threading.Thread(target = self.in_proxy_queue)
        out_proxy_queue_threads = [threading.Thread(target = self.out_proxy_queue) for i in range(100)]
        threads.append(in_proxy_queue_thread)
        threads.extend(out_proxy_queue_threads)
        [thread.start() for thread in threads]
        [thread.join() for thread in threads]



def main():
    spider = ProxySpider()
    spider.run()
    """上述任务执行完成后，上传结果到七牛,注意在上传之前先要配置七牛的认证"""
    #uploadtoqiniu = qiniuupload.uploadToqiniu()
    #uploadtoqiniu.upload() 


if __name__ == "__main__":
    main()