import csv
import os

# 获取文件夹中的所有CSV文件
folder_path = '/home/tsinghan/MPXV genomic data20231029/allgenecsv'
output_folder_path = '/home/tsinghan/MPXV genomic data20231029/allgenecsvnew'

# 遍历文件夹中的每个CSV文件
for filename in os.listdir(folder_path):
    if filename.endswith('.csv'):
        # 拼接文件路径
        file_path = os.path.join(folder_path, filename)

        # 打开CSV文件
        with open(file_path, 'r', newline='') as csvfile:
            reader = csv.reader(csvfile)

            # 读取所有行数据
            rows = list(reader)

        # 替换中文标点逗号和分号为英文逗号
        for row in rows:
            for i, value in enumerate(row):
                  row[i] = value.replace(',','')

        # 设置标题行为"Longitude"和"Latitude"
        #rows[0] = ['Longitude', 'Latitude']

        # 创建新的CSV文件路径和名称
        output_file_path = os.path.join(output_folder_path, filename)

        # 写入数据到新的CSV文件
        with open(output_file_path, 'w', newline='') as csvfile:
            writer = csv.writer(csvfile)

            # 将处理后的数据写入新的CSV文件
            writer.writerows(rows)