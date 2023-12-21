import time
import locale
import os
from utils import check_dir, save_txt, get_txt, get_gbk_txt
from parse_file_chatgpt import parse_file_using_chatgpt
from parse_file_wenxin import parse_file_using_wenxin

locale.setlocale(locale.LC_COLLATE, 'zh_CN.UTF-8')


mode = 'chatgpt'  # 'chatgpt' 'wenxin'  # 根据情况修改
data_dir = "data/安徽"  # 根据情况修改
save_dir = 'res/安徽'  # 根据情况修改

check_dir(save_dir)
chatgpt_str_limit = 5800
data_doc_dir = data_dir+'_doc'   # 用于文心
question = get_txt("question.txt")
no_result_num = 0
right_result_num = 0
wrong_result_num = 0
reopen_limit = 50  # 每50条关闭一次浏览器
parse_num = 0
is_reopen_browser = False  # 是否需要重启浏览器
time.sleep(3)


def parse_file(total_len, file_path, file_doc_path, is_reopen_browser, pre_res=None):
    res = '当前模式不支持'
    if mode == 'chatgpt' and total_len<chatgpt_str_limit:
        res = parse_file_using_chatgpt(file_path, question, is_reopen_browser)
    if mode == 'wenxin' and total_len>=chatgpt_str_limit:  # 如果是文心，一定要传入 pre_res
        res = parse_file_using_wenxin(file_doc_path, question, pre_res)
    return res


dir_names = os.listdir(data_dir)
dir_names.sort(key = lambda x: (int(x.split('-')[0]), int(x.split('-')[2][ : x.split('-')[2].index(')') ])))  # 安徽 先用第一个数字排序，再用括号里的排序
for dir_name in dir_names:  # 数字顺序
    sub_dir = os.path.join(data_dir, dir_name)
    sub_doc_dir = os.path.join(data_doc_dir, dir_name)
    sub_save_dir = os.path.join(save_dir, dir_name)
    check_dir(sub_save_dir)
    
    file_names = os.listdir(sub_dir)
    file_names.sort(key = lambda x: (int(x.split('__')[0])))
    for file_name in file_names:  # 按字符串中的数字排序
        file_path = os.path.join(sub_dir, file_name)  # chat直接用
        file_doc_path = os.path.abspath(os.path.join(sub_doc_dir, file_name[:-4]+'.doc'))  # 文心需要填入绝对路径

        content = get_txt(file_path)
        total_len = len(content)+len(question)
        save_path = None
        if total_len<chatgpt_str_limit:
            save_path = os.path.join(sub_save_dir, file_name[:-4]+'__chat.txt')
        if total_len>=chatgpt_str_limit:
            save_path = os.path.join(sub_save_dir, file_name[:-4]+'__wenxin.txt')

        res = None
        if not os.path.exists(save_path):  # 若结果不存在，才进行解析
            no_result_num += 1
            print(' ============ 第{}个无结果文件 ============ {}'.format(no_result_num, file_name))
            print('total_len:', total_len)
            print('\n第一次生成结果')

            parse_num += 1
            if parse_num>200:
                is_reopen_browser = True
                parse_num = 0
            res = parse_file(total_len, file_path, file_doc_path, is_reopen_browser)
            if parse_num>200:
                is_reopen_browser = False
                parse_num = 0

            print('\n生成结果：\n{} '.format(res))
            save_txt(res, save_path)
        else:  # 若结果存在 (注意当刷完一遍chat后，文心的结果文件肯定存在，肯定走这个分支，便以此结果来判断文心是否生成了新答案)
            pre_res = get_txt(save_path)

            pre_res_len = len(pre_res.split('\n\n'))  # result 的大概长度
            if pre_res_len<8:  # 说明结果没有生成对，重新来
                wrong_result_num += 1
                print(' ============ 第{}个未识别文件 ============ {}'.format(wrong_result_num, file_name))
                print('total_len:', total_len)
                print('\n以前的结果是：\n{} '.format(pre_res))
                print('共{}行信息'.format(pre_res_len))

                # if '由于提供的链接无法直接访问' not in res and \
                #     '由于提供的链接无法访问' not in res and \
                #     '无法回答问题 1 到 12' not in res and \
                #     '无法回答问题1到12' not in res and \
                #     '由于提供的链接无法直接打开查看内容' not in res and \
                #     '由于提供的文本信息中包含' not in res:  # 这几种情况先跳过，再来一遍，多半也是，所以可以留着后面整体重新来
                parse_num += 1
                if parse_num>200:
                    is_reopen_browser = True
                res = parse_file(total_len, file_path, file_doc_path, is_reopen_browser, pre_res=pre_res)
                if pre_res and res=='当前模式不支持':  # 若为模式不支持，则不刷新以前的答案
                    res = pre_res
                if parse_num>200:
                    is_reopen_browser = False
                    parse_num = 0

                print('\n重新生成结果：\n{} '.format(res))
                save_txt(res, save_path)
            else:
                right_result_num += 1
                print(' ============ 第{}个正确识别文件 ============ {}'.format(right_result_num, file_name))
                print('total_len:', total_len)


        
