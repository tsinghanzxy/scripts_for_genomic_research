import os
from pathlib import Path

def update_fasta_headers(folder_path):
    """
    修改文件夹内所有 .faa 文件的 FASTA 标题行.
    将标题行的内容替换为文件名.
    """
    for file_path in Path(folder_path).glob("*.faa"):
        print(f"Processing file: {file_path.name}")
        
        # 读取文件内容
        with file_path.open("r") as f:
            lines = f.readlines()
        
        # 修改第一行标题
        new_first_line = f">{file_path.stem}\n"
        lines[0] = new_first_line
        
        # 写回修改后的内容
        with file_path.open("w") as f:
            f.writelines(lines)

if __name__ == "__main__":
    folder_path = "/mnt/hgfs/G/Pan_and_core_202LP/202_Pan_C/RE/RE_rename/Clinical"
    update_fasta_headers(folder_path)