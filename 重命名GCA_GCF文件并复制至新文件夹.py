import os
import shutil

def rename_and_copy_fna(src_dir, dest_dir):
    # 如果目标文件夹不存在，则创建它
    if not os.path.exists(dest_dir):
        os.makedirs(dest_dir)
        print(f"已创建目标文件夹: {dest_dir}")

    # 遍历源文件夹中的所有文件
    for filename in os.listdir(src_dir):
        # 仅处理以 .fna 结尾的文件
        if filename.endswith(".fna"):
            # 逻辑：取文件名中第二个小数点之前的部分
            # 例如 GCA_048551335.1_ASM4855133v1_genomic.fna 
            # 拆分后取前两个部分再组合，或者按 "_" 拆分
            
            parts = filename.split('_')
            if len(parts) >= 2:
                # 提取 GCA 部分和随后的数字版本号部分
                # 结果如: GCA_048551335.1
                new_name = f"{parts[0]}_{parts[1]}.fna"
                
                src_path = os.path.join(src_dir, filename)
                dest_path = os.path.join(dest_dir, new_name)
                
                # 复制并重命名
                shutil.copy2(src_path, dest_path)
                print(f"已复制: {filename} -> {new_name}")

# 参数设置
source_folder = '2025-2026_BP'  # 你的源文件夹路径
rename_folder = 'rename'         # 你的目标文件夹路径

rename_and_copy_fna(source_folder, rename_folder)