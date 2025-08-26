import os
import subprocess

# 设置输入文件夹路径和输出文件夹路径
input_folder = '/data/Share/zhanxy_data/LP_research/All_4147_LP_HGT_faa_250320new'  # 输入文件夹路径
output_folder = '/data/Share/zhanxy_data/LP_research/All_4147_LP_HGT_faa_250320new_COG2024_results'  # 输出文件夹路径
diamond_db = '/data/Share/zhanxy_data/db/COG2024/cog-2024.dmnd'  # Diamond 数据库路径

# 创建输出文件夹（如果不存在）
os.makedirs(output_folder, exist_ok=True)

# 遍历所有 .faa 文件
for filename in os.listdir(input_folder):
    if filename.endswith('.faa'):
        input_file = os.path.join(input_folder, filename)
        output_file = os.path.join(output_folder, filename.replace('.faa', '.txt'))

        # 构建 diamond blastp 命令
        command = [
            'diamond', 'blastp',
            '-p', '20',
            '-d', diamond_db,
            '-q', input_file,
            '--outfmt', '6',
            'qseqid', 'sseqid', 'pident', 'length', 'mismatch', 'gapopen', 
            'qstart', 'qend', 'sstart', 'send', 'evalue', 'bitscore', 
            'qlen', 'slen', 'stitle',
            '--more-sensitive',
            '-o', output_file,
            '-k', '1',
            '-e', '1e-5'
        ]

        # 执行命令
        try:
            subprocess.run(command, check=True)
            print(f"已处理文件: {filename}，输出文件: {output_file}")
        except subprocess.CalledProcessError as e:
            print(f"处理文件 {filename} 时出错: {e}")