import os
import locale
import openpyxl
import re
import json
from utils import get_txt


locale.setlocale(locale.LC_COLLATE, 'zh_CN.UTF-8')


workbook = openpyxl.Workbook()
worksheet = workbook.active
save_dir = "res/安徽"
save_excel_path = 'res_安徽.xlsx'
wrong_res = []
dir_names = os.listdir(save_dir)
# sorted_dir_names = sorted(dir_names, key=locale.strxfrm)  # 这个文件夹是根据数字排序的，不是中文，所以暂时不用这个
# col_names = ['文件名', '债权人', '债务人', '是否涉及多个债权人', '涉案村委会名称', '涉案村委会地址','借贷发生时间', '债权人上诉时间', '法院立案或判决时间', '纠纷的借贷本金', '借贷利率', '法院是否支持', '法院支持的债务金额'] # 13列
col_names = ['文件名', '结果','债权人', '债务人', '是否涉及多个债权人', '省、直辖市','地级市、区、自治州、盟', '市辖区、县级市、县', '涉案村委会名称', '借贷发生时间', '债权人上诉时间', '法院立案或判决时间', '纠纷的借贷本金', '借贷利率', '法院是否支持', '法院支持的债务金额'] # 13列
line_idx = 2

def write_line(dt_list, write_line):
    char_dx = [chr(i) for i in range(ord('A'), ord('Z')+1)]
    for i,val in enumerate(dt_list):
        worksheet[char_dx[i]+str(write_line)] = val


write_line(col_names, 1)

with open("country.json", "r", encoding="utf-8") as f:
    prov_city = json.load(f)

# 读入所有的省、市、区
all_provs = prov_city.keys()
all_citys = []
all_areas = []
for prov in all_provs:
    city_areas = prov_city[prov]  # 单个省
    all_citys += list(city_areas.keys())
    for area in city_areas.values():
        all_areas += list(area)

print(len(all_citys))
print(len(all_areas))

def check_area(dist_str):
    is_prov, is_city, is_area = False, False, False
    res1, res2, res3 = None, None, None
    for area in all_areas:
        if (area in dist_str) or (len(area)>2 and area[:-1] in dist_str):  # 也可以不加最后一个字（县、市啥的）
            res3 = area
            is_area = True
    if not is_area:
        for city in all_citys:
            if (city in dist_str) or (len(city)>2 and city[:-1] in dist_str):
                res2 = city
                is_city = True
    if not is_area and not is_city:
        for prov in all_provs:
            if (prov in dist_str) or (len(prov)>2 and prov[:-1] in dist_str):
                res1 = prov
                is_prov = True
    return is_prov, is_city, is_area, res1, res2, res3

def get_prov_city_from_area(res):
    for prov in all_provs:
        city_areas = prov_city[prov]  # 单个省
        for city,areas in city_areas.items():
            for area in areas:
                if area==res:
                    return prov, city, area
            
def get_prov_from_city(res):
    for prov in all_provs:
        city_areas = prov_city[prov]  # 单个省
        for city,__ in city_areas.items():
            if city==res:
                return prov, city

dir_names.sort(key = lambda x: (int(x.split('-')[0]), int(x.split('-')[2][ : x.split('-')[2].index(')') ])))  # 安徽文件夹排序 先用第一个数字排序，再用括号里的排序
for dir_name in dir_names:  # 按数字排序
    sub_save_dir = os.path.join(save_dir, dir_name)
    
    file_names = os.listdir(sub_save_dir)
    file_names.sort(key = lambda x: (int(x.split('__')[0]))) # 按字符串中的数字排序
    for file_name in file_names:  # 按数字排序
        file_path = os.path.join(sub_save_dir, file_name)
        print(file_path)

        # 读取文件内容
        content = get_txt(file_path)
        content = content.replace('*', '')  # 若有加粗，则去除文本中的*号

        # 解析出答案
        suffix = file_name.split('__')[-1][:-4]  # chatgpt or wenxin
        ans_list = [file_name.split('...')[0] + suffix] + [content]

        # 解析 chatgpt 的结果
        if suffix=='chat':
            # ans_simple1 = content.split('. ')[1:]  # 以答题序号后的'.'分隔
            ans_simple1 = re.split('\d{1,}\. ', content)[1:]  # 以至少一位正实数 + '. ' 分隔
            ans_simple2 = [item.split('\n\n') if '\n\n' in item else item.split('\n') for item in ans_simple1]  # 以回车分隔
            for i,item in enumerate(ans_simple2):
                if len(item)==1:  # 若没有回车
                    ans_simple2[i] = item[0] 
                elif len(item)>1 and len(item[-1])<=5:  # 若最后一个长度小于5，即舍去
                    ans_simple2[i] = "  ".join(item[:-1])
                elif len(item)>1 and len(item[-1])>5:  # 若最后一个长度大于5，即全部保留
                    ans_simple2[i] = "  ".join(item)

            ans_simple3 = [item.split('：', 1)[1] if '：' in item else item for item in ans_simple2]  # 每一行，以第一个冒号分隔，取后面的内容
            ans_simple3 = [item.split(': ', 1)[1] if ': ' in item else item for item in ans_simple3]  # 每一行，以第一个冒号分隔，取后面的内容
            ans_simple4 = [item[:-1] if item.endswith('。') else item for item in ans_simple3]  # 每一行，以第一个冒号分隔，取后面的内容
            ans_list = ans_list + ans_simple4

        # 解析 wenxin 的结果
        if suffix=='wenxin':
            if '债权人' in content:
                idx = content.index('债权人')  # 从债权人开始截取
            content = content[idx:]
            ans_simple1 = content.split('\n\n') if '\n\n' in content else content.split('\n')
            ans_simple2 = [item.split('：')[1] if '：' in item else item for item in ans_simple1]  # 每一行，以第一个冒号分隔，取后面的内容
            ans_simple3 = [item.split('.')[1] if '.' in item else item for item in ans_simple2]  # 每一行，以第一个冒号分隔，取后面的内容
            ans_simple4 = [item[:-1] if item.endswith('。') else item for item in ans_simple3]  # 每一行，以第一个冒号分隔，取后面的内容
            ans_list = ans_list + ans_simple4  
            if len(ans_list)>len(col_names)-2:
                ans_list = ans_list[:len(col_names)-2]  # 去掉尾部

        # 确认解析出的长度是正确的
        try:
            assert len(ans_list)==len(col_names)-2  # 其中第四个问题：人民法院名称，用于 省、市、区三列
        except:
            ans_list = [file_name.split('...')[0]+suffix]  + [content] + ['文件解析错误']*(len(col_names)-4)
            wrong_res.append(file_name)  # 若这里长度错了，下面的长度肯定也错了，下面就不加了

        # 提取省、市、区
        prov, city, area = None, None, None
        is_prov, is_city, is_area = False, False, False

        __, __, is_area, res1, res2, res3 = check_area(file_name)  # 先从文件名中提取
        if is_area:
            prov, city, area = get_prov_city_from_area(res3)
        else:  # 没有找到area，才从人民法院中提取
            __, __, is_area, res1, res2, res3 = check_area(ans_list[4])
            if is_area:
                prov, city, area = get_prov_city_from_area(res3)
            else:  # 没有找到area，才从涉案村委会名称中提取
                __, __, is_area, res1, res2, res3 = check_area(ans_list[5])
                if is_area:
                    prov, city, area = get_prov_city_from_area(res3)

        if not is_area:
            __, is_city, __, res1, res2, res3 = check_area(file_name)  # 先从文件名中提取
            prov, city, area = None, None, '/'
            if is_city:
                prov, city = get_prov_from_city(res2)
            else:  # 没有找到city，才从人民法院中提取
                __, is_city, __, res1, res2, res3 = check_area(ans_list[4])
                if is_city:
                    prov, city = get_prov_from_city(res2)
                else:  # 没有找到city，才从涉案村委会名称中提取
                    __, is_city, __, res1, res2, res3 = check_area(ans_list[5])
                    if is_city:
                        prov, city = get_prov_from_city(res2)

        if not is_area and not is_city:
            is_prov, __, __, res1, res2, res3 = check_area(file_name)  # 先从文件名中提取
            prov, city, area = None, '/', '/'
            if is_prov:
                prov = res1
            else:  # 没有找到prov，才从人民法院中提取
                is_prov, __, __, res1, res2, res3 = check_area(ans_list[4])
                if is_prov:
                    prov = res1
                else:  # 没有找到prov，才从涉案村委会名称中提取
                    is_prov, __, __, res1, res2, res3 = check_area(ans_list[5])
                    if is_prov:
                        prov = res1

        if not is_area and not is_city and not is_prov:
            prov, city, area = '/', '/', '/'


        ans_list = ans_list[:5] + [prov] + [city] + [area] + [ans_list[6]] + ans_list[7:]

        # 确认解析出的长度是正确的
        try:
            assert len(ans_list)==len(col_names)  # 其中第四个问题：人民法院名称，用于 省、市、区三列
        except:
            ans_list = [file_name.split('...')[0]+suffix]  + [content] + ['文件解析错误']*(len(col_names)-2)

    
        # 写入表格
        write_line(ans_list, line_idx)
        line_idx += 1


# 遍历每个列并设置最合适的宽度
for col in worksheet.columns:
    max_length = max([len(str(cell.value)) + 0.7 * len(re.findall(r'([\u4e00-\u9fa5])', str(cell.value))) for cell in col])
    worksheet.column_dimensions[col[0].column_letter].width = min(30, max_length)  # (max_length + 2) * 0.8
# 加粗首行
char_dx = [chr(i) for i in range(ord('A'), ord('Z')+1)]
for i in range(len(col_names)):
    cell = worksheet[char_dx[i]+str(1)]
    cell.font = openpyxl.styles.Font(bold=True)
# 保存工作簿
workbook.save(save_excel_path)

print(' =================== 未识别文件 =================== ')
print('\n'.join(wrong_res))



