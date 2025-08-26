import os
import re
from collections import defaultdict

# 指定文件夹路径
folder_path = '/home/tsinghan/Helicobacter_pylori_genome_dataset_20240819/renamed_fna/Virulencefactors_merged'

# 创建一个字典以存储按前缀分组的文件
grouped_files = defaultdict(list)

# 获取所有符合条件的文件
for filename in os.listdir(folder_path):
    if re.search(r'(_merge|_\d+_merge)\.fas$', filename):
        # 提取前缀
        match = re.match(r'(_\w+).*?_merge(\d*)\.fas', filename)
        if match:
            key = match.group(1)  # 获取前缀
            grouped_files[key].append(filename)

# 合并文件并输出
for key, files in grouped_files.items():
    output_file = os.path.join(folder_path, f"{key}_merge_merge.fas")
    
    # 打开输出文件准备写入
    with open(output_file, 'w') as outfile:
        for filename in files:
            file_path = os.path.join(folder_path, filename)
            with open(file_path, 'r') as infile:
                # 读取文件内容并写入合并文件
                outfile.write(infile.read())
                outfile.write('\n')  # 添加换行符以分隔文件内容

    print(f"合并完成，输出文件为: {output_file}")