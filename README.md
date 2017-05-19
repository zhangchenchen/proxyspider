##  用途

用于采集网上的公用代理IP,目前该程序仍在跑，每隔三小时刷新一遍代理IP，并将可用代理IP 上传到七牛云，可用性测试用的百度，不保证其他网站代理可用。

想直接获取可用代理IP 的可以直接使用[这个](http://7xrnwq.com1.z0.glb.clouddn.com/proxy_list.txt)


## 说明

#### config.py

相关配置文件，比如代理网站站点，代理IP 输出位置，超时时间等，详情见注释。

#### proxyspider.py

主程序，大致包括一个用于采集网上代理IP 的线程，多个用于测试代理IP 是否可用的线程，测试网站用的百度，详情见注释。

#### proxy_list.txt

最终代理IP 的输出文档。

#### qiniuupload.py

将proxy_list.txt，定期提交到七牛云存储，目前是维护在这里[链接] (http://7xrnwq.com1.z0.glb.clouddn.com/proxy_list.txt)


## 使用

git clone https://github.com/zhangchenchen/proxyspider.git

cd proxyspider

python proxyspider.py

