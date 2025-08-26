import os
import shutil

def copy_files_from_list():
    """
    Reads a list of strain names from a file and copies corresponding .gff3 files
    from a source directory to a destination directory.
    """
    # Define paths relative to the user's home directory
    home_dir = os.path.expanduser("~")
    list_file_path = os.path.join(home_dir, 'BP_checkM_97.5&2.5_list.txt')
    source_dir = os.path.join(home_dir, 'BP_gff3')
    destination_dir = os.path.join(home_dir, 'BP_975_25_gff3')

    # --- 1. Validate Prerequisite Files and Folders ---
    if not os.path.isfile(list_file_path):
        print(f"错误：菌株列表文件不存在于 '{list_file_path}'")
        return

    if not os.path.isdir(source_dir):
        print(f"错误：源文件夹不存在于 '{source_dir}'")
        return

    # --- 2. Create Destination Directory ---
    if not os.path.exists(destination_dir):
        os.makedirs(destination_dir)
        print(f"已创建目标文件夹: {destination_dir}")

    print(f"正在从列表文件读取菌株名称: {list_file_path}")
    
    copied_count = 0
    not_found_count = 0
    # --- 3. Read List and Copy Files ---
    try:
        with open(list_file_path, 'r', encoding='utf-8') as f:
            strain_names = [line.strip() for line in f if line.strip()]
    except Exception as e:
        print(f"读取列表文件时出错: {e}")
        return

    print(f"共找到 {len(strain_names)} 个菌株名称，开始复制...")

    for strain_name in strain_names:
        gff3_filename = f"{strain_name}.gff3"
        source_file_path = os.path.join(source_dir, gff3_filename)
        destination_file_path = os.path.join(destination_dir, gff3_filename)

        if os.path.exists(source_file_path):
            try:
                shutil.copy2(source_file_path, destination_file_path)
                # print(f"已复制: {gff3_filename}") # Uncomment for verbose output
                copied_count += 1
            except Exception as e:
                print(f"复制文件 {gff3_filename} 时出错: {e}")
        else:
            print(f"警告：在源文件夹中未找到文件: {gff3_filename}")
            not_found_count += 1

    print("\n--- 操作完成 ---")
    print(f"成功复制了 {copied_count} 个文件。")
    if not_found_count > 0:
        print(f"{not_found_count} 个文件在源文件夹中未找到。")
    print(f"所有文件均已复制到: {destination_dir}")

if __name__ == "__main__":
    copy_files_from_list()
