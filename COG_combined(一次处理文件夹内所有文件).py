import os
import re
import sys
from custom import F3
import pandas as pd

# 初始化字典
a = {}
c = {}
wp2cog = {}
k = {}

# 读取数据
for rec in F3.read("cog-20.def.tab", header=False):
    a[rec[0]] = list(rec[1:])
for rec in F3.read("fun2003-2014.tab", header=False):
    c[rec[0]] = rec[1]
for rec in F3.read("cog-20.cog.csv", sep=",", header=False):
    wp2cog[rec[2].replace(".", "_")] = rec[6]

# 设置输入文件夹路径
input_folder = '/path/to/your/folder'  # 替换为你的输入文件夹路径
combined_data = []

# 遍历所有 .txt 文件
for filename in os.listdir(input_folder):
    if filename.endswith('.txt'):
        input_file = os.path.join(input_folder, filename)
        output_file = os.path.join(input_folder, filename.replace('.txt', '.tsv'))

        # 处理每个 .txt 文件
        k.clear()  # 重置计数器
        with open(input_file) as IN:
            for line in IN:
                lines = line.strip().split("\t")
                WP = lines[0]
                COG = wp2cog[lines[1].replace(".", "_")]
                anno = "\t".join(a[COG])
                for i in anno[0]:
                    k[i] = k.get(i, 0) + 1

        # 将结果写入 .tsv 文件
        with open(output_file, 'w') as OUT:
            OUT.write("code\tname\tnumber\n")
            for code in sorted(c):
                OUT.write(f"{code}\t{c[code]}\t{k.get(code, 0)}\n")
        
        print(f"已处理文件: {filename}，输出文件: {output_file}")
        
        # 收集偶数列数据
        with open(output_file) as OUT:
            data = [line.strip().split("\t") for line in OUT.readlines()[1:]]
            combined_data.append([line[0] for line in data])  # 奇数列
            combined_data[-1].extend([line[1] for line in data])  # 偶数列

# 生成 combined.tsv 文件
combined_output = os.path.join(input_folder, 'combined.tsv')
with open(combined_output, 'w') as OUT:
    OUT.write("code\tname\n")  # 假设只保留 code 和 name 列
    for i in range(len(combined_data)):
        if i == 0:
            for j in range(len(combined_data[i])):
                OUT.write(f"{combined_data[i][j]}\t{combined_data[i][j]}\n")
        else:
            for j in range(1, len(combined_data[i])):
                OUT.write(f"{combined_data[0][j]}\t{combined_data[i][j]}\n")

print(f"合并文件已生成: {combined_output}")