import os

def parse_fasta(faa_path):
    """解析FASTA文件，生成器返回(基因位点名称, 序列)"""
    current_gene = None
    current_seq = []
    with open(faa_path, 'r') as f:
        for line in f:
            if line.startswith('>'):
                if current_gene is not None:
                    yield (current_gene, ''.join(current_seq))
                # 提取基因位点名称（第一个空格前的内容）
                current_gene = line[1:].split(' ', 1)[0].strip()
                current_seq = []
            else:
                current_seq.append(line.strip())
        if current_gene is not None:  # 处理最后一个记录
            yield (current_gene, ''.join(current_seq))

def process_pair(txt_path, faa_path, output_path):
    """处理单个文件对"""
    # 读取txt文件中的基因位点名称
    with open(txt_path, 'r') as f:
        target_genes = {line.strip().split('\t')[0] for line in f if line.strip()}

    # 写入匹配的序列
    count = 0
    with open(output_path, 'w') as out_f:
        for gene, seq in parse_fasta(faa_path):
            if gene in target_genes:
                out_f.write(f'>{gene}\n{seq}\n')
                count += 1
    return count

def main():
    # 配置路径
    analyze_dir = "/mnt/hgfs/G/others/HP_data_new/Results/HGT_reanalyze/1127HP_faa_HGT_analyze_family_results"
    faa_dir = "/mnt/hgfs/G/others/HP_data_new/HP_2024data_from_home_tsinghan/faa/faa_files/1127HP_faa"
    output_dir = "/mnt/hgfs/G/others/HP_data_new/Results/HGT_reanalyze/1127HP_HGT_faa"
    
    # 确保输出目录存在
    os.makedirs(output_dir, exist_ok=True)

    # 遍历分析结果目录中的所有txt文件
    for txt_name in os.listdir(analyze_dir):
        if not txt_name.endswith('.txt'):
            continue

        # 构造对应文件路径
        base_name = os.path.splitext(txt_name)[0]
        txt_path = os.path.join(analyze_dir, txt_name)
        faa_path = os.path.join(faa_dir, f"{base_name}.faa")
        output_path = os.path.join(output_dir, f"{base_name}_HGT.faa")

        # 检查FASTA文件是否存在
        if not os.path.exists(faa_path):
            print(f"Warning: {faa_path} 不存在，跳过处理")
            continue

        # 处理文件对
        matched = process_pair(txt_path, faa_path, output_path)
        print(f"处理完成: {txt_name} -> 匹配到{matched}条序列")

if __name__ == "__main__":
    main()