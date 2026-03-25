#!/bin/bash
# 晨露记忆库自动备份脚本
# 运行此脚本将 SOUL.md, MEMORY.md, AGENTS.md 等核心文件备份到 GitHub

BACKUP_DIR="/home/cheche/.openclaw/workspace-chenlu/.github-backup"
SOURCE_DIR="/home/cheche/.openclaw/workspace-chenlu"

echo "🌟 开始备份晨露核心记忆文件..."

cd "$BACKUP_DIR" || exit 1

# 复制核心文件
cp "$SOURCE_DIR/SOUL.md" .
cp "$SOURCE_DIR/MEMORY.md" .
cp "$SOURCE_DIR/AGENTS.md" .
cp "$SOURCE_DIR/IDENTITY.md" .
cp "$SOURCE_DIR/USER.md" .
cp "$SOURCE_DIR/TOOLS.md" .
cp -r "$SOURCE_DIR/晨露产出物" .

# 添加所有变更
git add -A

# 提交（如果有变更）
if git diff --cached --quiet; then
    echo "✅ 没有新的变更需要备份"
else
    git commit -m "🌟 自动备份: $(date '+%Y-%m-%d %H:%M:%S')"
    git push origin main
    echo "✅ 备份完成！已推送到 GitHub"
fi
