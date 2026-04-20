#!/bin/bash
# auto-capture.sh - 统一日报捕获脚本
# 用法：./auto-capture.sh <bot_name> "内容摘要"

BOT_NAME="${1:-baby}"
CONTENT="${2:-对话结束}"

SCRIPT="$HOME/.openclaw/workspace-${BOT_NAME}/skills/baby-memory/scripts/capture.js"

if [ -f "$SCRIPT" ]; then
    node "$SCRIPT" --bot="$BOT_NAME" "$CONTENT"
else
    echo "capture.js not found for $BOT_NAME" >> /tmp/auto-capture-error.log
    exit 1
fi
