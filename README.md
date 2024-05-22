流程：
  1. 创建文件夹
    a. mkdir -p /u4/dnslog
    b. mkdir -p /u2/workdir/dnspkt
  2. 上传及解压程序
    a. /u4/ 下解压 dns.tar.gz(拆分好的跟域名文件) 为 dns 文件夹
    b. /u4/ 下解压 domain.tar.gz 为 domain 文件夹
    c. /usr/local 下解压 domain2brute.tar.gz 为 domain2brute 文件夹
  3. 执行程序
    a. 链接：ln -s /usr/local/python3.9/bin/python3.9 /usr/bin/python3
    b. 启动：/usr/local/domain2brute/restart.sh
    c. 查看 /u4/dns 文件是否减少
    d. 查看 /u4/dnslog 日志是否生成及是否正常(确认子域名和国家字段是否为空)
  4. 结果入库
    a. 将日志文件对应结果入138库，每月入一次，索引格式：base_social_user_domain_addr_202405

注意事项
  1. VPS目前存储空间25G，要注意存储空间，及时同步文件到内部138服务器上


# GeoLite2-City.mmdb

`GeoLite2-City.mmdb` 是一个 MaxMind 公司提供的 IP 地址到地理位置的映射数据库文件。这个文件通常用于将 IP 地址映射到特定的地理位置信息，比如国家、城市、经纬度等。

如果您想要在项目中使用这个文件，可以将它放在项目的合适位置，并在代码中使用相应的库来解析这个文件以获取地理位置信息。

在 Python 中，您可以使用 `geoip2` 库来解析 `GeoLite2-City.mmdb` 文件。以下是一个简单的示例代码：

```python
import geoip2.database

# 指定 GeoLite2-City.mmdb 文件的路径
reader = geoip2.database.Reader('path/to/GeoLite2-City.mmdb')

# 输入一个 IP 地址，获取地理位置信息
response = reader.city('8.8.8.8')

print(response.country.name)  # 输出国家名称
print(response.city.name)     # 输出城市名称
print(response.location.latitude)  # 输出纬度
print(response.location.longitude)  # 输出经度

reader.close()  # 记得关闭 reader 对象
```

请确保您已经下载了最新版本的 `GeoLite2-City.mmdb` 文件，并替换 `'path/to/GeoLite2-City.mmdb'` 为文件的实际路径。您也可以根据自己的需求调整代码来获取更多地理位置信息。

如果您有任何其他问题或需要进一步帮助，请随时告诉我。



# dns_process.py

这段代码是一个 Python 脚本，用于解析 DNS 数据包并提取其中的信息，包括域名、IP 地址、ASN（自治系统号）、ASN 组织、国家代码、国家名称和城市名称等信息。解析后的信息会以 JSON 格式写入文件中。

以下是代码的主要功能和结构：

1. 导入了必要的库，包括 `os`、`datetime`、`time`、`random`、`string`、`geoip2.database`、`scapy.all` 等。
2. 定义了一些变量，包括空的 IP 地址列表、是否安静模式、`geo_reader` 和 `asn_reader` 用于读取地理位置和 ASN 数据库文件。
3. 定义了一个函数 `dns_process(packet)` 用于处理 DNS 响应数据包，提取其中的信息并写入 JSON 文件。
4. 定义了一个函数 `decode_loop_pkt(file_dir)` 用于循环解析指定目录下的数据包文件。
5. 在 `__main__` 部分，设置了数据包文件目录 `file_dir`，并尝试读取地理位置和 ASN 数据库文件。
6. 使用 `while True` 循环不断解析数据包文件，并每隔3秒执行一次解析操作。

这段代码主要用于监控 DNS 数据包，提取其中的关键信息，并将信息以 JSON 格式保存到文件中。在解析 DNS 数据包时，还会使用 MaxMind 公司提供的 `GeoLite2-City.mmdb` 和 `GeoLite2-ASN.mmdb` 文件来获取地理位置和 ASN 相关信息。

如果您有任何关于代码的具体问题或需要进一步的解释，请随时告诉我。


# 
这段代码是一个简单的 Python 脚本，用于监听指定网卡上的 DNS 请求，并提取 DNS 响应中的关键信息，包括 A 记录、AAAA 记录和 CNAME 记录，并将捕获到的 DNS 响应数据包保存为 pcap 文件。

以下是代码的主要功能和结构：

1. 导入了必要的库，包括 `os`、`datetime`、`time`、`random`、`string`、`scapy.all` 等。
2. 定义了空的 IP 地址列表、是否安静模式以及生成随机字符串的函数 `random_string(length)`。
3. 定义了一个 DNS 响应解析回调函数 `dns_callback(packet)`，用于处理捕获到的 DNS 响应数据包。在函数中，如果数据包包含 A 记录、AAAA 记录或 CNAME 记录，会将整个数据包保存为 pcap 文件。
4. 在 `__main__` 部分，尝试创建一个目录 `/u2/workdir/dnspkt` 用于存储 pcap 文件。
5. 使用 `sniff` 函数监听指定网卡 `eth0` 上的 DNS 请求，并调用 `dns_callback` 函数处理捕获到的数据包。

这段代码的主要作用是监听 DNS 请求并捕获 DNS 响应中的特定记录类型，并将这些响应保存为 pcap 文件。您可以根据需要对代码进行调整，比如更改监听的端口、调整保存文件的路径等。

如果您有任何关于代码的具体问题或需要进一步的解释，请随时告诉我。




# dns2brute.py
这段代码是一个 Python 脚本，用于读取文件中的域名列表，将每个域名与预定义的字典中的域名结合，构成新的域名，并向 DNS 服务器发送查询请求。脚本会循环处理指定目录下的文件，每次处理一个文件中的域名列表。

以下是代码的主要功能和结构：

1. 导入了必要的库，包括 `requests`、`traceback`、`logging`、`signal`、`time`、`sys`、`os`、`json`、`socket`、`datetime`、`geoip2.database`、`dns.resolver`、`scapy.all` 等。
2. 定义了一些全局变量，包括存储域名字典和查询结果的变量，GeoIP 数据库读取器、ASN 数据库读取器、DNS 解析器、网卡名称、网卡 IP 地址等。
3. 定义了函数 `load_dict()` 用于从文件中加载域名字典，并将其存储在 `dns_dict` 中。
4. 定义了函数 `do_with_file(path)` 用于处理文件中的域名列表，将每个域名与预定义的字典中的域名结合，构成新的域名，并存储在 `json_map` 中。
5. 在 `__main__` 部分，加载域名字典并获取网卡 IP 地址。
6. 在一个无限循环中，遍历指定目录下的文件，对每个文件中的域名列表进行处理，构建新的域名并向 DNS 服务器发送查询请求。
7. 每次处理完一个文件后，会将该文件删除，并在循环中每隔3秒执行一次处理操作。

总体来说，这段代码的作用是构建新的域名并通过 DNS 查询请求获取相应的 DNS 解析结果。如果您有任何关于代码的具体问题或需要进一步的解释，请随时告诉我。