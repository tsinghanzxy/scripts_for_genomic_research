import os
import subprocess
import concurrent.futures
from datetime import datetime

# 配置参数
max_workers = (os.cpu_count() + 5) // 6  # CPU核心数分配
max_retries = 3  # 最大重试次数
faa_dir = "All_4147_LP_faa"
output_base = "All_4147_LP_faa_HGT_search"
log_file = "processing.log"
hgtector_bin = "hgtector"
diamond_db = "/data/Share/zhanxy_data/db/hgtdb_20230102/diamond.dmnd"
taxdump_dir = "/data/Share/zhanxy_data/db/hgtdb_20230102/taxdump"

# 初始化工作环境
os.makedirs(output_base, exist_ok=True)

# 获取所有待处理文件
def get_files():
    return [os.path.join(faa_dir, f) for f in os.listdir(faa_dir) if f.endswith(".faa")]

files = get_files()
total = len(files)
processed = 0
skipped = 0

# 日志函数
def log_message(message, file_path=None):
    timestamp = datetime.now().strftime("[%Y-%m-%d %H:%M:%S]")
    if file_path:
        print(f"{timestamp} [{file_path}] {message}")
    else:
        print(f"{timestamp} {message}")

# 主处理函数
def process_file(f):
    global processed, skipped
    base_name = os.path.splitext(os.path.basename(f))[0]
    out_dir = os.path.join(output_base, base_name)
    status_file = os.path.join(out_dir, ".success")

    # 跳过已成功处理的任务
    if os.path.exists(status_file):
        skipped += 1
        log_message("已跳过", f)
        return "skipped"

    # 重试机制
    for retry in range(max_retries):
        try:
            os.makedirs(out_dir, exist_ok=True)

            # 执行核心命令
            command = [
                hgtector_bin,
                "search",
                "-i", f,
                "-o", out_dir,
                "-m", "diamond",
                "-p", "16",
                "-d", diamond_db,
                "-t", taxdump_dir
            ]
            with open(os.path.join(out_dir, "hgtector.log"), "w") as log, \
                 open(os.path.join(out_dir, "error.log"), "w") as err:
                subprocess.run(command, stdout=log, stderr=err, check=True)
            open(status_file, "w").close()  # 标记任务成功
            processed += 1
            log_message("处理成功", f)
            return "success"
        except subprocess.CalledProcessError as e:
            log_message(f"处理失败 (重试 {retry + 1}/{max_retries}): {e}", f)
            continue
        except Exception as e:
            log_message(f"意外错误: {e}", f)
            break
    log_message("超过最大重试次数，放弃处理", f)
    return "failed"

# 主函数
def main():
    with open(log_file, "w") as log, open(log_file, "a") as log_append:
        log_message(f"开始处理 {total} 个文件 (并行度: {max_workers})", file_path=None)
        # 使用多线程并行处理
        with concurrent.futures.ThreadPoolExecutor(max_workers=max_workers) as executor:
            futures = {executor.submit(process_file, f): f for f in files}
            for future in concurrent.futures.as_completed(futures):
                result = future.result()
                # 实时进度显示
                success_count = processed - skipped
                print(f"\r进度: {processed}/{total} (成功: {success_count} 跳过: {skipped})", end="", flush=True)

        # 最终统计
        success_count = processed - skipped
        log_message(f"\n\n最终统计: 成功 {success_count} 跳过 {skipped}", file_path=None)

# 执行主函数
if __name__ == "__main__":
    main()