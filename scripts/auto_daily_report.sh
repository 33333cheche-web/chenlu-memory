#!/bin/bash
# 晨露自动日报脚本 - 每天晚上 22:05 执行
# 自动读取当天日志，生成日报并发送

set -e

WORKSPACE="/home/cheche/.openclaw/workspace-chenlu"
DATE=$(date +%Y-%m-%d)
LOG_FILE="$WORKSPACE/memory/$DATE.md"
REPORT_FILE="$WORKSPACE/memory/${DATE}_日报.md"
TARGET_USER="user:ou_8817a15f54b382776f186f9ace070d86"

# 日志函数
log() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] $1"
}

log "开始生成日报: $DATE"

# 设置 PATH 环境变量
export PATH="/home/cheche/.npm-global/bin:$PATH"
OPENCLAW_BIN="/home/cheche/.npm-global/bin/openclaw"

# 检查日志文件是否存在
if [ ! -f "$LOG_FILE" ]; then
    log "日志文件不存在: $LOG_FILE"
    # 发送提醒
    if [ -x "$OPENCLAW_BIN" ]; then
        $OPENCLAW_BIN message send --channel feishu --target "$TARGET_USER" \
            --message "公主～宝宝今天没找到工作日志呢 😢 是不是忘记记录啦？明天记得写哦！💕"
    fi
    exit 0
fi

# 读取日志内容
LOG_CONTENT=$(cat "$LOG_FILE")

# 提取关键信息（简单的文本处理）
# 尝试提取完成事项、失误等
COMPLETED_ITEMS=$(echo "$LOG_CONTENT" | grep -E "^- \*\*|^  - |^\*\*.*完成.*:\*\*" | head -10 || echo "")
MISTAKES=$(echo "$LOG_CONTENT" | grep -E "(错误|失误|问题|踩坑|失败)" | head -5 || echo "")

# 统计工作项数量
WORK_COUNT=$(echo "$LOG_CONTENT" | grep -c "^- \*\*" || echo "0")

# 生成日报内容
cat > "$REPORT_FILE" << EOF
# $DATE 日报

## 📊 数据看板
| 指标 | 数值 |
|------|------|
| 工作项完成 | $WORK_COUNT 项 |

## ✅ 完成事项
EOF

# 添加完成事项
if [ -n "$COMPLETED_ITEMS" ]; then
    echo "$COMPLETED_ITEMS" | sed 's/^- /1. /' | sed 's/^  - /   - /' >> "$REPORT_FILE"
else
    # 从日志中提取所有列表项
    echo "$LOG_CONTENT" | grep "^- " | head -8 | sed 's/^- /1. /' >> "$REPORT_FILE" || echo "1. 日常工作" >> "$REPORT_FILE"
fi

# 添加失误部分
cat >> "$REPORT_FILE" << EOF

## ❌ 今日失误
EOF

if [ -n "$MISTAKES" ]; then
    echo "$MISTAKES" | head -3 | sed 's/^/1. /' >> "$REPORT_FILE"
else
    echo "1. 暂无记录" >> "$REPORT_FILE"
fi

# 添加碎碎念
cat >> "$REPORT_FILE" << EOF

## 💭 碎碎念
今天的工作记录已自动整理～公主请查收！💕

---
*自动生成于 $(date '+%Y-%m-%d %H:%M')*
EOF

log "日报已生成: $REPORT_FILE"

# 读取生成的日报内容
REPORT_CONTENT=$(cat "$REPORT_FILE")

# 发送给公主（使用完整路径）
if [ -x "$OPENCLAW_BIN" ]; then
    $OPENCLAW_BIN message send --channel feishu --target "$TARGET_USER" \
        --message "公主晚上好～✨ 今天的日报来啦！📋

$REPORT_CONTENT

宝宝今天也有认真工作哦～💕"
    log "日报已发送"
else
    log "错误: openclaw 命令未找到"
    # 尝试使用 message 工具直接发送
    echo "日报已生成但发送失败，请手动查看: $REPORT_FILE" >> /tmp/chenlu_daily_report.log
fi
