# Baby Memory 触发机制 - 可行方案

**文档版本**: 2026-04-03  
**适用对象**: 晨露 (chenlu)  
**状态**: 实际可行方案

---

## ❌ 为什么自动触发很难

### 核心问题
- **Bot 无法监听自己的对话** - OpenClaw 没有提供会话钩子
- **AGENTS.md 的指令只是"理想"** - 实际不会自动执行
- **n8n 有依赖问题** - 缺少 `Execute Command` 节点

### 之前的问题
v2.3.x 和 v2.4.0 的脚本都写好了，但**没人调用它** = 实际不生效

---

## ✅ 可行方案（按可靠性排序）

### 方案 1: 手动快捷命令（最可靠，推荐）

**原理**: 公主要求时，晨露手动执行记录

**部署**:
```bash
# 1. 创建快捷脚本
cat > ~/.openclaw/workspace-chenlu/remember.sh << 'EOF'
#!/bin/bash
# 快速记录记忆

if [ -z "$1" ]; then
    echo "❌ 用法: remember '要记录的内容'"
    exit 1
fi

~/.openclaw/workspace-chenlu/auto-capture.sh chenlu "$1"
echo "✅ 已记录"
EOF

chmod +x ~/.openclaw/workspace-chenlu/remember.sh

# 2. 添加到 bash 快捷方式（可选）
echo 'alias remember="~/.openclaw/workspace-chenlu/remember.sh"' >> ~/.bashrc
source ~/.bashrc
```

**使用场景**:
```
公主: "晨露，记录一下"
晨露执行: remember "完成了早报设计，公主确认通过"
```

**优点**: 100% 可靠，不会漏重要信息  
**缺点**: 需要公主主动说"记录一下"

---

### 方案 2: 心跳定时记录（备用）

**原理**: 每小时自动生成一条记录

**配置** - 添加到 `HEARTBEAT.md`:
```markdown
## 每小时记忆记录

每小时检查一次，如果有活动就记录：

```bash
HOUR=$(date +%H:%M)
~/.openclaw/workspace-chenlu/auto-capture.sh chenlu "活跃记录: ${HOUR} 在线"
```
```

**效果**: 每小时一条"在线"记录，不会太频繁

**优点**: 全自动，不会遗漏在线状态  
**缺点**: 不知道具体做了什么，只有时间戳

---

### 方案 3: n8n 工作流（有条件使用）

**原理**: n8n 监听飞书消息，自动调用脚本

**前提条件**:
1. 安装 n8n 社区节点：`n8n-nodes-execute-command`
2. n8n 服务一直运行

**安装命令**:
```bash
# 1. 停止 n8n
pkill n8n

# 2. 安装社区节点
n8n community-node install n8n-nodes-execute-command

# 3. 重启 n8n
n8n start
```

**工作流配置**:
```
触发器: Webhook (飞书消息)
  ↓
节点: Execute Command
  命令: ~/.openclaw/workspace-chenlu/auto-capture.sh chenlu "飞书消息摘要"
  ↓
完成
```

**优点**: 真正的全自动  
**缺点**: 
- 需要安装社区节点
- n8n 必须一直运行
- 配置复杂，容易出问题

---

### 方案 4: 飞书机器人 Webhook（进阶）

**原理**: 飞书机器人收到消息时，调用 HTTP API

**需要**:
1. 写一个 HTTP 接收服务
2. 飞书机器人配置 Webhook
3. 服务调用 auto-capture.sh

**复杂度**: 🔴 高（不推荐）

---

## 🎯 推荐组合

| 场景 | 方案 | 说明 |
|------|------|------|
| **重要工作完成** | 方案 1 (手动) | 公主说"记录一下"，立即记录 |
| **日常在线状态** | 方案 2 (心跳) | 每小时自动记录"在线" |
| **全自动记录** | 方案 3 (n8n) | 等社区节点安装好后再试 |

---

## 📋 现在立即部署

### 步骤 1: 部署方案 1（手动）

```bash
# 创建快捷脚本
cat > ~/.openclaw/workspace-chenlu/remember.sh << 'EOF'
#!/bin/bash
if [ -z "$1" ]; then
    echo "❌ 用法: remember '内容'"
    exit 1
fi
~/.openclaw/workspace-chenlu/auto-capture.sh chenlu "$1"
echo "✅ 已记录: $1"
EOF

chmod +x ~/.openclaw/workspace-chenlu/remember.sh
```

### 步骤 2: 配置方案 2（心跳）

编辑 `~/.openclaw/workspace-chenlu/HEARTBEAT.md`，添加：

```markdown
## 每小时记忆记录

```bash
HOUR=$(date +%H:%M)
~/.openclaw/workspace-chenlu/auto-capture.sh chenlu "活跃记录: ${HOUR} 在线"
```
```

### 步骤 3: 测试

```bash
# 测试手动记录
~/.openclaw/workspace-chenlu/remember.sh "测试记录功能"

# 检查结果
cat ~/.openclaw/workspace-chenlu/memory/daily/$(date +%Y-%m-%d).md
```

---

## 📝 日常使用

### 公主说"记录一下"时：

```bash
# 晨露执行
~/.openclaw/workspace-chenlu/remember.sh "完成了XX任务，结果是YY"

# 或者简写（如果配置了 alias）
remember "完成了XX任务，结果是YY"
```

### 自动记录（心跳）：

每小时自动有一条：
```
## 14:00
- 活跃记录: 14:00 在线

## 15:00
- 活跃记录: 15:00 在线
```

---

## ⚠️ 注意事项

1. **手动记录最可靠** - 重要的事一定要手动记
2. **心跳只是备用** - 证明"我当时在线"，但不知道做了什么
3. **n8n 以后再试** - 等依赖问题解决
4. **不要依赖 AGENTS.md 的自动指令** - 实际不会执行

---

## 🆘 故障排查

| 问题 | 检查 | 解决 |
|------|------|------|
| 记录失败 | `cat memory/auto-capture.log` | 看错误日志 |
| 文件不存在 | `ls -la memory/daily/` | 检查目录权限 |
| 跨 Bot 没记录 | `cat shared-memory/cross-agent-log.md` | 检查是否是重要事件 |

---

*方案整理完成 | 晨露宝宝 🌟*
