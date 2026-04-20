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

# 推送（直接在工作目录 push，不要用临时目录 clone）
git push origin master >> "$LOG_FILE" 2>&1

echo "[$(date '+%Y-%m-%d %H:%M:%S')] ✅ 备份成功" >> "$LOG_FILE"
echo "" >> "$LOG_FILE"
