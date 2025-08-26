import os
import subprocess
from concurrent.futures import ProcessPoolExecutor
from pathlib import Path
import time
from tqdm import tqdm  # 需要安装tqdm库

MAX_RETRY = 3  # 最大重试次数
SUCCESS_FLAG = "_SUCCESS"  # 完成标志文件

def process_file(input_tsv, output_root, taxdump_path):
    """处理单个TSV文件（含重试机制）"""
    relative_path = Path(input_tsv).relative_to("All_4147_LP_faa_HGT_search")
    output_dir = output_root / relative_path.with_suffix('')
    success_flag = output_dir / SUCCESS_FLAG
    
    # 如果已完成则直接返回
    if success_flag.exists():
        return {"status": "skipped", "input": input_tsv}
    
    # 创建输出目录（原子操作）
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # 重试逻辑
    for attempt in range(MAX_RETRY + 1):
        cmd = [
            "hgtector", "analyze",
            "-i", str(input_tsv),
            "-o", str(output_dir),
            "-t", taxdump_path,
            "--donor-name", "--donor-rank", "family"
        ]
        
        try:
            result = subprocess.run(
                cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                check=True  # 非零返回码时抛出异常
            )
            
            # 标记成功完成
            success_flag.touch()
            return {"status": "success", "input": input_tsv}
            
        except subprocess.CalledProcessError as e:
            if attempt == MAX_RETRY:  # 最终重试失败
                # 清理可能残留的文件
                if output_dir.exists():
                    for f in output_dir.glob("*"):
                        if f.is_file(): 
                            f.unlink()
                    output_dir.rmdir()
                return {
                    "status": "failed",
                    "input": input_tsv,
                    "error": str(e),
                    "stderr": e.stderr
                }
            
            # 指数退避重试
            time.sleep(2 ** attempt)

if __name__ == "__main__":
    # 配置参数
    input_dir = Path("All_4147_LP_faa_HGT_search")
    output_root = Path("All_4147_LP_faa_HGT_analyze_family")
    taxdump_path = "/data/Share/zhanxy_data/db/hgtdb_20230102/taxdump/"
    max_workers = 20  # 固定20个线程
    
    # 查找所有未完成的TSV文件
    all_files = [p for p in input_dir.rglob("*.tsv") if p.is_file()]
    pending_files = [
        str(f) for f in all_files
        if not (output_root / f.relative_to(input_dir).with_suffix('') / SUCCESS_FLAG).exists()
    ]
    
    print(f"Total files: {len(all_files)} | Pending: {len(pending_files)}")
    
    # 创建进程池
    with ProcessPoolExecutor(max_workers=max_workers) as executor:
        futures = {
            executor.submit(process_file, Path(f), output_root, taxdump_path): f
            for f in pending_files
        }
        
        # 用进度条跟踪进度
        success_count = skipped_count = failed_count = 0
        with tqdm(total=len(futures), desc="Processing") as pbar:
            for future in futures:
                result = future.result()
                pbar.update(1)
                
                if result["status"] == "success":
                    success_count += 1
                elif result["status"] == "skipped":
                    skipped_count += 1
                elif result["status"] == "failed":
                    failed_count += 1
                    print(f"\nFailed: {result['input']}")
                    print(f"Error: {result.get('error', '')}")
                    print(f"Stderr: {result.get('stderr', '')[:500]}...")  # 截断输出

    # 输出统计报告
    print("\nProcessing Summary:")
    print(f"Successfully processed: {success_count}")
    print(f"Skipped completed files: {skipped_count}")
    print(f"Failed after {MAX_RETRY} retries: {failed_count}")
    if failed_count > 0:
        print("\nTips: 可以尝试以下方法处理失败任务：")
        print("1. 检查错误信息中的输入文件路径")
        print("2. 确认hgtector命令能单独执行成功")
        print("3. 手动清理残留的空白输出目录")
        print("4. 调整MAX_RETRY参数后重新运行")