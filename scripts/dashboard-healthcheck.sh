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
DASHBOARD_PID=$(pgrep -f "api_server.py" || true)

if [ -z "$DASHBOARD_PID" ]; then
    echo "[$TIMESTAMP] Dashboard 进程未运行，正在启动..." >> "$LOG_FILE"
    
    # 检查 dashboard 状态并重启
    if [ -z "$NEW_PID" ]; then
        echo "[$TIMESTAMP] Dashboard 启动失败，使用 systemd 重试..." >> "$LOG_FILE"
        # 使用 systemd 启动（不再用 nohup，避免端口冲突）
        systemctl --user restart openclaw-dashboard.service
        sleep 3
        
        # 检查 systemd 状态
        if systemctl --user is-active openclaw-dashboard.service >/dev/null 2>&1; then
            SYSTEMD_PID=$(systemctl --user show openclaw-dashboard.service -p MainPID | cut -d= -f2)
            echo "[$TIMESTAMP] Dashboard 已通过 systemd 恢复 ✅ PID: $SYSTEMD_PID" >> "$LOG_FILE"
            $OPENCLAW_HOME/../.npm-global/bin/openclaw message send \
                --channel feishu \
                --target "$TARGET_USER" \
                --message "💧 Dashboard 刚才挂了，晨露已通过 systemd 自动重启成功啦！✅" \
                2>> "$LOG_FILE"
        else
            echo "[$TIMESTAMP] Dashboard systemd 启动也失败了" >> "$LOG_FILE"
            $OPENCLAW_HOME/../.npm-global/bin/openclaw message send \
                --channel feishu \
                --target "$TARGET_USER" \
                --message "⚠️ Dashboard 挂了且自动重启失败！systemd 也无法启动，请找晨露紧急处理！" \
                2>> "$LOG_FILE"
        fi
        exit
    fi
fi

# 检查 HTTP 响应
HTTP_CODE=$(curl -s -o /dev/null -w "%{http_code}" http://localhost:8080 2>/dev/null)
if [ "$HTTP_CODE" != "200" ]; then
    echo "[$TIMESTAMP] Dashboard HTTP 异常 (code: $HTTP_CODE)，尝试重启..." >> "$LOG_FILE"
    
    # 使用 systemd 重启
    systemctl --user restart openclaw-dashboard.service
    sleep 3
    
    if systemctl --user is-active openclaw-dashboard.service > /dev/null 2>&1; then
        echo "[$TIMESTAMP] Dashboard 已通过 systemd 重启 ✅" >> "$LOG_FILE"
        $OPENCLAW_HOME/../.npm-global/bin/openclaw message send \
            --channel feishu \
            --target "$TARGET_USER" \
            --message "💧 Dashboard HTTP 异常，已通过 systemd 自动重启恢复 ✅" \
            2>> "$LOG_FILE"
    else
        echo "[$TIMESTAMP] Dashboard systemd 重启失败" >> "$LOG_FILE"
        $OPENCLAW_HOME/../.npm-global/bin/openclaw message send \
            --channel feishu \
            --target "$TARGET_USER" \
            --message "⚠️ Dashboard 重启失败！HTTP 异常且 systemd 恢复失败，请人工检查！" \
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