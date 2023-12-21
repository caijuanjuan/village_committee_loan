目录结构

```python
|-- data
	|-- 安徽
    	|-- 1-(1-6)北大法宝司法案例库批量下载20231119195819
        	|-- 安徽省宿州市萧县黄口镇马常庄村村民委员会、...(FBM-CLI.C.308356482).txt
        	|-- 安徽省宿州市萧县黄口镇马常庄村村民委员会、...(FBM-CLI.C.308356482).txt
    	|-- 1-(1-6)北大法宝司法案例库批量下载20231119195819
        	|-- ...
        |-- ...
	|-- 北京
	|-- ...
|-- 0uzip_file.py  # 批量解压数据，但是还没完善，有一部分会出错，待解决
|-- 1get_coordinate.py  # 得到当前鼠标坐标，用于查看各个button的位置
|-- 2rename_origin_file_by_number.py  # 给当前省份的每个文件重命名，加上数字编号（按文件夹显示的顺序）
|-- 3change_txt_to_doc.py  # 把txt文件的复制一份出来，全部改后缀为 doc
|-- 4main.py  # 解析文件主代码，需要更改参数：mode，data_dir，save_dir
|-- 5generate_excel.py  # 把生成后的结果总结到表格中
|-- question.txt  # 回答的问题，注意，文心一言需要删除其中的第一句 “根据以上信息，回答以下问题：”
```













