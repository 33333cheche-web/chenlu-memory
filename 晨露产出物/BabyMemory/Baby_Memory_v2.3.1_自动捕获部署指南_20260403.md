# Baby Memory System v2.3.1 - 自动捕获部署指南

**版本**: v2.3.1  
**更新日期**: 2026-04-03  
**适用 Bot**: Sunny（及其他 5 个 Bots）

---

## 📦 文件清单

```
baby-memory/
├── scripts/
│   ├── init.js          # 初始化脚本
│   ├── capture.js       # 捕获脚本
│   └── cleanup.js       # 清理脚本
├── auto-capture.sh      # ⭐ 新增：自动捕获包装脚本
├── config/
│   └── default.json     # 配置文件
├── package.json         # 项目信息
└── SKILL.md             # 使用说明
```

---

## 🚀 部署步骤

### 步骤 1: 复制 Skill 到 Sunny

```bash
# 创建目录
mkdir -p ~/.openclaw/workspace-sunny/skills/baby-memory

# 复制所有文件（包括 auto-capture.sh）
cp -r baby-memory/* ~/.openclaw/workspace-sunny/skills/baby-memory/
```

### 步骤 2: 初始化 Sunny

```bash
cd ~/.openclaw/workspace-sunny/skills/baby-memory
node scripts/init.js --bot=sunny
```

**输出示例**:
```
=== 初始化 Baby Memory System for sunny ===
✅ 共享层
✅ 私有层
✅ MEMORY.md 已精简
=== ✅ 初始化成功 ===
```

### 步骤 3: 设置权限

```bash
chmod +x ~/.openclaw/workspace-sunny/skills/baby-memory/auto-capture.sh
```

### 步骤 4: 测试自动捕获

```bash
~/.openclaw/workspace-sunny/skills/baby-memory/auto-capture.sh sunny "测试自动捕获功能"
```

**验证记录**:
```bash
cat ~/.openclaw/workspace-sunny/memory/daily/2026-04-03.md
```

应该能看到刚刚的记录。

---

## 🔧 自动捕获配置

### 方式 1: 心跳触发（推荐）

在 `HEARTBEAT.md` 中添加：

```bash
# 对话后自动捕获
~/.openclaw/workspace-sunny/skills/baby-memory/auto-capture.sh sunny "对话摘要"
```

### 方式 2: 消息事件触发

在 OpenClaw 配置中添加事件处理器：

```json
{
  "events": {
    "message_received": [
      "~/.openclaw/workspace-sunny/skills/baby-memory/auto-capture.sh sunny \"${message.summary}\""
    ]
  }
}
```

### 方式 3: 定时任务

```bash
# 每 5 分钟检查并捕获
crontab -e
*/5 * * * * ~/.openclaw/workspace-sunny/skills/baby-memory/auto-capture.sh sunny "定时捕获"
```

---

## 📋 日常使用

### 查看今日记录

```bash
cat ~/.openclaw/workspace-sunny/memory/daily/$(date +%Y-%m-%d).md
```

### 查看跨 Bot 日志

```bash
cat ~/.openclaw/shared-memory/cross-agent-log.md
```

### 运行清理（试运行）

```bash
node ~/.openclaw/workspace-sunny/skills/baby-memory/scripts/cleanup.js --bot=sunny --dry-run
```

### 运行清理（正式）

```bash
node ~/.openclaw/workspace-sunny/skills/baby-memory/scripts/cleanup.js --bot=sunny
```

---

## 🔍 故障排查

| 问题 | 检查命令 | 解决方案 |
|------|---------|---------|
| 捕获失败 | `cat memory/auto-capture.log` | 查看错误日志 |
| 文件不存在 | `ls -la memory/daily/` | 检查目录权限 |
| 无跨 Bot 记录 | `cat shared-memory/cross-agent-log.md` | 确保是重要事件 |
| 初始化失败 | `node scripts/init.js --bot=sunny` | 重新运行初始化 |

---

## ✅ 验证清单

部署完成后，检查以下项目：

- [ ] `~/.openclaw/shared-memory/.abstract` 存在
- [ ] `~/.openclaw/workspace-sunny/memory/.abstract` 存在
- [ ] `auto-capture.sh` 可执行
- [ ] 测试记录写入 daily log
- [ ] 重要事件写入 cross-agent-log
- [ ] 自动触发机制配置完成

---

## 📝 重要提示

1. **不要手动修改** shared-memory/ 下的文件
2. **自动捕获失败时**，系统会记录日志，不影响主流程
3. **重要事件**（含"完成"、"部署"等关键词）会自动写入跨 Bot 日志
4. **每天 22:00** 建议运行 cleanup 清理过期文件

---

## 🆘 联系 Baby

遇到任何问题，立即联系 Baby（医生）：
- 记录失败
- 文件权限错误
- 系统报错
- 不确定的操作

**不要自己修，让 Baby 来修！**

---

*部署完成 | 晨露宝宝 🌟*
