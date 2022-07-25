# !/usr/bin/env python3
# _*_ coding:utf-8 _*_
import os
import inspect
from pathlib import Path
from lib.obfuscator_m1 import obfuscate_js_m1
from lib.obfuscator_m2_bug import obfuscate_js_m2


# 判断列表内的字符串是否某个字符串内 # 如果列表为空,就返回default值
def list_in_str(list_=None, str_=None, default=True):
    flag = False
    if list_:
        for ele in list_:
            if ele in str_:
                flag = True
                break
    else:
        flag = default
    return flag


# 读取文件内容并返回结果列表
def read_file_to_list_de_weight(file_name, encoding='utf-8', errors="ignore"):
    """
    读取文件内容并返回结果列表
    """
    with open(file_name, 'r', encoding=encoding, errors=errors) as f_obj:
        result_list = []
        for line in f_obj.readlines():
            if line.strip() != "":
                result_list.append(line.strip())
        return result_list


# 判断文件是否存在
def file_is_exist(file_path):
    '''判断文件是否存在'''
    if file_path:
        path = Path(file_path)
        if path.is_file():
            return True
        else:
            return False


def mkdir(path):
    # 去除首位空格
    path = path.strip()
    # 去除尾部\符号
    path = path.rstrip("\\")
    # 判断路径是否存在
    # 存在     True
    # 不存在   False
    isExists = os.path.exists(path)
    # 判断结果
    if not isExists:
        # 如果不存在则创建目录
        os.makedirs(path)
        return True
    else:
        # 如果目录存在则不创建，并提示目录已存在
        return False


# 替换生成新文件
def replace_templates(src_dir_path=None, dst_dir_path=None, ext=None, replace_dict=None):
    print("[+] 正在通过模板动态生成JS文件")

    if replace_dict is None:
        replace_dict = {}
    file_ext_list = []
    for root, dirs, files in os.walk(src_dir_path, topdown=False):
        for name in files:
            if name.endswith(ext):
                file_ext_list.append(os.path.join(root, name))

    for file_name in file_ext_list:
        with open(file_name, "r+", encoding="utf-8", errors="ignore") as f_old:
            new_file_path = file_name.rsplit(ext, 1)[0].replace(src_dir_path, dst_dir_path)
            with open(new_file_path, "w+", encoding="utf-8", errors="ignore") as f_new:
                content = f_old.read()
                for raw_string, new_string in replace_dict.items():
                    content = content.replace(raw_string, new_string)
                f_new.write(content)
                print(f"[+] {new_file_path} 生成完毕...")


# 进行常规JS代码混淆
def js_obfuscate_m1(js_code_dir=None, ext=".js"):
    print("[+] 已开启JS文件加密功能,当前使用js_obfuscate_m1...")
    file_ext_list = []
    for root, dirs, files in os.walk(js_code_dir, topdown=False):
        for name in files:
            if name.endswith(ext):
                file_ext_list.append(os.path.join(root, name))

    for file_name in file_ext_list:
        with open(file_name, "r", encoding="utf-8", errors="ignore") as f_old:
            content = f_old.read()
            with open(file_name, "w", encoding="utf-8", errors="ignore") as f_new:
                new_content = obfuscate_js_m1(content)
                f_new.write(new_content)
                print(f"[+] {file_name} 混淆完毕...混淆前长度{len(content)}...混淆后长度{len(new_content)}...")


def js_obfuscate_m2(js_code_dir=None, ext=".js"):
    print("[+] 已开启JS文件加密功能,当前使用js_obfuscate_m2...")
    file_ext_list = []
    for root, dirs, files in os.walk(js_code_dir, topdown=False):
        for name in files:
            if name.endswith(ext):
                file_ext_list.append(os.path.join(root, name))

    for file_name in file_ext_list:
        with open(file_name, "r", encoding="utf-8", errors="ignore") as f_old:
            content = f_old.read()
            with open(file_name, "w", encoding="utf-8", errors="ignore") as f_new:
                new_content = obfuscate_js_m2(content)
                f_new.write(new_content)
                print(f"[+] {file_name} 混淆完毕...混淆前长度{len(content)}...混淆后长度{len(new_content)}...")


def touch_file(file_path):
    if not file_is_exist(file_path):
        open(file_path, "a+", encoding="utf-8").close()


def get_var_name(var):
    callers_local_vars = inspect.currentframe().f_back.f_locals.items()
    return [var_name for var_name, var_val in callers_local_vars if var_val is var][0]
