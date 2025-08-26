#!/usr/bin/env python3
# batch_sra_downloader_v3.py

import subprocess
import os
import concurrent.futures
from tqdm import tqdm

# --- 用户配置 ---

# 1. 包含SRA/ENA编号的文本文件名
SRR_LIST_FILE = "srr_list.txt"

# 2. prefetch 下载参数 (1TB)
MAX_SIZE_BYTES = 1000 * 1024 * 1024 * 1024

# 3. 设置并行下载的任务数量
#    建议根据你的网络带宽和CPU性能调整，4到8是一个比较合理的值
NUM_PARALLEL_DOWNLOADS = 8

# --- 单个文件下载函数 ---

def download_single_accession(accession_id):
    """
    下载单个SRA/ENA序列的函数，供进程池调用。
    返回一个元组 (accession_id, status, message)
    """
    command = f'prefetch {accession_id} --max-size {MAX_SIZE_BYTES}'
    try:
        # 使用 capture_output=True 来捕获输出，避免多个进程的输出混杂在一起
        # 只有在出错时才需要分析输出
        result = subprocess.run(
            command,
            shell=True,
            check=True,
            capture_output=True,
            text=True,
            encoding='utf-8'
        )
        return (accession_id, "Success", f"Successfully downloaded {accession_id}")
    except subprocess.CalledProcessError as e:
        # 如果下载失败，格式化错误信息以便报告
        error_message = (
            f"下载失败，返回码: {e.returncode}\n"
            f"  - Stderr: {e.stderr.strip()}\n"
            f"  - Stdout: {e.stdout.strip()}"
        )
        return (accession_id, "Failed", error_message)
    except Exception as e:
        return (accession_id, "Failed", f"下载过程中发生未知异常: {str(e)}")

# --- 脚本主程序 ---

def main():
    """
    主函数，用于并行下载序列。
    """
    # 步骤 1: 检查和读取SRR列表文件
    if not os.path.exists(SRR_LIST_FILE):
        print(f"---! 错误 !---")
        print(f"找不到编号列表文件: '{SRR_LIST_FILE}'")
        print(f"\n已为您创建一个示例文件 '{SRR_LIST_FILE}'。")
        print("请将你要下载的SRR/ERR编号填入此文件中，每行一个。")
        with open(SRR_LIST_FILE, 'w', encoding='utf-8') as f:
            f.write("SRR000001\n")
            f.write("SRR000002\n")
        return

    print(f"正在从 '{SRR_LIST_FILE}' 文件中读取编号...")
    with open(SRR_LIST_FILE, 'r', encoding='utf-8') as f:
        accession_ids = [line.strip() for line in f if line.strip()]

    if not accession_ids:
        print(f"---! 警告 !---")
        print(f"文件 '{SRR_LIST_FILE}' 为空，没有需要下载的编号。")
        return

    total_ids = len(accession_ids)
    print(f"读取完成，总共找到 {total_ids} 个编号准备下载。")
    print(f"将使用 {NUM_PARALLEL_DOWNLOADS} 个并行任务进行下载。")

    # 步骤 2: 使用进程池并行执行下载
    success_count = 0
    failed_items = []

    with concurrent.futures.ProcessPoolExecutor(max_workers=NUM_PARALLEL_DOWNLOADS) as executor:
        # 提交所有下载任务到进程池
        future_to_accession = {executor.submit(download_single_accession, accession_id): accession_id for accession_id in accession_ids}
        
        # 使用tqdm创建进度条，并随着任务完成而更新
        with tqdm(total=total_ids, desc="总体下载进度", unit="个") as pbar:
            for future in concurrent.futures.as_completed(future_to_accession):
                accession_id, status, message = future.result()
                if status == "Success":
                    success_count += 1
                else:
                    failed_items.append((accession_id, message))
                
                # 更新进度条
                pbar.update(1)

    # 步骤 3: 打印总结报告
    print("\n" + "=" * 60)
    print("--- 全部下载任务执行完毕 ---")
    print(f"总任务数: {total_ids}")
    print(f"成功: {success_count}")
    print(f"失败: {len(failed_items)}")

    if failed_items:
        print("\n--- 以下编号下载失败及其错误详情 ---")
        for accession_id, error_message in failed_items:
            print(f"\n[!] 编号: {accession_id}")
            print(f"    错误信息: {error_message}")
    print("=" * 60)

    # 提示如何安装tqdm
    print("\n提示: 本脚本使用 'tqdm' 库来显示进度条。")
    print("如果未安装，请在命令行运行: pip install tqdm")


if __name__ == "__main__":
    main()
