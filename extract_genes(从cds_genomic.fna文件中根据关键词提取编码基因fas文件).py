def extract_lines_to_file(input_file, output_file, keyword):
    within_content = False

    with open(input_file, 'r') as input_f, open(output_file, 'w') as output_f:
        for line in input_f:
            if keyword in line:
                within_content = True
                output_f.write(line)
            elif ">" in line:
                if within_content:
                    break
            elif within_content:
                output_f.write(line)
# 调用示例
input_file = '/mnt/hgfs/G/Bordetella_pertussis_complete_genome_dataset/ncbi_dataset/data/GCF_000193595.2/cds_from_genomic.fna' # 替换为实际的输入文件路径
output_file = '/mnt/hgfs/G/Bordetella_pertussis_complete_genome_dataset/ncbi_dataset/data/GCF_000193595.2/fhaB.fas'  # 替换为实际的输出文件路径
keyword = "fhaB"

extract_lines_to_file(input_file, output_file, keyword)