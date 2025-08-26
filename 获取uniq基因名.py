import pandas as pd

# 读取Excel文件
df = pd.read_excel('155_gene_presence_absence_modified.xlsx', header=None)

# 将列名强制转换为字符串类型，然后去除空格和特殊字符
df.columns = df.columns.astype(str).str.strip().str.replace(r'\s+', '', regex=True)

# 获取基因名称和基因存在性数据
gene_names = df.iloc[1:, 0].values  # 基因名称
gene_presence_absence = df.iloc[1:, 1:].values  # 基因存在性数据，以 NumPy 数组表示

# 计算每个基因存在于多少个菌株中
gene_counts = gene_presence_absence.sum(axis=1)  # 每行的和，即基因在多少个菌株中存在

# 找到仅存在于一个菌株中的基因的索引
only_in_one_strain_indices = gene_counts == 1

# 获取仅存在于一个菌株中的基因名称
only_in_one_strain_genes = gene_names[only_in_one_strain_indices]

# 输出仅存在于一个菌株中的基因名至新文件
with open('genes_only_in_one_strain.txt', 'w') as f:
    for gene in only_in_one_strain_genes:
        f.write(gene + '\n')

# 打印结果
print(f"仅存在于一个菌株中的基因数量: {only_in_one_strain_indices.sum()}")
print(f"这些基因已保存至 'genes_only_in_one_strain.txt'。")