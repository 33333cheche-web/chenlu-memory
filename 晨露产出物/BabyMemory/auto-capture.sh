#!/bin/bash
# auto-capture.sh - 自动捕获对话到 Baby Memory System
# 
# 用法: ./auto-capture.sh {bot_name} "对话摘要内容"
# 示例: ./auto-capture.sh sunny "用户询问天气情况"

set -e

# 配置
BOT_NAME="${1:-sunny}"
CONTENT="${2:-}"
HOME_DIR="${HOME}"
WORKSPACE="${HOME_DIR}/.openclaw/workspace-${BOT_NAME}"
LOG_FILE="${WORKSPACE}/memory/auto-capture.log"

# 检查参数
if [ -z "$CONTENT" ]; then
    echo "❌ 错误: 未提供内容"
    echo "用法: $0 {bot_name} \"对话摘要内容\""
    exit 1
fi

# 检查工作区是否存在
if [ ! -d "$WORKSPACE" ]; then
    echo "❌ 错误: 工作区不存在: $WORKSPACE"
    echo "请先运行: node scripts/init.js --bot=${BOT_NAME}"
    exit 1
fi

# 检查 capture.js 是否存在
CAPTURE_SCRIPT="${WORKSPACE}/skills/baby-memory/scripts/capture.js"
if [ ! -f "$CAPTURE_SCRIPT" ]; then
    echo "❌ 错误: capture.js 不存在: $CAPTURE_SCRIPT"
    exit 1
fi

# 记录日志函数
log() {
    local timestamp=$(date '+%Y-%m-%d %H:%M:%S')
    echo "[$timestamp] $1" | tee -a "$LOG_FILE"
}

# 确保日志目录存在
mkdir -p "$(dirname "$LOG_FILE")"

log "=== Auto Capture Start ==="
log "Bot: $BOT_NAME"
# 截断内容用于日志显示
CONTENT_PREVIEW="$CONTENT"
if [ ${#CONTENT} -gt 100 ]; then
    CONTENT_PREVIEW=$(echo "$CONTENT" | head -c 100)
    CONTENT_PREVIEW="${CONTENT_PREVIEW}..."
fi
log "Content: $CONTENT_PREVIEW"

# 执行捕获
if node "$CAPTURE_SCRIPT" --bot="$BOT_NAME" "$CONTENT"; then
    log "✅ 捕获成功"
    exit 0
else
    log "❌ 捕获失败"
    exit 1
fi
