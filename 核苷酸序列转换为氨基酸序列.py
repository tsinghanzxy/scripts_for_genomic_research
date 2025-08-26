from Bio import SeqIO

# 输入和输出文件名
input_file = 'core_2154.fas'
output_file = 'core_2154.faa'

# 读取输入文件并翻译序列
with open(input_file, 'r') as infile, open(output_file, 'w') as outfile:
    for record in SeqIO.parse(infile, 'fasta'):
        # 翻译序列，使用标准密码子表
        protein_sequence = str(record.seq.translate())
        
        # 写入输出文件
        SeqIO.write(SeqIO.SeqRecord(
            protein_sequence,
            id=record.id,
            description=record.description
        ), outfile, 'fasta')

print(f"翻译完成，结果已保存到 '{output_file}'。")