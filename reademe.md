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




