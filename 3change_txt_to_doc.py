import os
from utils import check_dir
import shutil


data_txt_dir = "data/安徽"
data_doc_dir = data_txt_dir+'_doc'
shutil.copytree(data_txt_dir, data_doc_dir)
# check_dir(data_doc_dir)

dir_names = os.listdir(data_doc_dir)


for dir_name in dir_names:  
    sub_data_doc_dir = os.path.join(data_doc_dir, dir_name)
    file_names = os.listdir(sub_data_doc_dir)

    for file_name in file_names:  
        file_path = os.path.join(sub_data_doc_dir, file_name)

        new_file_name = file_name[:-4] +'.doc'
        new_file_path = os.path.join(sub_data_doc_dir, new_file_name)

        os.rename(file_path, new_file_path)
