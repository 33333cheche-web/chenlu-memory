---
name: baby-memory-suite
version: 2.4.0
description: |
  Baby Memory System - 三层记忆架构完整实现
  - L0: 每日记录 (daily/)
  - L1: 工作记忆 (MEMORY.md, active-tasks.md)
  - L2: 长期记忆 (INDEX.md, RELATIONS.md)
  - P0/P1/P2 生命周期自动管理
  - 跨 Bot 共享记忆
---

# Baby Memory Suite v2.4.0 🧠

## 三层记忆架构

### L0 - 每日记录层 (Raw)
**位置**: `memory/daily/YYYY-MM-DD.md`
**保留时间**: 30天 (P2)
**内容**: 当天对话、决策、任务、时间线
**更新**: 自动捕获 + 手动记录

### L1 - 工作记忆层 (Working)
**位置**: 
- `active-tasks.md` - 进行中任务
- `learnings.md` - 错误教训
- `memory/entities/*.md` - 实体知识
**保留时间**: 90天 (P1)
**内容**: 近期项目、待办事项、经验教训
**更新**: 重要变更时立即更新

### L2 - 长期记忆层 (Long-term)
**位置**:
- `MEMORY.md` - 核心身份、偏好
- `INDEX.md` - 记忆索引
- `RELATIONS.md` - 关联图谱
**保留时间**: 永久 (P0)
**内容**: 人设、系统规则、重要关系
**更新**: 关键变更时更新

## 生命周期管理 (P0/P1/P2)

| 标签 | 类型 | 保留时间 | 例子 |
|------|------|---------|------|
| **P0** | 核心信息 | 永久 | 名字、写作风格、系统配置 |
| **P1** | 活跃项目 | 90天 | 当前文章、调试功能 |
| **P2** | 临时信息 | 30天 | 某次对话细节 |

**自动清理**: `cleanup.js` 每周日 23:00 执行

## 会话流程

### 启动时读取（按顺序）
1. **SOUL.md** - 我是谁
2. **MEMORY.md** - 长期记忆 (P0)
3. **INDEX.md** - 索引 (L2)
4. **memory/daily/今天.md** - 今日记录 (L0)
5. **shared-memory/cross-agent-log.md** - 跨 Bot 协作

### 对话中记录（重要时刻）
- **重要决策** → 立即记录
- **完成工作** → 立即记录
- **新发现** → 立即记录

### 结束时保存
1. 生成今日总结
2. 保存到 daily log
3. 更新 cross-agent-log（重要结论）

## 使用方式

### 自动捕获
```bash
# 重要决策
~/.openclaw/workspace-{bot}/auto-capture.sh {bot} "决策: 选择XX方案，因为..."

# 完成工作
~/.openclaw/workspace-{bot}/auto-capture.sh {bot} "完成: XX任务，结果是..."

# 新发现
~/.openclaw/workspace-{bot}/auto-capture.sh {bot} "发现: XX知识点"

# 会话结束
~/.openclaw/workspace-{bot}/auto-capture.sh {bot} "今日总结: 完成了..."
```

### 跨 Bot 协作记录
```bash
# 帮其他 Bot 时
~/.openclaw/workspace-{bot}/auto-capture.sh {bot} "[执行者/角色] 帮 受益者: 具体做了什么，结果如何"

# 示例
~/.openclaw/workspace-baby/auto-capture.sh baby "[Baby/医生] 帮 Sunny: 修复 capture.js 路径问题，从 memory/ 改到 memory/daily/，现在记录正常"
```

## 文件结构

```
workspace-{bot}/
├── SOUL.md                    # 人设 (P0)
├── MEMORY.md                  # 长期记忆 (P0)
├── INDEX.md                   # 索引 (L2)
├── RELATIONS.md               # 关联图谱 (L2)
├── AGENTS.md                  # 代理配置
├── TOOLS.md                   # 工具配置
└── memory/
    ├── .abstract              # L0 快速索引
    ├── active-tasks.md        # P1 活跃任务
    ├── learnings.md           # P1 错误教训
    ├── daily/                 # P2 每日记录
    │   └── YYYY-MM-DD.md
    └── archive/               # 自动归档

shared-memory/                 # 跨 Bot 共享
├── .abstract
├── cross-agent-log.md         # 协作记录
├── active-tasks.md            # 当前任务
└── entities/                  # 共享实体
    ├── apis.md
    └── tools.md
```

## 安装

```bash
# 初始化记忆系统
node scripts/init.js --bot={bot_name}

# 配置定时清理
# 添加到 crontab: 0 23 * * 0 {path}/scripts/cleanup.sh {bot_name}
```

## 配置

编辑 `config/lifecycle.json`:
```json
{
  "P0": { "retention": "forever" },
  "P1": { "retention_days": 90 },
  "P2": { "retention_days": 30 }
}
```

## 注意事项

1. **启动只加载索引** - 不要全量加载，Token 会爆
2. **按需读取详细内容** - 需要时再读 L1/L2
3. **及时记录** - 重要信息立即存档，不要依赖"我记得"
4. **定期清理** - 让系统自动归档过期记忆
5. **共享协作** - 重要结论写到 cross-agent-log

## 版本历史

- **v2.4.0** (2026-04-03): 重构三层架构，优化记录格式，添加跨 Bot 协作
- **v2.3.1** (2026-04-02): 初始版本，基础捕获 + 清理功能
