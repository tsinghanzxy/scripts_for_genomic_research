import pandas as pd
import numpy as np
import random

def process_and_save(file_index):
    # 读取Excel文件
    df = pd.read_excel('4147_gene_presence_absence_modified.xlsx', header=None)

    # 将列名强制转换为字符串类型，然后去除空格和特殊字符
    df.columns = df.columns.astype(str).str.strip().str.replace(r'\s+', '', regex=True)

    # 获取基因名称（第一列从第二行开始）
    gene_names = df.iloc[1:, 0].values

    # 获取菌株存在性数据，为后续的向量化操作准备
    gene_presence_absence = df.iloc[1:, 1:].values  # 变成 NumPy 二维数组

    # 获取所有菌株名称
    strain_names = df.columns[1:].tolist()  # 从第二列开始的列名作为菌株名称

    # 被选择的菌株和结果列表
    selected_strains = []
    results = []

    # 初始化全基因集合
    all_genes_set = set()

    # 逐步添加菌株并计算
    for i in range(len(strain_names)):
        # 随机选择一个菌株，确保不重复选择
        available_indices = [index for index, s in enumerate(strain_names) if s not in selected_strains]
        strain_index = random.choice(available_indices)
        strain = strain_names[strain_index]

        selected_strains.append(strain)
        print(f"Selected strain: {strain} (Total selected: {i + 1})")

        # 获取该菌株的基因存在性记录
        strain_data = gene_presence_absence[:, strain_index]  # 选择该菌株的列

        # 更新所有基因集合
        unique_genes = {gene_names[j] for j in np.where(strain_data == 1)[0]}  # 直接通过 NumPy 获取
        all_genes_set.update(unique_genes)

        # 计算总基因数
        all_genes_count = len(all_genes_set)

        # 更新共有基因集合
        if i > 0:
            # 使用 NumPy 进行交集计算
            shared_genes_indices = np.where(np.all(gene_presence_absence[:, [strain_names.index(s) for s in selected_strains]] == 1, axis=1))[0]
            shared_genes_count = len(shared_genes_indices)
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
    output_file = f'gene_counts_and_shared_genes_{file_index:02d}.xlsx'
    result_df.to_excel(output_file, index=False)

    print(f"计算完成，结果已保存到 '{output_file}'。")


def main():
    # 重复执行10次，生成10个文件
    for i in range(1, 11):
        process_and_save(i)

if __name__ == "__main__":
    main()