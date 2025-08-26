import os
import subprocess

def process_fastq_files(directory):
    # 遍历指定目录
    for filename in os.listdir(directory):
        if filename.endswith(".fastq"):
            # 构建完整的文件路径
            fastq_file = os.path.join(directory, filename)
            bowtie2out_file = os.path.splitext(filename)[0] + '.bowtie2.bz2'
            output_file = 'profiled_' + os.path.splitext(filename)[0] + '.txt'

            # 构建命令
            command = [
                'metaphlan',
                fastq_file,
                '--bowtie2out', bowtie2out_file,
                '--nproc', '32',
                '--input_type', 'fastq',
                '-o', output_file
            ]

            # 执行命令
            try:
                subprocess.run(command, check=True)
                print(f"Processed {fastq_file} successfully.")
            except subprocess.CalledProcessError as e:
                print(f"Error processing {fastq_file}: {e}")

if __name__ == "__main__":
    # 替换为包含 .fastq 文件的目录路径
    directory_path = '/mnt/hgfs/G/Gastric_ECC20220330/GC-plasma-HD-12samples/00.mergeRawFq/Merged_by_flash'
    process_fastq_files(directory_path)