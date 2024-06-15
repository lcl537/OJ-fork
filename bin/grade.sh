#!/bin/bash

# 标准答案文件的路径
ANSWER_FILE="/path/to/answer.txt"

# 存放待批改代码文件的目录路径
CODE_DIR="/path/to/code_directory"

# 管理服务器的URL
MANAGE_URL="<manage>/submission"

# 遍历代码目录中的所有 .py 文件
for CODE_FILE in "$CODE_DIR"/*.py; do
    # 从文件名中提取ID（去掉扩展名）
    ID=$(basename "$CODE_FILE" .py)
    
    # 标准输出和标准错误的文件路径
    STDOUT_FILE="$CODE_DIR/$ID.stdout"
    STDERR_FILE="$CODE_DIR/$ID.stderr"
    
    # 执行代码文件，将标准输出和标准错误分别保存到文件中
    python3 "$CODE_FILE" >"$STDOUT_FILE" 2>"$STDERR_FILE"
    
    # 如果标准错误文件不为空，说明有编译错误
    if [ -s "$STDERR_FILE" ]; then
        RESULT="ERROR"
    else
        # 比较标准输出文件和答案文件
        if diff -q "$STDOUT_FILE" "$ANSWER_FILE" > /dev/null; then
            RESULT="CORRECT"
        else
            RESULT="INCORRECT"
        fi
    fi
    
    # 将结果以JSON格式发送到管理服务器
    curl -X PATCH "$MANAGE_URL" -H "Content-Type: application/json" -d "{\"id\": \"$ID\", \"result\": \"$RESULT\"}"
done

