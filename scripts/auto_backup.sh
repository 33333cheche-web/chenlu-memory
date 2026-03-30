#!/bin/bash
# 晨露自动备份脚本

cd /home/cheche/.openclaw/workspace-chenlu

# 读取保存的 Token
TOKEN=$(cat ~/.github_token)

# 添加所有改动
git add -A

# 提交（如果有改动）
if git diff --cached --quiet; then
    echo "没有需要备份的改动"
    exit 0
fi

# 提交并推送
git commit -m "🔄 自动备份 - $(date '+%Y-%m-%d %H:%M:%S')"
git push https://${TOKEN}@github.com/33333cheche-web/chenlu-memory.git master

echo "✅ 自动备份完成！$(date)"
