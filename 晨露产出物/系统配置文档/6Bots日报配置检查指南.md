# 6 Bots 日报配置规范与检查指南

> 日期：2026-03-29
> 更新：2026-03-30 - 添加附录A：各 Bot 模型配置速查
> 目的：统一所有 Bot 日报配置，明确检查标准

---

## 一、日报配置标准

### 1.1 正确配置结构

一个完整的日报配置应包含：

```
1. 脚本文件      - /workspace/scripts/daily-report.sh
2. Cron 任务     - 在 crontab 中配置
3. 环境变量      - OPENCLAW_HOME 必须设置
4. 目标用户      - 统一使用公主的 OpenID
5. 日志记录      - 输出到 /tmp 或 workspace
```

### 1.2 时间分配（避免冲突）

| 时间 | Bot | 说明 |
|------|-----|------|
| 22:00 | 晨露 (Chenlu) | 第一个发送 |
| 22:02 | Melody | 避免并发 |
| 22:04 | Baby | 避免并发 |
| 22:06 | Rainbow | 避免并发 |
| 22:08 | Sunny/Bot2 | 已有配置 |
| 22:10 | Mumu | 最后发送 |

**间隔至少 2 分钟**，避免 gateway 过载

### 1.3 目标用户规范

**重要说明**：不同飞书应用看到的用户 OpenID 可能不同！

| Bot | 公主的 OpenID | 说明 |
|-----|--------------|------|
| 晨露 (Main) | `ou_8817a15f54b382776f186f9ace070d86` | 主应用 |
| Sunny (Bot2) | `ou_e40c5df02fc12d4786a84a078a9b180d` | 另一个应用 |
| Rainbow | `ou_bf3db991aeebfd871fed45e9925a2110` | 另一个应用 |

**⚠️ 每个 bot 应该使用自己的配置中记录的目标用户 ID，不要跨应用复制！**

**如何确认自己的 ID**：
```bash
# 查看当前对话中用户的 ID
grep "sender_id" /tmp/openclaw/latest_message.json
# 或查看已有脚本中的配置
grep -r "user:ou_" /home/cheche/.openclaw/workspace-[bot]/scripts/
```

### 1.4 环境变量规范

Cron 任务必须包含：
```bash
export OPENCLAW_HOME="/home/cheche/.openclaw-[bot名字]"
export PATH="/home/cheche/.npm-global/bin:$PATH"
```

---

## 二、6 Bots 当前状态检查表

### 2.1 检查清单

| Bot | 脚本存在 | Cron配置 | 环境变量 | 目标用户正确 | 可发送 |
|-----|---------|----------|----------|-------------|--------|
| **CHENLU** | ✅ | ✅ (22:00) | ✅ | ✅ | ✅ |
| **SUNNY/Bot2** | ✅ | ✅ (22:08) | ❓ | ❓ 需确认ID | ❓ |
| **RAINBOW** | ✅ | ❌ 未激活 | - | ❓ | ❌ |
| **MUMU** | ✅ | ✅ (22:08) | ❌ 需修复 | ✅ | ❌ 只能生成不能发 |
| **MELODY** | ❌ | ❌ | - | - | ❌ |
| **BABY** | ❌ | ❌ | - | - | ❌ |

### 2.2 各 Bot 详细情况

#### CHENLU (晨露) ✅ 正常
- **脚本**: `/scripts/auto_daily_report_fixed.sh`
- **Cron**: `0 22 * * *`
- **状态**: 已修复，正常

#### SUNNY/Bot2 ⚠️ 需确认用户ID
- **脚本**: `/workspace/bot2-import/scripts/daily-report.sh`
- **Cron**: `8 22 * * *`
- **目标用户**: `ou_e40c5df02fc12d4786a84a078a9b180d`
- **问题**: 目标用户ID与公主ID不一致，需确认

#### RAINBOW ❌ 未激活
- **脚本**: `/workspace-rainbow/scripts/rainbow_daily_report.sh`
- **Cron**: 无
- **问题**: 脚本存在但 cron 未配置，不会自动执行

#### MUMU (沐木) ❌ 发送功能缺失
- **脚本**: 
  - `generate-daily-report.sh` - 生成文件
  - `send-daily-report.sh` - 只创建标记，不发送
- **Cron**: `8 22 * * *`
- **问题**: 没有真正的发送功能

#### MELODY ❌ 完全缺失
- **脚本**: 无
- **Cron**: 无
- **问题**: 没有日报功能

#### BABY ❌ 完全缺失
- **脚本**: 无
- **Cron**: 无
- **问题**: 没有日报功能

---

## 三、排查步骤

### 3.1 检查 Cron 配置

```bash
# 查看所有日报相关任务
crontab -l | grep -E "(22:|日报|daily|report)"

# 检查输出
# - 确认时间正确
# - 确认有 OPENCLAW_HOME
# - 确认脚本路径正确
```

### 3.2 检查脚本文件

```bash
# 检查脚本是否存在且可执行
ls -la [workspace]/scripts/*daily*.sh
ls -la [workspace]/scripts/*report*.sh

# 查看脚本内容
cat [workspace]/scripts/daily-report.sh

# 确认包含：
# 1. OPENCLAW_HOME 设置
# 2. 目标用户 ID
# 3. openclaw message send 命令
```

### 3.3 检查目标用户

**⚠️ 重要：每个 Bot 使用自己的 ID！**

```bash
# 方法1：查看当前对话中的用户ID
grep "sender_id" ~/.openclaw/[bot]/.openclaw/sessions/latest.json 2>/dev/null

# 方法2：查看已有脚本中的配置
grep -rn "user:ou_\|--target\|--to" [workspace]/scripts/

# 方法3：查看飞书 channel 配置
grep -A 5 "feishu" [workspace]/.openclaw/openclaw.json | grep "allowFrom"
```

**注意**：不同应用看到的 OpenID 不同，不要直接复制其他 bot 的 ID！

**验证方法**：
```bash
# 手动测试发送
export OPENCLAW_HOME=/home/cheche/.openclaw-[bot]
/home/cheche/.npm-global/bin/openclaw message send \
    --target "user:[查到的ID]" \
    --message "测试日报"
```

### 3.4 手动测试

```bash
# 手动运行脚本测试
export OPENCLAW_HOME=/home/cheche/.openclaw-[bot]
/home/cheche/.npm-global/bin/openclaw message send \
    --target user:ou_8817a15f54b382776f186f9ace070d86 \
    --message "测试日报"
```

### 3.5 检查日志

```bash
# 查看日报执行日志
cat /tmp/[bot]_daily_report.log
cat /tmp/chenlu_daily_report.log

# 查看 cron 系统日志
grep CRON /var/log/syslog | tail -20
```

---

## 四、修复方案

### 4.1 立即修复（高优先级）

1. **Mumu** - 添加真正的发送功能
2. **Rainbow** - 在 cron 中激活日报
3. **确认 Sunny 目标用户** - 验证用户ID是否正确

### 4.2 后续补充（中优先级）

1. **Melody** - 创建日报脚本
2. **Baby** - 创建日报脚本

### 4.3 统一优化（低优先级）

1. 统一时间间隔（22:00, 22:02, 22:04...）
2. 统一日报格式
3. 统一日志路径

---

## 五、日报脚本模板

```bash
#!/bin/bash
# [BotName] 日报脚本
# 执行时间：[具体时间]

set -e

# 环境变量（必须）
export OPENCLAW_HOME="/home/cheche/.openclaw-[botname]"
export PATH="/home/cheche/.npm-global/bin:$PATH"

# 工作目录
WORKSPACE="/home/cheche/.openclaw/workspace-[botname]"
DATE=$(date +%Y-%m-%d)
MEMORY_FILE="$WORKSPACE/memory/$DATE.md"
LOG_FILE="/tmp/[botname]_daily_report.log"

# 日志函数
log() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] $1" >> "$LOG_FILE"
}

log "开始生成日报: $DATE"

# 生成日报内容
REPORT="# [BotName] 日报 - $DATE

## 📊 今日工作
[从 memory 文件提取或手动填写]

## ❌ 今日失误
[如有]

## 💭 碎碎念
[bot 个性签名]

---
*[BotName] 汇报*"

# 发送日报（关键！）
# ⚠️ 使用自己 bot 配置中对应的目标用户 ID！
TARGET_USER="user:[从配置中查到的OpenID]"

$OPENCLAW_HOME/../.npm-global/bin/openclaw message send \
    --channel feishu \
    --target "$TARGET_USER" \
    --message "$REPORT" \
    2>> "$LOG_FILE"

log "日报发送完成"
```

---

## 六、Cron 条目模板

```bash
# [BotName] 日报 - 每晚[具体时间]
[分钟] [小时] * * * export OPENCLAW_HOME=/home/cheche/.openclaw-[botname] && export PATH=/home/cheche/.npm-global/bin:$PATH && /home/cheche/.openclaw/workspace-[botname]/scripts/daily-report.sh >> /tmp/[botname]_daily_report.log 2>&1
```

---

## 七、验证检查表

在确认配置正确后，逐项勾选：

- [ ] 脚本文件存在且可执行 (`chmod +x`)
- [ ] Cron 任务已添加
- [ ] OPENCLAW_HOME 设置正确
- [ ] **目标用户 ID 是【本 bot】配置中记录的 ID**（不要复制其他 bot）
- [ ] 手动测试发送成功（公主能收到）
- [ ] 日志文件有记录
- [ ] 时间与其他 bot 不冲突
- [ ] 第二天自动收到日报

**⚠️ 注意**：每个 bot 看到的目标用户 OpenID 可能不同，务必使用自己配置中的 ID！

---

## 八、常见问题

### Q1: Cron 不执行
**排查**:
- 检查 `crontab -l` 是否包含任务
- 检查脚本权限 `chmod +x script.sh`
- 检查日志 `/var/log/syslog | grep CRON`

### Q2: 发送失败
**排查**:
- 检查 OPENCLAW_HOME 是否设置
- 检查目标用户 ID 是否正确
- 手动运行脚本查看错误

### Q3: 收到重复日报
**排查**:
- 检查是否有多个 cron 任务
- 检查时间是否冲突

### Q4: 日报内容为空
**排查**:
- 检查 memory 文件是否存在
- 检查脚本是否正确读取文件

---

**更新日期**: 2026-03-29
**下次检查**: 建议 3 天后验证所有日报正常发送

---

## 附录A：各 Bot 模型配置速查（2026-03-30更新）

### 模型切换命令

```bash
/model [provider]/[model]
```

### 6 Bots 模型配置

| Bot | 主模型 | 备用模型 | 可选模型 |
|-----|--------|----------|----------|
| **晨露 (Chenlu)** | `kimi-coding/kimi-for-coding` | `fox-gemini/gemini-3.1-pro` | - |
| **Sunny** | `fox-gemini/gemini-3.1-pro` | `kimi-coding/kimi-for-coding` | - |
| **Rainbow** | `fox-gemini/gemini-3.1-pro` | `kimi-coding/kimi-for-coding` | - |
| **Mumu** | `kimi-coding/kimi-for-coding` | `moonshot/kimi-k2.5` | - |
| **Melody** | `kimi-coding/kimi-for-coding` | `moonshot/kimi-k2.5` | - |
| **Baby** | `fox-gemini/gemini-3.1-pro` | `kimi-coding/kimi-for-coding` | `openai/gpt-5.4` ✅ |

### 常用切换命令

```bash
# 切换到 Kimi
/model kimi-coding/kimi-for-coding

# 切换到 Gemini
/model fox-gemini/gemini-3.1-pro

# 切换到 Moonshot
/model moonshot/kimi-k2.5

# Baby 专属：切换到 GPT-5.4
/model openai/gpt-5.4
```

### 故障排查

**症状**: Bot 回复报错 500
**原因**: 主模型失效
**解决**: 
1. 临时切换：`/model kimi-coding/kimi-for-coding`
2. 或切到备用模型

**症状**: Unknown provider
**原因**: Provider 名称错误
**解决**: 使用上表中的正确 provider/model 名称
