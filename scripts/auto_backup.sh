#!/bin/bash
# 晨露自动备份脚本

cd /home/cheche/.openclaw/workspace-chenlu

# 读取保存的 Token
TOKEN=$(cat ~/.github_token)

# 添加所有改动
git add -A

# 提交（如果有改动）
if git diff --cached --quiet; then
    echo "没有需要备份的改动"
    exit 0
fi

# 提交并推送（带重试机制）
git commit -m "🔄 自动备份 - $(date '+%Y-%m-%d %H:%M:%S')"

MAX_RETRIES=3
RETRY_COUNT=0
PUSH_SUCCESS=false

while [ $RETRY_COUNT -lt $MAX_RETRIES ] && [ "$PUSH_SUCCESS" = "false" ]; do
    RETRY_COUNT=$((RETRY_COUNT + 1))
    echo "Push 尝试 $RETRY_COUNT/$MAX_RETRIES..."
    
    if git push https://${TOKEN}@github.com/33333cheche-web/chenlu-memory.git master 2>&1; then
        PUSH_SUCCESS=true
        echo "✅ Push 成功！"
    else
        echo "❌ Push 失败，等待 30 秒后重试..."
        sleep 30
    fi
done

if [ "$PUSH_SUCCESS" = "false" ]; then
    echo "❌ 最终 Push 失败（已重试 $MAX_RETRIES 次）"
fi

echo "✅ 自动备份完成！$(date)"
