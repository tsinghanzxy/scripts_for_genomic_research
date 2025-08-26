import argparse
import os
from Bio import SeqIO
from Bio.SeqRecord import SeqRecord

parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)
parser.add_argument(
    "-i", "--input_dir", type=str, required=True, help="path to raw gbk dir"
)
parser.add_argument(
    "-o", "--output_dir", type=str, required=True, help="path to new gbk dir"
)
args = args = parser.parse_args()
input_dir = args.input_dir
output_dir = args.output_dir

if not os.path.exists(output_dir):
    os.makedirs(output_dir)
    print(f"文件夹 '{output_dir}' 创建成功")


def generate_new_gbk_file(input_file: str, output_file: str):
    # 解析GeneBank文件
    records = SeqIO.parse(input_file, "genbank")

    # 创建新的记录列表
    new_records = []

    # 遍历每个记录
    for record in records:
        # 创建新的特征列表
        new_features = []
        # 遍历每个特征
        for feature in record.features:
            # 如果特征类型是 "gene"，则清空qualifiers
            if feature.type == "gene":
                feature.qualifiers = {}

            # 将特征添加到新的特征列表中
            if feature.type != "mRNA":
                new_features.append(feature)

        # 创建新的记录对象，只保留原记录中的序列和新的特征列表
        new_record = SeqRecord(
            record.seq, name=record.name, id=record.id, description=record.description
        )
        new_record.features = new_features
        new_record.annotations = record.annotations
        new_record.letter_annotations = record.letter_annotations

        # 将新的记录添加到新的记录列表中
        new_records.append(new_record)

    # 将新的记录列表写入GeneBank文件
    SeqIO.write(new_records, output_file, "genbank")


# %%
# input_dir = "/mnt/results/test/gbk_duplicate_error"
# 列出文件夹中的所有文件
files = os.listdir(input_dir)

# 过滤以".gbk"结尾的文件
gbk_files = [file for file in files if file.endswith(".gbk")]
for gbk_file in gbk_files:
    gbk_file_name = gbk_file.split(".gbk")[0]
    error_gbk_file = f"{input_dir}/{gbk_file}"
    correct_gbk_file = f"{output_dir}/{gbk_file_name}.gbk"
    generate_new_gbk_file(input_file=error_gbk_file, output_file=correct_gbk_file)
#

# %%
