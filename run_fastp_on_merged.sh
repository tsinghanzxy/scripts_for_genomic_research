#!/bin/bash
set -e

# --- 配置 ---
# 1. 设置你希望同时运行的fastp任务数量 (并行处理的样本对数)
NUM_PARALLEL_JOBS=8

# 2. 设置每个fastp任务可以使用的线程数
THREADS_PER_JOB=4

# 3. 输入和输出目录
INPUT_DIR="/mnt/hgfs/H/RE_LLO/163LLO_fastq_merged"
OUTPUT_DIR="/mnt/hgfs/H/RE_LLO/163LLO_fastq_deal"
mkdir -p "$OUTPUT_DIR"

# --- 警告 ---
TOTAL_THREADS=$((NUM_PARALLEL_JOBS * THREADS_PER_JOB))
echo "============================================================"
echo "重要提示:"
echo "脚本将启动 ${NUM_PARALLEL_JOBS} 个并行的fastp任务。"
echo "每个任务将使用 ${THREADS_PER_JOB} 个线程。"
echo "总计将占用 ${TOTAL_THREADS} 个CPU线程。请确保服务器资源充足。"
echo "============================================================"
sleep 3 # 等待3秒让用户看到提示

# --- 主逻辑 ---

# 1. 定义一个函数，用于处理单对fastq文件
process_pair() {
    file1="$1"
    
    # 从前向读文件（_1）推断出样本名和反向读文件名（_2）
    sample_name=$(basename "$file1" _1.fastq.gz)
    file2="${INPUT_DIR}/${sample_name}_2.fastq.gz"
    
    if [[ -f "$file2" ]]; then
        echo "==> 开始处理: $sample_name"
        
        # 定义fastp的输出文件
        output_file1="$OUTPUT_DIR/${sample_name}_1.fastq"
        output_file2="$OUTPUT_DIR/${sample_name}_2.fastq"
        
        # 执行fastp命令, 使用配置的线程数
        fastp -i "$file1" -I "$file2" \
              -o "$output_file1" -O "$output_file2" \
              --correction --thread="$THREADS_PER_JOB" --length_required=25 \
              --n_base_limit=5 --compression=5
        
        if [ $? -eq 0 ]; then
            echo "==> 成功完成: $sample_name"
        else
            echo "==> 处理失败: $sample_name" >&2
        fi
    else
        echo "警告：找不到与 $(basename "$file1") 配对的文件 $(basename "$file2")"
    fi
}

# 2. 导出函数和需要的变量，以便xargs调用的子shell能访问它们
export INPUT_DIR
export OUTPUT_DIR
export THREADS_PER_JOB
export -f process_pair

# 3. 使用find和xargs并行处理
echo "在 $INPUT_DIR 中查找 *_1.fastq.gz 文件并开始并行处理..."

find "$INPUT_DIR" -type f -name "*_1.fastq.gz" -print0 | xargs -0 -n 1 -P "$NUM_PARALLEL_JOBS" -I {} bash -c 'process_pair "{}"'

echo "所有fastp并行任务已完成。"