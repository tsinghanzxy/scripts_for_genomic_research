import os
import shutil

def copy_all_txt_files_flat(source_dir, target_dir):
    """
    递归复制源目录中所有子文件夹下的.txt文件到目标目录的根目录（不保留文件夹结构）
    """
    # 创建目标目录
    os.makedirs(target_dir, exist_ok=True)
    
    total_files = 0
    copied_files = 0
    duplicate_files = 0
    error_files = 0

    # 遍历所有子文件夹
    for root, _, files in os.walk(source_dir):
        for filename in files:
            if filename.lower().endswith(".txt"):
                total_files += 1
                src_path = os.path.join(root, filename)
                dst_path = os.path.join(target_dir, filename)
                
                # 检查文件是否已存在（避免覆盖）
                if os.path.exists(dst_path):
                    print(f"文件已存在，跳过: {filename}")
                    duplicate_files += 1
                    continue  # 如果希望覆盖，注释这行
                
                # 尝试复制文件
                try:
                    shutil.copy2(src_path, dst_path)
                    copied_files += 1
                except Exception as e:
                    print(f"复制失败: {filename} - {str(e)}")
                    error_files += 1

    # 输出统计信息
    print("\n操作统计:")
    print(f"扫描到 .txt 文件总数: {total_files}")
    print(f"成功复制新文件: {copied_files}")
    print(f"跳过重复文件: {duplicate_files}")
    print(f"复制失败文件: {error_files}")

# 使用示例
source_dir = "/data/Share/zhanxy_data/LP_research/All_4147_LP_faa_HGT_analyze_family"
target_dir = "/data/Share/zhanxy_data/LP_research/All_4147_LP_faa_HGT_analyze_family_results"
copy_all_txt_files_flat(source_dir, target_dir)