from Bio import SeqIO
from collections import OrderedDict

# 设置输入文件路径
input_file = '/mnt/hgfs/G/all_DV.fas'
output_file = '/mnt/hgfs/G/all_DV_alleles.fas'

# 从 .fas 文件中读取序列,并去重
unique_records = OrderedDict()
for record in SeqIO.parse(input_file, 'fasta'):
    seq = str(record.seq)
    if seq not in unique_records:
        unique_records[seq] = record

# 将去重后的序列写入新的 .fas 文件
with open(output_file, 'w') as out_handle:
    for record in unique_records.values():
        SeqIO.write(record, out_handle, 'fasta')

print(f"已将去重后的序列写入到 {output_file} 文件。")