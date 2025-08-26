import os
import subprocess

# 定义目标文件夹路径
target_folder = '/data/Share/zhanxy_data/BP_research/BP_975_25_fna'

# 遍历文件夹中的所有 .fna 文件
for filename in os.listdir(target_folder):
    if filename.endswith('.fna'):
        file_path = os.path.join(target_folder, filename)
        
        # 构造输出目录和前缀
        output_dir = os.path.join(target_folder, os.path.splitext(filename)[0])
        prefix = os.path.splitext(filename)[0]
        
        # 构造 prokka 命令
        command = [
            'prokka',
            '--outdir', output_dir,
            '--compliant',
            '--CPUS', '32',
            '--prefix', prefix,
            '--species', 'Burkholderia pseudomallei',
            '--strain', prefix,
            '--addgenes',
            '--addmrna',
            file_path
        ]

        # 执行命令
        print(f'Processing {file_path}...')
        subprocess.run(command)

print('Processing completed.')