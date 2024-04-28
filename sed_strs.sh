#!/bin/bash

# 检查是否提供了足够的参数
if [ $# -lt 5 ]; then
    echo "Usage: $0 文件名 [开始行号,如果为\"\"则从第一行开始] [结束行号,如果为\"\"则搜索至最后一行]  [替换前ID] [替换后ID]"
    echo "ERR:参数不够"
    exit 1
fi
if [ -z "$1" ] || [ -z "$4" ]|| [ -z "$5" ]; then
    echo "Usage: $0 文件名 [开始行号,如果为\"\"则从第一行开始] [结束行号,如果为\"\"则搜索至最后一行]  [替换前ID] [替换后ID]"
    echo "ERR:[文件名] OR [替换前ID] OR [替换后ID] 是空字符串"
    exit 2
fi

file_opt=$1
# 统计文件行数
total_lines=$(wc -l < "${file_opt}")

# 设置默认的开始搜索行号和结束搜索行号
start_line=1
end_line=$total_lines

# 检查是否提供了命令行参数，并相应地更新开始搜索行号和结束搜索行号
if [ -n "$2" ]; then
    start_line=$2
else
    echo "开始行号为空，从第${start_line}行开始"
fi

if [ -n "$3" ]; then
    end_line=$3
else
    echo "结束行号为空，至${end_line}行结束"
fi
if [ $start_line -lt 1 ]; then
    echo "开始行号${start_line}小于文件开始，修正至第1行"
    start_line=1
    
fi
if [ $end_line -gt $total_lines ]; then
    echo "结束行号${end_line}大于文件总行号，修正至第${total_lines}行"
    end_line=$total_lines
    
fi

if [ "$end_line" -lt "$start_line" ]; then
    echo "Usage: $0 文件名 [开始行号,如果为\"\"则从第一行开始] [结束行号,如果为\"\"则搜索至最后一行]  [替换前ID] [替换后ID]"
    echo "ERR:结束行号小于开始行号"
    exit 3
fi
old_context=",${4}|"
new_context=",${5}|"
echo "[Param]: file:${file_opt}, start_line ${start_line}, end_line ${end_line}, old_context ${old_context}, new_context ${new_context}"

# 执行替换操作
sed -i "${start_line},${end_line}s/${old_context}/${new_context}/g" ${file_opt}
# 查看将结果

cat_start_line=$((start_line - 2))
if [ $cat_start_line -lt 1 ]; then
    cat_start_line=1
fi
cat_end_line=$((end_line + 2))
if [ $cat_end_line -gt $total_lines ]; then
    sum=$total_lines
fi
cat -n ${file_opt} | head -n ${cat_end_line} | tail -n +${cat_start_line}  #显示10行到50行
