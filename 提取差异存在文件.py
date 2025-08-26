import os
import shutil

# 设置两个要比较的文件夹路径
folder1 = 'path/to/folder1'
folder2 = 'path/to/folder2'

# 设置保存差异文件的新文件夹路径
output_folder = 'path/to/output_folder'

# 创建输出文件夹,如果不存在的话
if not os.path.exists(output_folder):
    os.makedirs(output_folder)

# 比较两个文件夹,找出差异存在的文件
diff_files = []
for root, dirs, files in os.walk(folder1):
    for file in files:
        file_path1 = os.path.join(root, file)
        file_path2 = os.path.join(folder2, os.path.relpath(file_path1, folder1))
        if not os.path.exists(file_path2) or not filecmp.cmp(file_path1, file_path2):
            diff_files.append(file_path1)

# 将差异存在的文件复制到输出文件夹
for file_path in diff_files:
    output_file_path = os.path.join(output_folder, os.path.relpath(file_path, folder1))
    output_dir = os.path.dirname(output_file_path)
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    shutil.copy2(file_path, output_file_path)

print(f"已将 {len(diff_files)} 个差异文件复制到 {output_folder} 文件夹。")