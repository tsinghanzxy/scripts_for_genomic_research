import pandas as pd  
import random  

# 读取Excel文件  
df = pd.read_excel('155_gene_presence_absence_modified.xlsx', header=None)  

# 将列名强制转换为字符串类型，然后去除空格和特殊字符  
df.columns = df.columns.astype(str).str.strip().str.replace(r'\s+', '', regex=True)  

# 获取基因名称（第一列从第二行开始）  
gene_names = df.iloc[1:, 0].tolist()  

# 获取所有菌株名称（假设菌株名称从第二列的列名中获取）  
strain_names = df.columns[1:]  # 从第二列开始的列名作为菌株名称  

# 检查菌株名称是否与列名一致  
print("Strain names from the header:", strain_names)  
print("Columns in DataFrame:", df.columns.tolist())  

# 被选择的菌株和结果列表  
selected_strains = []  
results = []  

# 初始化全基因集合  
all_genes_set = set()  

# 逐步添加菌株并计算  
for i in range(len(strain_names)):  
    # 随机选择一个菌株，确保不重复选择  
    available_strains = [s for s in strain_names if s not in selected_strains]  
    strain = random.choice(available_strains)  

    # 检查菌株是否存在于 DataFrame 的列中  
    if strain not in df.columns:  
        print(f"Warning: Strain {strain} not found in DataFrame columns. Skipping...")  
        continue  

    selected_strains.append(strain)  
    print(f"Selected strain: {strain} (Total selected: {i + 1})")  

    # 获取该菌株的基因存在性数据  
    strain_idx = df.columns.get_loc(strain)  
    strain_data = df.iloc[1:, strain_idx]  # 获取菌株的基因存在性数据  

    # 更新所有基因集合  
    unique_genes = {gene_names[j] for j in range(len(strain_data)) if strain_data.iloc[j] == 1}  
    
    # 更新全基因集合，确保每个基因只计算一次  
    all_genes_set.update(unique_genes)  

    # 计算总基因数  
    all_genes_count = len(all_genes_set)  

    # 更新共有基因集合  
    if i > 0:  
        shared_genes = set.intersection(  
            *[set(gene_names[j] for j in range(len(df.iloc[1:, df.columns.get_loc(s)])) if df.iloc[1:, df.columns.get_loc(s)].iloc[j] == 1) for s in selected_strains]  
        )  
        shared_genes_count = len(shared_genes)  
    else:  
        shared_genes_count = 0  

    # 将结果添加到列表  
    results.append({  
        'Number of Strains': i + 1,  
        'Total Gene Count': all_genes_count,  
        'Shared Gene Count': shared_genes_count  
    })  

    # 打印当前结果  
    print(f"Number of strains: {i + 1}, Total gene count: {all_genes_count}, Shared gene count: {shared_genes_count}")  

# 创建一个新的DataFrame来保存结果  
result_df = pd.DataFrame(results)  

# 保存结果到新的Excel文件  
result_df.to_excel('gene_counts_and_shared_genes.xlsx', index=False)  

print("计算完成，结果已保存到 'gene_counts_and_shared_genes.xlsx'。")