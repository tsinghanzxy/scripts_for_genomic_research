import os
from collections import defaultdict

# 指定文件夹路径
folder_path = '/home/tsinghan/Helicobacter_pylori_genome_dataset_20240819/renamed_fna/extracted_genes'

# 用于存储按相同部分分组的文件
grouped_files = defaultdict(list)

# 获取所有文件名并分组
for filename in os.listdir(folder_path):
    if filename.endswith('.out'):
        parts = filename.split('.')
        if len(parts) > 2:
            key = parts[1]  # 获取第一个.之后和第二个.之前的部分
            grouped_files[key].append(filename)

# 合并文件并输出
for key, files in grouped_files.items():
    output_file = os.path.join(folder_path, f"{key}_merge.fas")
    with open(output_file, 'w') as outfile:
        for filename in files:
            file_path = os.path.join(folder_path, filename)
            with open(file_path, 'r') as infile:
                outfile.write(infile.read())
                outfile.write('\n')  # 添加换行符以分隔文件内容
    print(f"合并完成，输出文件为: {output_file}")