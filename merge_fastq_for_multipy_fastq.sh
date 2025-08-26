#!/bin/bash
set -e # 如果任何命令失败，则立即退出

# --- 配置 ---
# 包含原始fastq文件的目录 (可能有多个文件对)
INPUT_DIR="/mnt/hgfs/H/RE_LLO/163LLO_fastq"

# 用于存放合并后文件的目录
MERGED_DIR="/mnt/hgfs/H/RE_LLO/163LLO_fastq_merged"

# --- 主逻辑 ---
echo "开始文件合并..."
mkdir -p "$MERGED_DIR"

# 通过查找所有 *_1.fastq* 文件来获取唯一的样本名称列表
# 例如，从 "SRR123_1.fastq.gz" 提取出 "SRR123"
SAMPLES=$(find "$INPUT_DIR" -type f -name "*_1.*fastq*" | while read F; do basename "$F" | sed -E 's/_1\..*//'; done | sort -u)

if [ -z "$SAMPLES" ]; then
    echo "错误：在目录 $INPUT_DIR 中没有找到符合 '*_1.*fastq*' 格式的文件。"
    exit 1
fi

echo "找到以下样本进行处理："
echo "$SAMPLES"
echo "---------------------------------"

for sample in $SAMPLES; do
    echo "正在处理样本: $sample"

    # 找到属于该样本的所有前向和反向读文件，并按名称排序
    forward_files=$(find "$INPUT_DIR" -type f -name "${sample}*1.*fastq*" | sort)
    reverse_files=$(find "$INPUT_DIR" -type f -name "${sample}*2.*fastq*" | sort)

    if [ -z "$forward_files" ] || [ -z "$reverse_files" ]; then
        echo "警告：找不到样本 ${sample} 的成对文件，已跳过。"
        continue
    fi

    echo "找到的前向读文件:"
    echo "$forward_files"
    echo "找到的反向读文件:"
    echo "$reverse_files"

    # 定义合并后的输出文件名
    output_fwd="$MERGED_DIR/${sample}_1.fastq.gz"
    output_rev="$MERGED_DIR/${sample}_2.fastq.gz"

    # 使用cat命令合并文件。合并压缩的gz文件是安全且正确的。
    echo "正在合并前向读文件 -> $output_fwd"
    cat $forward_files > "$output_fwd"

    echo "正在合并反向读文件 -> $output_rev"
    cat $reverse_files > "$output_rev"

    echo "成功合并样本: $sample"
    echo "---------------------------------"
done

echo "所有样本合并完成！合并后的文件位于: $MERGED_DIR"
