#!/bin/bash

# 设置脚本出错时自动退出
set -e

# 定义日志文件
LOG_FILE=$(date +"%Y%m%d%H%M%S")_process.log

# 输出脚本开始运行的信息
echo "-------------------------------------" | tee -a ${LOG_FILE}
echo "Starting script execution at $(date)" | tee -a ${LOG_FILE}
echo "Log file: $(readlink -f ${LOG_FILE})" | tee -a ${LOG_FILE}
echo "-------------------------------------" | tee -a ${LOG_FILE}

# 定义第一个和第二个 Python 脚本的路径
SCRIPT1="diamond_blastp_for_allfaa_for_remote_LP_HGT.py"
SCRIPT2="COG_combined_for_alltxt_scripts_for_4147LP_HGT_gene_distribution.py"

# 检查第一个脚本是否存在
if [ ! -f "${SCRIPT1}" ]; then
    echo "Error: Script ${SCRIPT1} not found!" | tee -a ${LOG_FILE}
    exit 1
fi

# 检查第二个脚本是否存在
if [ ! -f "${SCRIPT2}" ]; then
    echo "Error: Script ${SCRIPT2} not found!" | tee -a ${LOG_FILE}
    exit 1
fi

# 输出第一个脚本运行信息
echo "-------------------------------------" | tee -a ${LOG_FILE}
echo "Running ${SCRIPT1}..." | tee -a ${LOG_FILE}
echo "-------------------------------------" | tee -a ${LOG_FILE}

# 执行第一个脚本并记录输出
python "${SCRIPT1}" 2>&1 | tee -a ${LOG_FILE}

# 检查第一个脚本的退出状态
if [ $? -ne 0 ]; then
    echo "-------------------------------------" | tee -a ${LOG_FILE}
    echo "Error: ${SCRIPT1} failed!" | tee -a ${LOG_FILE}
    echo "Script execution terminated." | tee -a ${LOG_FILE}
    echo "Check the log file for details: $(readlink -f ${LOG_FILE})" | tee -a ${LOG_FILE}
    exit 1
else
    echo "-------------------------------------" | tee -a ${LOG_FILE}
    echo "${SCRIPT1} completed successfully." | tee -a ${LOG_FILE}
    echo "-------------------------------------" | tee -a ${LOG_FILE}
fi

# 输出第二个脚本运行信息
echo "-------------------------------------" | tee -a ${LOG_FILE}
echo "Running ${SCRIPT2}..." | tee -a ${LOG_FILE}
echo "-------------------------------------" | tee -a ${LOG_FILE}

# 执行第二个脚本并记录输出
python "${SCRIPT2}" 2>&1 | tee -a ${LOG_FILE}

# 输出脚本结束运行的信息
echo "-------------------------------------" | tee -a ${LOG_FILE}
echo "All done! Script execution completed at $(date)" | tee -a ${LOG_FILE}
echo "Log file: $(readlink -f ${LOG_FILE})" | tee -a ${LOG_FILE}
echo "-------------------------------------" | tee -a ${LOG_FILE}