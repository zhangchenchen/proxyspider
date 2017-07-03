#!/usr/bin/env python
# -*- coding: utf-8 -*-
# -*- author by pekingzcc -*-
# -*- date : 2017-05-19 -*-



import requests
import Queue
import re
from lxml import etree
from lxml import html
from random import choice
import threading
import time
import qiniuupload


from config import (
    PROXY_SITES_BY_REGX, PROXY_SITES_BY_XPATH, OUTPUT_FILE, USER_AGENT_LIST, RETRY_NUM, TIME_OUT, TEST_URL, CHECK_PROXY_XPATH
)   


class Proxy(object):
    def __init__(self, ip_port, anonymity_level, proxy_type='HTTP'):
        self.ip_port = ip_port
        self.proxy_type = proxy_type
        self.anonymity_level = anonymity_level
    def __eq__(self, other):  
        if isinstance(other, Proxy):  
            return ((self.ip_port == other.ip_port) and (self.proxy_type == other.proxy_type) and (self.anonymity_level == other.anonymity_level))    
        else:  
            return False  
      
    def __hash__(self):  
        return hash(self.ip_port + " " + self.proxy_type + " " + self.anonymity_level) 

class ProxySpider(object):
    """代理IP 爬虫"""
    def __init__(self):
        
        self.fetch_finish = False
        self.proxy_queue = Queue.Queue()
        self.lock = threading.Lock()
        self.good_proxy = set()

    """
       起一个线程将采集到的所有代理IP写入一个queue中
    """
    def in_proxy_queue(self):
        '''根据正则直接获取代理IP 部分'''
        for site in PROXY_SITES_BY_REGX['urls']:
            resp  = self._fetch(site)
            if resp is not None and resp.status_code == 200:
                try:
                    proxy_list = self._extract_by_regx(resp)
                    for proxy in proxy_list:
                        print "Get proxy %s and get into queue" % (proxy)
                        self.proxy_queue.put(proxy)
                except Exception as e:
                    continue
        '''根据xpath 获取代理IP 部分'''
        for sites in PROXY_SITES_BY_XPATH:
            for site in sites['urls']:
                resp  = self._fetch(site)
                if resp is not None and resp.status_code == 200:
                    try:
                        proxy_list = self._extract_by_xpath(resp, sites['ip_xpath'], sites['port_xpath'])
                        for proxy in proxy_list:
                            print "Get proxy %s and get into queue" % (proxy)
                            self.proxy_queue.put(proxy)
                    except Exception as e:
                        continue                  
        print "Get all proxy in queue!"        
        self.fetch_finish = True


    """
        起多个线程取出queue中的代理IP 测试是否可用
    """
    def out_proxy_queue(self):

        while not self.proxy_queue.empty() or self.fetch_finish == False:
            print "Begin to get proxy from queue"
            proxy = self.proxy_queue.get()
            check_proxy = self._fetch(TEST_URL, proxy)
            if check_proxy is not None and check_proxy.status_code == 200:
                resp_str = html.fromstring(check_proxy.text)
                http_via = resp_str.xpath(CHECK_PROXY_XPATH['HTTP_VIA'])              
                http_x_forward_for = resp_str.xpath(CHECK_PROXY_XPATH['HTTP_X_FORWARDED_FOR'])
                if http_via[0] == "anonymous / none" and http_x_forward_for[0] == "anonymous / none":
                    kwargs = {"ip_port": proxy, "anonymity_level": "Elite"}
                elif http_via[0] and http_x_forward_for[0]:
                    kwargs = {"ip_port": proxy, "anonymity_level": "Anonymous"}
                else:
                    kwargs = {"ip_port": proxy, "anonymity_level": "Transparent"}
                proxy_instance = Proxy(**kwargs)
                self._deduplicate_proxy(proxy_instance)
              

    """ 抓取代理网站函数"""
    def _fetch(self, url, proxy=None):
        kwargs = {
            "headers": {
                "User-Agent": choice(USER_AGENT_LIST),
            }, 
            "timeout": TIME_OUT,
            "verify": False,       
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
                time.sleep(1)
                continue
        return resp

    """ 根据解析抓取到的内容，得到代理IP"""
    def _extract_by_regx(self, resp):
        proxy_list = []
        if resp is not None:
            proxy_list = re.findall(PROXY_SITES_BY_REGX['proxy_regx'], resp.text)
        return proxy_list

    def _extract_by_xpath(self, resp, ip_xpath, port_xpath):
        #import pdb;pdb.set_trace()
        proxy_list = []
        if resp is not None:
            resp = html.fromstring(resp.text)
            ip_list = resp.xpath(ip_xpath)
            port_list = resp.xpath(port_xpath)
            for i in range(len(ip_list)):
                proxy = ip_list[i] + ":" + port_list[i]
                proxy_list.append(proxy)
        return proxy_list        


    """ 输出可用的代理IP 到 set 中以达到去重"""
    def _deduplicate_proxy(self, proxy):
        if not proxy:
            return
        with self.lock:
            self.good_proxy.add(proxy)     

            
    """ 持久化可用代理IP """
    def output_proxy(self):
        with open(OUTPUT_FILE, "w+") as proxy_file:
            proxy_file.write("proxy  type  anonymity_level\n" )           
            for proxy in self.good_proxy:
                print "Write %sto proxy_list.txt" % proxy 
                proxy_file.write("%s  %s  %s\n" % (proxy.ip_port, proxy.proxy_type, proxy.anonymity_level))

    """一个线程用于抓取，多个线程用于测试"""
    def run(self):       
        threads = []
        in_proxy_queue_thread = threading.Thread(target = self.in_proxy_queue)
        out_proxy_queue_threads = [threading.Thread(target = self.out_proxy_queue) for i in range(50)]
        threads.append(in_proxy_queue_thread)
        threads.extend(out_proxy_queue_threads)
        [thread.start() for thread in threads]
        [thread.join() for thread in threads]  
        """最终输出可用代理IP"""
        self.output_proxy()



def main():
    spider = ProxySpider()
    spider.run()
    print "fetch is over, begin to upload!!!!!!"    
    """上述任务执行完成后，上传结果到七牛,注意在上传之前先要配置七牛的认证"""
    #uploadtoqiniu = qiniuupload.uploadToqiniu()
    #uploadtoqiniu.upload() 


if __name__ == "__main__":
    main()