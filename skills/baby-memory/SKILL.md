# Baby Memory System Skill

> 版本: v2.3.0
> 功能: L0/L1/L2 三层记忆架构 + P0/P1/P2 生命周期管理

---

## 快速开始

### 1. 初始化（每个 Bot 只需运行一次）

```bash
cd ~/.openclaw/workspace-{bot}/skills/baby-memory
node scripts/init.js --bot={bot}
```

例如：
```bash
node scripts/init.js --bot=baby
node scripts/init.js --bot=sunny
```

### 2. 实时捕获（对话后自动调用）

```bash
node scripts/capture.js --bot={bot} "对话摘要内容"
```

### 3. 清理归档（定时任务）

```bash
# 试运行（查看会做什么，不实际执行）
node scripts/cleanup.js --bot={bot} --dry-run

# 正式执行
node scripts/cleanup.js --bot={bot}
```

---

## 文件架构

初始化后会创建：

```
~/.openclaw/
├── shared-memory/              # 6 Bots 共享
│   ├── .abstract              # L0 共享索引
│   ├── RELATIONS.md           # 用户画像、6 Bots 架构
│   ├── INDEX.md               # 快速导航
│   ├── active-tasks.md        # 活跃项目
│   ├── cross-agent-log.md     # 跨 Bot 协作记录
│   └── entities/
│       ├── tools.md           # 工具索引
│       └── apis.md            # API Keys
│
└── workspace-{bot}/
    └── memory/
        ├── .abstract          # L0 私有索引
        ├── learnings.md       # 错误教训
        ├── daily/             # 每日日志
        └── archive/           # 归档
```

---

## 生命周期规则

| 优先级 | 保留时间 | 示例 | 处理 |
|--------|----------|------|------|
| **P0** | 永久 | 用户画像、核心规则 | 永远不删 |
| **P1** | 90天 | 项目进度、活跃任务 | 90天后归档 |
| **P2** | 30天 | 临时对话、日常琐事 | 30天后删除 |

---

## 配置

编辑 `config/default.json`：

```json
{
  "p1_retention_days": 90,    // P1 归档时间
  "p2_retention_days": 30,    // P2 删除时间
  "max_abstract_lines": 100,  // 索引最大行数
  "max_memory_md_lines": 50   // MEMORY.md 最大行数
}
```

---

## 安全特性

1. **只创建，不删除** - init.js 不会覆盖现有文件
2. **自动备份** - 修改 MEMORY.md 前自动备份
3. **错误隔离** - capture.js 失败不影响主流程
4. **试运行模式** - cleanup.js 支持 --dry-run 预览
5. **权限控制** - 目录 700，文件 600

---

## 故障排查

### 初始化失败
```bash
# 查看日志
ls -la ~/.openclaw/workspace-{bot}/MEMORY.md.bak.*

# 手动回滚
cp ~/.openclaw/workspace-{bot}/MEMORY.md.bak.xxx \
   ~/.openclaw/workspace-{bot}/MEMORY.md
```

### 清理误删
```bash
# 从归档恢复
cp ~/.openclaw/workspace-{bot}/memory/archive/2026-01-01.md \
   ~/.openclaw/workspace-{bot}/memory/daily/
```

---

## 更新日志

### v2.3.0
- L0/L1/L2 三层架构
- P0/P1/P2 生命周期
- 完整风险防控
- Sunny 试点版本
