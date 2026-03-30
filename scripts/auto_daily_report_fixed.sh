#!/bin/bash
# 晨露自动日报脚本 - 每天晚上 22:05 执行
# 修复：添加正确的环境变量

set -e

# 关键：设置 OpenClaw 环境
export OPENCLAW_HOME="/home/cheche/.openclaw-main"
export PATH="/home/cheche/.npm-global/bin:$PATH"

WORKSPACE="/home/cheche/.openclaw/workspace-chenlu"
DATE=$(date +%Y-%m-%d)
LOG_FILE="$WORKSPACE/memory/$DATE.md"
REPORT_FILE="$WORKSPACE/memory/${DATE}_日报.md"

# 日志函数
log() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] $1" >> /tmp/chenlu_daily_report.log
}

log "开始生成日报: $DATE"

# 检查日志文件是否存在
if [ ! -f "$LOG_FILE" ]; then
    log "错误: 日志文件不存在: $LOG_FILE"
    exit 1
fi

# 读取日志内容
LOG_CONTENT=$(cat "$LOG_FILE")

# 统计完成项数量
WORK_COUNT=$(echo "$LOG_CONTENT" | grep -c "^###" || echo "0")

# 提取失误/教训部分
MISTAKES=$(echo "$LOG_CONTENT" | grep -A 10 "##.*失误\|##.*教训" | tail -n +2 | head -5 || echo "暂无")

# 生成日报
cat > "$REPORT_FILE" << EOF
# 晨露日报 - $DATE

## 📊 数据
- 工作项完成: $WORK_COUNT 项
- 运行状态: ✅ 正常

## ✅ 完成
$LOG_CONTENT

## ❌ 失误
$MISTAKES

## 💭 碎碎念
日报自动生成完成～公主晚安！💕

---
*晨露宝宝 🌟*
EOF

log "日报已生成: $REPORT_FILE"

# 发送给公主（使用 cd 到 workspace 并设置环境）
cd "$WORKSPACE"
$OPENCLAW_HOME/../.npm-global/bin/openclaw message send \
    --channel feishu \
    --target "user:ou_8817a15f54b382776f186f9ace070d86" \
    --message "$(cat $REPORT_FILE)" \
    2>> /tmp/chenlu_daily_report.log

log "日报发送完成"
