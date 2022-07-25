# FishingAutoMonitor


## 严正声明:

本项目仅限于合法用户的合法测试，如使用者有任何违法行为目的，请立刻马上删除本项目。



## 项目介绍:

用Python实现URL钓鱼时自动收杆框架。

此处URL钓鱼主要是指：XSS钓鱼、网页钓鱼、链接下载等需要通过访问web页面进行钓鱼的操作。





## 功能特点：

使用Python Flask框架实现、部署简单

目前版本通过Cookie和IP|IP段进行收杆。

支持动态替换模板中的变量、无需手动替换HOST信息。

支持对JS代码进行混淆加密。

支持多种记录参数自定义。

支持限制IP记录上线记录数据

支持限制IP访问上线记录数据

支持限制IP下载钓鱼文件

## 快速使用：

### 1、必须参数配置

首先setting.py中配置pwd、HOST、PORT、下载文件等参数。

pwd = "12345"   #设置访问上线页面的密码

PROTOCOL = "http"     #替换module文件夹中的{PROTOCOL }
DOMAIN = "192.168.1.1"    #替换module文件夹中的{DOMAIN }
DOWNLOAD = f"{PROTOCOL}://{DOMAIN}/download/notepad.exe" #替换module文件夹中的{DOWNLOAD }



### 2、设置是否需要混淆JS文件

 js_obfuscate_method == 0: 不加密
 js_obfuscate_method == 1: js_obfuscate_m1(js_code_dir=static_path)  

注意：混淆后可能会导致JS运行出错、请先测试

注意：浏览器存在静态文件缓存、测试页面已解决该问题

注意：可先在module或static目录使用自己的诱导模板，欢迎大家提交JS模板



### 3、设置上线成功条件



在符合条件时，会对前端JS调用返回对应的True|FALSE值

HAS_IP_HAS_COOKIE = "TRUE"  # 存在IP上线记录、并且存在Cookie访问记录,
HAS_CIP_HAS_COOKIE = "TRUE"  # 存在CIP上线记录、并且存在Cookie访问记录,

HAS_IP_NOT_COOKIE = "TRUE"  # 存在IP上线记录、但不存在Cookie访问记录, # 动态判断
HAS_CIP_NOT_COOKIE = "TRUE"  # 存在CIP上线记录、但不存在Cookie访问记录, # 动态判断

NOT_IP_HAS_COOKIE = "FALSE"  # 不存在IP上线记录、但存在Cookie访问记录 # 动态判断
NOT_CIP_HAS_COOKIE = "FALSE"  # 不存在CIP上线记录、但存在Cookie访问记录 # 动态判断

NOT_IP_NOT_COOKIE = "FALSE"  # 不存在IP上线记录、也不存在Cookie访问记录
NOT_CIP_NOT_COOKIE = "FALSE"  # 不存在CIP上线记录、也不存在Cookie访问记录



### 4、接口说明

http://host:port/test  # 加载JS的测试页面

http://host:port/exist # 判断IP是否已经上线

http://host:port/download/<file_name> # 下载文件

http://host:port/static/xxx # 静态文件目录

http://host:port/store # CS服务器上线时调用webhook，格式如:/store?action=store&internalIP=192.168.88.88&userName=hong66&computerName=hong66-pc&externalIP=88.88.88.88

http://host:port/online?pwd=12345  # 查看已经上线的IP信息,需要携带密码参数



## 更新改进:

才疏学浅,欢迎大家提出改进需求。

即时联系：请联系【NOVASEC】团队或关注【NOVASEC】公众号获取WX。

其他方案：GITHUB提取需求

