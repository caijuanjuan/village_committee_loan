import zipfile
import os
import locale
locale.setlocale(locale.LC_COLLATE, 'zh_CN.UTF-8')

data_dir = 'data'  # 按情况修改
dir_names = os.listdir(data_dir)

sorted_dir_names = sorted(dir_names, key=locale.strxfrm)
for dir_name in sorted_dir_names:  # 按中文排序
    sub_data_dir = os.path.join(data_dir, dir_name)
    print(sub_data_dir)
    
    file_names = os.listdir(sub_data_dir)
    for file_name in file_names:  # 按数字排序
        print(file_name)
        file_path = os.path.join(sub_data_dir, file_name)
        extract_folder = os.path.join(sub_data_dir, file_name[:-4])
        zip_ref = zipfile.ZipFile(file_path, 'r')  # 打开zip文件
        zip_ref.extractall(extract_folder)  # 解压zip文件中的所有文件
        # zip_ref.extract('file.txt', 'destination_folder')  # 解压zip文件中的特定文件
        zip_ref.close()

