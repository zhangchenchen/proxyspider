#!/usr/bin/env python
# -*- coding: utf-8 -*-
# -*- author by pekingzcc -*-
# -*- date : 2017-05-19 -*-

"""配置文件
"""

# 利用一个正则就可以直接采集代理IP的站点
PROXY_SITES_BY_REGX = {
    'urls': [
        'http://ab57.ru/downloads/proxyold.txt',
        'http://www.proxylists.net/http_highanon.txt',
        'http://www.atomintersoft.com/high_anonymity_elite_proxy_list',
        'http://www.atomintersoft.com/transparent_proxy_list',
        'http://www.atomintersoft.com/anonymous_proxy_list',
        'http://www.proxy4free.info/',
        'http://tools.rosinstrument.com/proxy/plab100.xml',
        'https://www.rmccurdy.com/scripts/proxy/good.txt',
        'http://proxy.ipcn.org/proxylist2.html',
        'http://best-proxy.ru/feed',
        'http://www.proxylists.net/?HTTP',
        'http://uks.pl.ua/script/getproxy.php?last'
    ],
    'proxy_regx': r"\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}:\d{2,4}"   
}

# 需要利用xpath 定位代理IP 的站点
PROXY_SITES_BY_XPATH = [
    {
        'urls': ['http://www.66ip.cn/%s.html' % page for page in ['index'] + list(range(2, 11))],
        'ip_xpath': ".//*[@id='main']/div/div[1]/table/tr[position()>1]/td[1]/text()" , 
        'port_xpath': ".//*[@id='main']/div/div[1]/table/tr[position()>1]/td[2]/text()" 
    },
    {
        'urls': ['http://www.mimiip.com/gngao/%s' % page for page in range(2, 10)],
        'ip_xpath': ".//table[@class='list']/tbody/tr/td[1]/text()",
        'port_xpath': ".//table[@class='list']/tbody/tr/td[2]/text()" 
    },
    {
        'urls': ['http://www.ip181.com/daili/%s.html' % page for page in range(1, 8)],
        'ip_xpath': ".//div[@class='row']/div[3]/table/tbody/tr[position()>1]/td[1]/text()" ,
        'port_xpath': ".//div[@class='row']/div[3]/table/tbody/tr[position()>1]/td[2]/text()" 
    }
]

CHECK_PROXY_XPATH = {
    "HTTP_VIA": ".//li[@class='proxdata'][1]/span/text()", 
    "HTTP_X_FORWARDED_FOR": ".//li[@class='proxdata'][2]/span/text()"
}

# 代理输出位置
OUTPUT_FILE = "proxy_list.txt"


# User-Agent list
USER_AGENT_LIST = [
    'Mozilla/4.0 (compatible; MSIE 5.0; SunOS 5.10 sun4u; X11)',
    'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; Avant Browser;',
    'Mozilla/4.0 (compatible; MSIE 7.0b; Windows NT 5.1)',
    'Microsoft Internet Explorer/4.0b1 (Windows 95)',
    'Opera/8.00 (Windows NT 5.1; U; en)',
    'Mozilla/4.0 (compatible; MSIE 5.0; AOL 4.0; Windows 95; c_athome)',
    'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)',
    'Mozilla/5.0 (compatible; Konqueror/3.5; Linux) KHTML/3.5.5 (like Gecko) (Kubuntu)',
    'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.0; ZoomSpider.net bot; .NET CLR 1.1.4322)',
    'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; QihooBot 1.0 qihoobot@qihoo.net)',
]


# 超时时间
TIME_OUT = 4

#重试次数
RETRY_NUM = 3


# 测试URL
TEST_URL = "http://www.iprivacytools.com/proxy-checker-anonymity-test/"

## 七牛AccessKey/SecretKey,具体含义参考七牛官网文档

QINIU_AUTH = {
    "AccessKey": "*********************",
    "SecretKey": "*********************"
}

## 上传到七牛 的bucket, 具体含义参考七牛官网文档
QINIU_BUCKET = "*****"