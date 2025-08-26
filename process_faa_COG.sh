#!/bin/bash

# 设置输入文件夹和输出文件夹
input_dir="/home/tsinghan/Data_VV/VV_all_min/VV_all_min_faa"
output_dir="/home/tsinghan/Data_VV/VV_all_min/COG_txt"

# 创建输出文件夹
mkdir -p "$output_dir"

#设置diamond路径
diamond_path="/home/tsinghan/anaconda3/bin/diamond"

# 处理所有 .faa 文件
for faa_file in "$input_dir"/*.faa; do
    # 获取文件名
    basename=$(basename "$faa_file" .faa)
    
    # 运行 diamond blastp
    diamond blastp -p 32 -d cog-20.dmnd -q "$faa_file" --outfmt 6 qseqid sseqid pident length mismatch gapopen qstart qend sstart send evalue bitscore qlen slen stitle --more-sensitive -o "$output_dir/$basename.txt" -k 1 -e 1e-5
done

echo "处理完成!"