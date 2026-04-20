#!/bin/bash
# 💧 晨露记忆备份脚本 v3.4 — 使用 clean-history 分支（避免旧提交中的 Token）
# 每周一 23:10 执行

set -euo pipefail

WORKSPACE="/home/cheche/.openclaw/workspace-chenlu"
DATE=$(date '+%Y-%m-%d %H:%M:%S')
LOG_FILE="/tmp/chenlu-memory-backup.log"

echo "===== 💧 晨露记忆备份开始 =====" >> "$LOG_FILE"
echo "时间: $DATE" >> "$LOG_FILE"

cd "$WORKSPACE" || exit 1

# 切换到 clean-history 分支（避免 master 分支上的旧 Token 提交）
git checkout clean-history 2>/dev/null || git checkout -b clean-history

# 只添加核心文件
git add memory/daily/ SOUL.md MEMORY.md AGENTS.md IDENTITY.md USER.md TOOLS.md HEARTBEAT.md scripts/ .gitignore "晨露产出物/" 2>/dev/null || true

# 检查是否有变更
if git diff --cached --quiet; then
    echo "[$DATE] ℹ️ 无变更，跳过提交" >> "$LOG_FILE"
    git checkout master 2>/dev/null || true
    exit 0
fi

# 提交
git commit -m "💧 晨露记忆备份 - $DATE" 2>/dev/null || {
    echo "[$DATE] ℹ️ 无变更需要提交" >> "$LOG_FILE"
    git checkout master 2>/dev/null || true
    exit 0
}

# 推送（使用 --ipv4 解决 IPv6 连接问题）
git push --ipv4 origin clean-history >> "$LOG_FILE" 2>&1

echo "[$(date '+%Y-%m-%d %H:%M:%S')] ✅ 备份成功" >> "$LOG_FILE"
echo "" >> "$LOG_FILE"

# 切回 master
git checkout master 2>/dev/null || true