#!/bin/bash

# 设置输入文件夹和输出文件夹
input_dir="/home/tsinghan/Data_VV/VV_all_min/COG_txt"
output_dir="/home/tsinghan/Data_VV/VV_all_min/Code_stat"

# 创建输出文件夹
mkdir -p "$output_dir"

# 处理所有 .txt 文件
for txt_file in "$input_dir"/*.txt; do
    # 获取文件名
    basename=$(basename "$txt_file" .txt)
    
    # 运行 Python 代码
    python3 <<EOF
import re
from custom import F3
import sys

a = {}
c = {}
wp2cog = {}
k = {}

for rec in F3.read("cog-20.def.tab", header=False):
    a[rec[0]] = list(rec[1:])
for rec in F3.read("fun2003-2014.tab", header=False):
    c[rec[0]] = rec[1]
for rec in F3.read("cog-20.cog.csv", sep=",", header=False):
    wp2cog[rec[2].replace(".", "_")] = rec[6]

with open("$txt_file") as IN:
    for line in IN:
        lines = line.strip().split("\t")
        WP = lines[0]
        COG = wp2cog[lines[1].replace(".", "_")]
        anno = "\t".join(a[COG])
        for i in anno[0]:
            k[i] = k.get(i, 0) + 1

with open("$output_dir/$basename.tsv", 'w') as OUT:
    OUT.write("code\tname\tnumber\n")
    for code in sorted(c):
        OUT.write(f"{code}\t{c[code]}\t{k.get(code, 0)}\n")
EOF
done

echo "处理完成!"