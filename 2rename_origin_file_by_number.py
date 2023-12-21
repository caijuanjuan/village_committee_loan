import os
import locale

locale.setlocale(locale.LC_COLLATE, 'zh_CN.UTF-8')

data_dir = "data/安徽"  # 按情况修改
dir_names = os.listdir(data_dir)
# sorted_dir_names = sorted(dir_names, key=locale.strxfrm)  # 文件夹是根据数字排序的，不是中文，所以暂时不用这个

# 将结果文件重命名--加上数字编号
idx = 1
# sorted_dir_names = sorted(dir_names, key=locale.strxfrm)
dir_names.sort(key = lambda x: (int(x.split('-')[0]), int(x.split('-')[2][ : x.split('-')[2].index(')') ])))  # 先用第一个数字排序，再用括号里的排序
for dir_name in dir_names:  # 按数字排序
    sub_data_dir = os.path.join(data_dir, dir_name)
    file_names = os.listdir(sub_data_dir)
    sorted_file_names = sorted(file_names, key=locale.strxfrm)
    for file_name in sorted_file_names:  # 按中文排序
        file_path = os.path.join(sub_data_dir, file_name)
        new_file_name = str(idx) + '__' + file_name
        new_file_path = os.path.join(sub_data_dir, new_file_name)  # 重命名为以数字开头
        os.rename(file_path, new_file_path)
        idx += 1