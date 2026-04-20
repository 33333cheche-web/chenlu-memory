#!/bin/bash
# ============================================================
# Baby Memory Daily Triage - 每日 P0/P1/P2 自动分拣脚本
# 扫描昨天/今天的 daily log，按标签分发到 P0/P1/P2 月度文件
# cron: 每天 23:59 或每小时检查一次
# ============================================================

MEMORY_DIR="/home/cheche/.openclaw/workspace-chenlu/memory"
DAILY_DIR="$MEMORY_DIR/daily"
P0_DIR="$MEMORY_DIR/P0"
P1_DIR="$MEMORY_DIR/P1"
P2_DIR="$MEMORY_DIR/P2"

# 颜色日志
log() { echo "[$(date '+%Y-%m-%d %H:%M')] $1"; }

# 确保目录存在
mkdir -p "$P0_DIR" "$P1_DIR" "$P2_DIR"

# 获取日期（默认昨天）
TARGET_DATE="${1:-$(date -d 'yesterday' '+%Y-%m-%d')}"
TODAY_DATE="$(date '+%Y-%m-%d')"

log "开始分拣: $TARGET_DATE"

# 检查目标文件
DAILY_FILE="$DAILY_DIR/${TARGET_DATE}.md"
if [[ ! -f "$DAILY_FILE" ]]; then
    log "文件不存在: $DAILY_FILE，跳过"
    exit 0
fi

# 提取年月（用于月度归档文件名）
YEAR_MONTH="${TARGET_DATE:0:7}"  # 2026-04

# 分拣函数：提取指定标签行，追加到月度文件
triage_tag() {
    local tag="$1"       # #P0, #P1, #P2
    local target_dir="$2"
    local label="$3"     # P0, P1, P2

    local target_file="$target_dir/${YEAR_MONTH}.md"

    # 提取所有该标签行（去掉标签本身前面的 #P0 格式，保留完整行）
    # 格式: #P0 09:27 内容描述
    grep -E "^${tag}[[:space:]]" "$DAILY_FILE" > /tmp/triage_${label}_tmp.txt 2>/dev/null

    if [[ -s /tmp/triage_${label}_tmp.txt ]]; then
        # 追加到月度文件（带日期分隔符）
        {
            echo ""
            echo "## 📅 ${TARGET_DATE}"
            cat /tmp/triage_${label}_tmp.txt
        } >> "$target_file"

        local count=$(wc -l < /tmp/triage_${label}_tmp.txt)
        log "✅ $label: +${count} 条 → $target_file"
        rm /tmp/triage_${label}_tmp.txt
    else
        log "⏭️  $label: 无新记录"
    fi
}

# 执行分拣
triage_tag "#P0" "$P0_DIR" "P0"
triage_tag "#P1" "$P1_DIR" "P1"
triage_tag "#P2" "$P2_DIR" "P2"

log "分拣完成: $TARGET_DATE"
