import os
import re

def get_txt(filename):
    file = open(filename, "r", encoding='utf-8')
    context = file.read()  # 读取文件内容
    file.close()
    return context

def get_gbk_txt(filename):
    file = open(filename, "r", encoding='GBK')
    context = file.read()  # 读取文件内容
    file.close()
    return context


def save_txt(re, save_path):
    file = None
    with open(save_path, 'w', encoding='utf-8') as file:
        file.write(re)
    file.close()


def check_dir(dir):
    if not os.path.exists(dir):
        os.makedirs(dir, exist_ok=True)
    return 'hhh'

def check_res_ok(file_path, res):
    if file_path.endswith('chat.txt'):
        if len(re.split('\d{1,}\. ', res)[1:])<15:
            return False
    if file_path.endswith('wenxin.txt'):
        if len(res.split('\n\n'))<10:
            return False
    return True

        