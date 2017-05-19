##  用途

用于采集网上的公用代理IP


## 说明

#### config.py

相关配置文件，比如代理网站站点，代理IP 输出位置，超时时间等，详情见注释。

#### proxyspider.py

主程序，大致包括一个用于采集网上代理IP 的线程，多个用于测试代理IP 是否可用的线程，测试网站用的百度，详情见注释。

#### proxy_list.txt

最终代理IP 的输出文档。


## 使用

git clone https://github.com/zhangchenchen/proxyspider.git

cd proxyspider

python proxyspider.py