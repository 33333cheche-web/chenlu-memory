#!/bin/bash
# 💧 晨露记忆备份脚本 v3.2 — 参考 Melody 直接 push 方式
# 每周一 23:10 执行

set -euo pipefail

WORKSPACE="/home/cheche/.openclaw/workspace-chenlu"
DATE=$(date '+%Y-%m-%d %H:%M:%S')
LOG_FILE="/tmp/chenlu-memory-backup.log"

echo "===== 💧 晨露记忆备份开始 =====" >> "$LOG_FILE"
echo "时间: $DATE" >> "$LOG_FILE"

cd "$WORKSPACE" || exit 1

# 只添加核心文件（避免 .gitignore 漏掉的文件混入）
git add memory/daily/ SOUL.md MEMORY.md AGENTS.md IDENTITY.md USER.md TOOLS.md HEARTBEAT.md scripts/ .gitignore "晨露产出物/" 2>/dev/null || true

# 检查是否有变更需要提交
if git diff --cached --quiet; then
    echo "[$DATE] ℹ️ 无变更，跳过提交" >> "$LOG_FILE"
    exit 0
fi

# 提交
git commit -m "💧 晨露记忆备份 - $DATE" 2>/dev/null || {
    echo "[$DATE] ℹ️ 无变更需要提交" >> "$LOG_FILE"
    exit 0
}

# 推送（带重试机制）—— 使用环境变量中的token避免泄露
MAX_RETRIES=3
RETRY_COUNT=0
PUSH_SUCCESS=false

# 从环境变量或文件读取token（不要在脚本中硬编码）
TOKEN="${GITHUB_TOKEN:-$(cat ~/.github_token 2>/dev/null || echo '')}"

if [ -z "$TOKEN" ]; then
    echo "[$DATE] ❌ 未找到GitHub Token，请设置 GITHUB_TOKEN 环境变量或 ~/.github_token 文件" >> "$LOG_FILE"
    exit 1
fi

while [ $RETRY_COUNT -lt $MAX_RETRIES ] && [ "$PUSH_SUCCESS" = "false" ]; do
    RETRY_COUNT=$((RETRY_COUNT + 1))
    echo "[$DATE] 🚀 Push 尝试 $RETRY_COUNT/$MAX_RETRIES..." >> "$LOG_FILE"
    
    if git push "https://${TOKEN}@github.com/33333cheche-web/chenlu-memory.git" master >> "$LOG_FILE" 2>&1; then
        PUSH_SUCCESS=true
        echo "[$DATE] ✅ Push 成功！" >> "$LOG_FILE"
    else
        echo "[$DATE] ❌ Push 失败，等待 30 秒后重试..." >> "$LOG_FILE"
        sleep 30
    fi
done

if [ "$PUSH_SUCCESS" = "false" ]; then
    echo "[$DATE] ❌ 最终 Push 失败（已重试 $MAX_RETRIES 次）" >> "$LOG_FILE"
fi
