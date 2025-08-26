import pandas as pd

# 读取 Excel 文件
df = pd.read_excel('pangenome_matrix.xlsx', header=None)

# 打开输出文件
with open('pangenome_matrix.fas', 'w') as f:
    # 遍历每一列
    for col in range(df.shape[1]):
        # 第一行内容前加 ">"
        header = f">{df.iloc[0, col]}"
        f.write(header + '\n')
        
        # 合并第二行至第5849行的内容为一行
        merged_content = ''.join(str(df.iloc[row, col]) for row in range(1, min(5850, df.shape[0])))
        f.write(merged_content + '\n')