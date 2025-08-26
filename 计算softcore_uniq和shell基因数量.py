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

# 统计不同条件下的基因数量  
only_in_one_strain = (gene_counts == 1).sum()             # 仅存在于一个菌株中的基因数量  
more_than_equal_147_strains = (gene_counts >= 147).sum()  # 存在于>=147个菌株中的基因数量  
more_than_one_less_than_147 = ((gene_counts > 1) & (gene_counts < 147)).sum()  # >1且<147的基因数量  

# 打印结果  
print(f"仅存在于一个菌株中的基因数量: {only_in_one_strain}")  
print(f"存在于≥147个菌株中的基因数量: {more_than_equal_147_strains}")  
print(f"存在于>1和<147个菌株中的基因数量: {more_than_one_less_than_147}")