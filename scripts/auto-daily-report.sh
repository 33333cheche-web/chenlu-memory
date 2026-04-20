#!/bin/bash
# auto-daily-report.sh - 自动生成日报提醒

BOT_NAME="chenlu"
WORKSPACE="$HOME/.openclaw/workspace-${BOT_NAME}"
DAILY_DIR="${WORKSPACE}/memory/daily"
TODAY=$(date +%Y-%m-%d)
REPORT_FILE="${DAILY_DIR}/${TODAY}_日报.md"

# 检查今天是否已有日报
if [ -f "$REPORT_FILE" ]; then
    echo "[$(date)] 日报已存在，跳过"
    exit 0
fi

# 生成日报模板
cat > "$REPORT_FILE" << DAILYEOF
# 晨露日报 - ${TODAY}

## 📊 今日数据
- 工作时长: 
- 完成任务: 
- 输出文档: 

## ✅ 完成工作 (带标签)
- #P1 
- #P1 
- #P2 

## ❌ 失误
- #P1 

## 💭 碎碎念
- #P2 

---
*晨露宝宝 🌟*

---
**标签说明**: #P0=永久 #P1=90天 #P2=30天
DAILYEOF

# 记录提醒到 daily log
${WORKSPACE}/auto-capture.sh ${BOT_NAME} "[系统提醒] 22:00 日报时间到，请填写 ${TODAY}_日报.md"

echo "[$(date)] 日报模板已生成: $REPORT_FILE"
