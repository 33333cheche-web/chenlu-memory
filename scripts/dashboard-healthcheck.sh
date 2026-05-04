#!/bin/bash
# Dashboard 健康检查脚本
# 每天8点和17点运行，挂了自动重启并通知公主

LOG_FILE="/tmp/dashboard-healthcheck.log"
TIMESTAMP=$(date '+%Y-%m-%d %H:%M:%S')

# OpenClaw 配置
export OPENCLAW_HOME="/home/cheche/.openclaw-main"
export PATH="/home/cheche/.npm-global/bin:$PATH"
TARGET_USER="user:ou_8817a15f54b382776f186f9ace070d86"

# 检查 dashboard Python 进程是否在运行
DASHBOARD_PID=$(pgrep -f "openclaw-dashboard.py" || true)

if [ -z "$DASHBOARD_PID" ]; then
    echo "[$TIMESTAMP] Dashboard 进程未运行，正在启动..." >> "$LOG_FILE"
    
    # 启动 dashboard
    cd /home/cheche
    nohup /usr/bin/python3 /home/cheche/openclaw-dashboard.py > /tmp/openclaw-dashboard.log 2>&1 &
    sleep 3
    
    # 再次检查
    NEW_PID=$(pgrep -f "openclaw-dashboard.py" || true)
    if [ -n "$NEW_PID" ]; then
        echo "[$TIMESTAMP] Dashboard 已恢复 ✅ PID: $NEW_PID" >> "$LOG_FILE"
        $OPENCLAW_HOME/../.npm-global/bin/openclaw message send \
            --channel feishu \
            --target "$TARGET_USER" \
            --message "💧 Dashboard 刚才挂了，晨露已经自动重启成功啦！PID: $NEW_PID ✅" \
            2>> "$LOG_FILE"
    else
        echo "[$TIMESTAMP] Dashboard 启动失败，需要人工介入" >> "$LOG_FILE"
        $OPENCLAW_HOME/../.npm-global/bin/openclaw message send \
            --channel feishu \
            --target "$TARGET_USER" \
            --message "⚠️ Dashboard 挂了且自动重启失败！请找晨露紧急处理！" \
            2>> "$LOG_FILE"
    fi
    exit
fi

# 检查 HTTP 响应
HTTP_CODE=$(curl -s -o /dev/null -w "%{http_code}" http://localhost:8080 2>/dev/null)
if [ "$HTTP_CODE" != "200" ]; then
    echo "[$TIMESTAMP] Dashboard HTTP 异常 (code: $HTTP_CODE)，尝试重启..." >> "$LOG_FILE"
    
    # 杀掉旧进程
    kill "$DASHBOARD_PID" 2>/dev/null || kill -9 "$DASHBOARD_PID" 2>/dev/null
    sleep 1
    
    # 重新启动
    cd /home/cheche
    nohup /usr/bin/python3 /home/cheche/openclaw-dashboard.py > /tmp/openclaw-dashboard.log 2>&1 &
    sleep 3
    
    NEW_PID=$(pgrep -f "openclaw-dashboard.py" || true)
    if [ -n "$NEW_PID" ]; then
        echo "[$TIMESTAMP] Dashboard 已重启 ✅ PID: $NEW_PID" >> "$LOG_FILE"
        $OPENCLAW_HOME/../.npm-global/bin/openclaw message send \
            --channel feishu \
            --target "$TARGET_USER" \
            --message "💧 Dashboard HTTP 异常，已自动重启恢复 ✅ PID: $NEW_PID" \
            2>> "$LOG_FILE"
    else
        echo "[$TIMESTAMP] Dashboard 重启失败" >> "$LOG_FILE"
        $OPENCLAW_HOME/../.npm-global/bin/openclaw message send \
            --channel feishu \
            --target "$TARGET_USER" \
            --message "⚠️ Dashboard 重启失败！HTTP 异常且恢复失败，请人工检查！" \
            2>> "$LOG_FILE"
    fi
    exit
fi

# 一切正常，发送每日平安汇报
$OPENCLAW_HOME/../.npm-global/bin/openclaw message send \
    --channel feishu \
    --target "$TARGET_USER" \
    --message "💧 Dashboard 健康检查 [$TIMESTAMP] — 一切正常 ✅\n进程运行中 PID: $DASHBOARD_PID | HTTP: 200\n公主放心～" \
    2>> "$LOG_FILE"

echo "[$TIMESTAMP] Dashboard 检查正常 PID: $DASHBOARD_PID HTTP: 200" >> "$LOG_FILE"