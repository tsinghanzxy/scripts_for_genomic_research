#!/bin/bash

# --- 配置 ---
# 设置你希望同时运行的任务数量。
# 一个好的起始值是你的CPU核心数，或者略少于核心数。
NUM_PARALLEL_JOBS=4

# --- 主逻辑 ---

# 1. 定义一个函数，包含处理单个.sra文件的所有操作。
#    这个函数将接收一个.sra文件路径作为参数。
process_single_file() {
    sra_file="$1"
    
    # 检查传入的是否为文件
    if [ ! -f "$sra_file" ]; then
        echo "警告: '$sra_file' 不是一个有效文件，已跳过。"
        return
    fi
    
    echo "==> 开始处理: $sra_file"
    
    # 执行fastq-dump命令
    fastq-dump --gzip --split-files "$sra_file"
    
    # 检查fastq-dump命令是否成功执行
    if [ $? -eq 0 ]; then
        echo "==> 成功完成: $sra_file"
    else
        # 将错误信息输出到标准错误流
        echo "==> 处理失败: $sra_file" >&2
    fi
}

# 2. 将上面定义的函数导出，以便xargs命令调用的子shell可以使用它
export -f process_single_file

# 3. 使用find找到当前目录下的所有.sra文件，然后通过管道传给xargs进行并行处理
echo "在当前目录下查找 .sra 文件..."
# 使用-print0和-0可以安全处理带空格等特殊字符的文件名
# -P 指定并行任务数
# -n 1 一次给命令传递一个参数（一个文件名）
# -I {} 将参数占位符设置为{}
find . -maxdepth 1 -type f -name "*.sra" -print0 | xargs -0 -n 1 -P "$NUM_PARALLEL_JOBS" -I {} bash -c 'process_single_file "{}"'

echo "所有并行任务已完成。"
