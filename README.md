## 更新 ---2017-07-06

- 因为代理IP源网站为了反爬取，会经常变更版版面，所以爬取策略做了一些修改，删除了一些无用的源。
- 增加了代理IP的隐匿级别，最终输出的格式如下：

    | proxy               | type    |  anonymity_level  |
    | --------            | -----:  | :----:            |
    | 212.126.113.179:80  | HTTP    |   Elite           |
    | 61.191.41.130:80    | HTTP    |   Elite           |
    | 47.52.18.182:80     | HTTP    |   Transparent     |



## 更新 ---2017-06-12

- 因为vps的问题，该程序已经不再更新七牛云的代理IP 文件，也就是说[该文件](http://7xrnwq.com1.z0.glb.clouddn.com/proxy_list.txt?v=1000) 不再是最新的代理IP。
- 建议按照使用步骤自己爬取。


##  用途

用于采集网上的公用代理IP（源站见配置文件）,目前该程序仍在跑，每隔三小时刷新一遍代理IP，并将可用代理IP 上传到七牛云，可用性测试用的百度，因为时效性，不保证完全可用，但能保证基本的可用性。

想直接获取可用代理IP 的可以直接使用[这个](http://7xrnwq.com1.z0.glb.clouddn.com/proxy_list.txt?v=1000)





## 说明


### 文件更新慢问题

因为七牛CDN的原因，可能存在源文件已更新，但命中缓存仍然是之前没变的文件，这时
参考[这里](https://developer.qiniu.com/fusion/kb/1325/refresh-the-cache-and-the-effect-of-time)的第一种情况来解决。
可以在这个 url  “http://7xrnwq.com1.z0.glb.clouddn.com/proxy_list.txt”  后面添加“?v=2000” ，比如 “http://7xrnwq.com1.z0.glb.clouddn.com/proxy_list.txt?v=2000”  数字可以随意，尽量大，即可获取最新的文件。


### 源码说明


#### config.py

相关配置文件，比如代理网站站点，代理IP 输出位置，超时时间等，详情见注释。

#### proxyspider.py

主程序，大致包括一个用于采集网上代理IP 的线程，多个用于测试代理IP 是否可用的线程，测试网站用的百度，详情见注释。

#### proxy_list.txt

最终代理IP 的输出文档。

#### qiniuupload.py

将proxy_list.txt，定期提交到七牛云存储，目前是维护在这里[链接](http://7xrnwq.com1.z0.glb.clouddn.com/proxy_list.txt)

如果要用此模块的话，需要先安装七牛的库，pip install qiniu


## 使用

注：建议使用virtualenv

git clone https://github.com/zhangchenchen/proxyspider.git

cd proxyspider

pip install -r requirements.txt

python proxyspider.py

注：程序跑完后，所有代理IP输出到当前目录下的proxy_list.txt 

## TO BE CONTINUED

- 增加https 代理
- 增加socks代理