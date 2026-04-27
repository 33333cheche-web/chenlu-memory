#!/bin/bash
# Dashboard 健康检查脚本
# 每天8点和17点运行，挂了自动重启

LOG_FILE="/tmp/dashboard-healthcheck.log"
TIMESTAMP=$(date '+%Y-%m-%d %H:%M:%S')

# 检查 dashboard 是否在运行
if ! systemctl --user is-active --quiet openclaw-dashboard.service; then
    echo "[$TIMESTAMP] Dashboard 挂了，正在恢复..." >> "$LOG_FILE"
    systemctl --user start openclaw-dashboard.service
    sleep 2
    if systemctl --user is-active --quiet openclaw-dashboard.service; then
        echo "[$TIMESTAMP] Dashboard 已恢复 ✅" >> "$LOG_FILE"
    else
        echo "[$TIMESTAMP] Dashboard 恢复失败，请找晨露修" >> "$LOG_FILE"
    fi
    exit
fi

# 检查 HTTP 响应
HTTP_CODE=$(curl -s -o /dev/null -w "%{http_code}" http://localhost:8080 2>/dev/null)
if [ "$HTTP_CODE" != "200" ]; then
    echo "[$TIMESTAMP] Dashboard 异常，尝试重启..." >> "$LOG_FILE"
    systemctl --user restart openclaw-dashboard.service
    exit
fi

# 正常时不输出，日志只保留异常
