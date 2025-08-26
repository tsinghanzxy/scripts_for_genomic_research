import os
import subprocess
from concurrent.futures import ProcessPoolExecutor

# 定义数据库路径
db_path = "/data/Share/zhanxy_data/db/bakta_db"

# 定义输出文件夹基础路径
output_base_path = "/data/Share/zhanxy_data/BP_research/20250705_3386BP_annonation_bakta"

# 定义物种名称
species = "Burkholderia pseudomallei"

# 定义线程数
threads = 32

# 定义输入文件夹路径
input_dir = "/data/Share/zhanxy_data/BP_research/BP_95_5_fna"


def process_file(filename):
    # 提取文件名（不含扩展名）作为前缀
    prefix = filename.split(".fasta")[0]
    
    # 定义输出文件夹路径
    output_path = os.path.join(output_base_path, prefix)
    
    # 定义目标.gff文件路径
    gff_file_path = os.path.join(output_path, f"{prefix}.gff3")
    
    # 如果输出文件夹和.gff文件都存在，则跳过处理
    if os.path.exists(output_path) and os.path.exists(gff_file_path):
        print(f"跳过已处理文件: {filename}")
        return
    
    # 创建输出文件夹（如果不存在）
    if not os.path.exists(output_path):
        os.makedirs(output_path)
    
    # 定义输入文件路径
    input_file_path = os.path.join(input_dir, filename)
    
    # 构建bakta命令
    command = [
        "bakta",
        "--db", db_path,
        "--prefix", prefix,
        "--output", output_path,
        "--species", species,
        "--threads", str(threads),
        "--strain", prefix,
        "--force",
        input_file_path
    ]
    
    # 运行bakta命令
    subprocess.run(command, check=True)
    print(f"处理完成: {filename}")


# 获取所有.fasta文件
fasta_files = [f for f in os.listdir(input_dir) if f.endswith(".fasta")]

# 使用ProcessPoolExecutor来并行处理文件
with ProcessPoolExecutor(max_workers=20) as executor:
    executor.map(process_file, fasta_files)

print("所有文件处理完成。")