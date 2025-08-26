#!/bin/bash
# 遍历当前目录下的所有.sra文件
for sra_file in *.sra; do
    # 检查文件是否存在
    if [ -f "$sra_file" ]; then
        # 提取不带扩展名的文件名
        base_name=$(basename "$sra_file" .sra)
        
        # 执行fastq-dump命令
        echo "Processing $sra_file..."
        fastq-dump --gzip --split-files "$sra_file"
        
        # 如果需要，可以在这里添加其他处理步骤
    else
        echo "No .sra files found in the directory."
    fi
done
echo "All .sra files have been processed."