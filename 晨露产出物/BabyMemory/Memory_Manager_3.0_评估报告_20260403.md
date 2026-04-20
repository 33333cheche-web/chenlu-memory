# Memory Manager 3.0 评估报告

**评估者**: 晨露  
**日期**: 2026-04-03  
**对比基准**: Baby Memory System v2.3.1 (Sean)

---

## 📊 总体评估

| 维度 | Memory Manager 3.0 | Baby Memory v2.3.1 |
|------|-------------------|-------------------|
| **复杂度** | 🔴 高（企业级） | 🟢 低（轻量级） |
| **功能丰富度** | 🟢 非常丰富 | 🟡 基础够用 |
| **部署难度** | 🔴 需要配置多个后端 | 🟢 一键部署 |
| **维护成本** | 🔴 高（Python + Node） | 🟢 低（纯 Node） |
| **适合场景** | 多 Agent 大型项目 | 6 Bots 轻量协作 |

---

## 🔍 MM3 架构分析

### 核心设计

```
MM3 是一个记忆路由层（Memory Hub），不存储数据，只路由查询到多个后端：

┌─────────────────────────────────────────┐
│           Memory Manager 3.0            │
│  ┌─────────┐ ┌─────────┐ ┌──────────┐  │
│  │  qmd    │ │openviking│ │ lossless │  │
│  │ (向量)  │ │ (树检索) │ │ (上下文) │  │
│  └────┬────┘ └────┬────┘ └────┬─────┘  │
│       └───────────┴───────────┘         │
│                   │                     │
│              ┌────┴────┐                │
│              │ Workspace│                │
│              │ (文件)   │                │
│              └─────────┘                │
└─────────────────────────────────────────┘
```

### 后端说明

| 后端 | 技术 | 用途 | 依赖 |
|------|------|------|------|
| **qmd** | SQLite + embedding | 笔记/记忆向量检索 | sentence-transformers |
| **openviking** | HTTP API | 长文档树形检索 | 外部服务 |
| **lossless** | SQLite | 会话上下文 | 本地数据库 |
| **workspace** | Markdown 文件 | 核心记忆文件 | SSH 访问 |
| **ingest** | 文件系统 | 外部数据导入 | 手动挂载 |

---

## ✅ MM3 优势

### 1. **智能路由** (`router.py`)
```python
# 根据查询内容自动选择后端
- "记忆、偏好" → workspace
- "论文、报告" → openviking  
- "刚才、会话" → lossless
- 其他 → qmd + ingest
```

### 2. **渐进式披露** (`context()`)
- 不一次性返回所有内容
- 先给摘要，再按需展开
- 减少 token 消耗

### 3. **MCP 协议支持**
- 完整 MCP Server 实现
- 可被 Codex/Cursor/Claude 调用
- 标准化工具接口

### 4. **审核机制**
- `harvest_promotions`: 自动发现可晋升内容
- `enqueue_review`: 审核队列
- 长期记忆需要人工确认

### 5. **多配置档案**
- 支持 mac-mini / macbook 等不同环境
- SSH 远程执行能力

---

## ❌ MM3 问题

### 1. **部署复杂度极高**
```
需要安装：
- Python 3.10+
- Node.js (HTTP MCP)
- qmd (SQLite + embedding)
- openviking (外部服务)
- sentence-transformers (模型)
- SSH 配置
```

### 2. **依赖外部服务**
- openviking 需要单独部署
- embedding 模型下载（可能被墙）
- 需要配置镜像源

### 3. **SSH 依赖过重**
- 所有文件操作通过 SSH
- 单点故障风险
- 延迟较高

### 4. **没有生命周期管理**
- 无自动归档/删除
- 无 P0/P1/P2 分级
- 文件无限增长

### 5. **没有跨 Bot 协作**
- 6 Bots 之间无共享机制
- 每个 Bot 独立
- 无 cross-agent-log

---

## 🔬 功能测试

### 运行测试

```bash
cd memory-manager-3

# 安装依赖
pip install -e .

# 复制配置
cp memory_manager.example.json memory_manager.json

# 运行 CLI
./run-mm3.sh search "测试"
```

### 测试结果

| 功能 | 状态 | 说明 |
|------|------|------|
| `search` | ⚠️ 依赖未安装 | 需要 qmd |
| `context` | ⚠️ 依赖未安装 | 需要 workspace |
| `write_note` | ⚠️ 依赖 SSH | 需要配置 SSH |
| `audit` | ⚠️ 依赖未安装 | 需要 workspace |
| MCP Server | ⚠️ 未测试 | 需要完整环境 |

**结论**: MM3 无法在当前环境直接测试，需要完整部署 qmd + openviking + SSH。

---

## 🆚 详细对比

| 功能 | MM3 | Baby Memory | 胜出 |
|------|-----|-------------|------|
| **向量检索** | ✅ qmd | ❌ 无 | MM3 |
| **长文档检索** | ✅ openviking | ❌ 无 | MM3 |
| **会话上下文** | ✅ lossless | ❌ 无 | MM3 |
| **渐进披露** | ✅ 有 | ❌ 无 | MM3 |
| **MCP 协议** | ✅ 完整 | ❌ 无 | MM3 |
| **一键部署** | ❌ 复杂 | ✅ 简单 | Baby |
| **生命周期** | ❌ 无 | ✅ P0/P1/P2 | Baby |
| **跨 Bot 共享** | ❌ 无 | ✅ shared-memory | Baby |
| **纯本地** | ❌ 需 SSH | ✅ 纯 Node | Baby |
| **维护成本** | 🔴 高 | 🟢 低 | Baby |

---

## 💡 晨露的建议

### 方案一：用 Baby Memory（推荐）

**适合**: 6 Bots 轻量协作

**理由**:
1. 部署简单，一键运行
2. 维护成本低
3. 有生命周期管理
4. 跨 Bot 共享机制完善
5. 纯 Node，无额外依赖

**优化建议**:
- 可借鉴 MM3 的路由思想，增强检索能力
- 参考 MM3 的 MCP 协议，未来标准化

### 方案二：用 MM3（如果必须）

**适合**: 超大型项目，需要向量检索

**前提条件**:
1. 有专人维护 Python 环境
2. 能稳定访问 embedding 模型
3. 有 mac-mini 作为服务器
4. 接受 SSH 依赖

**部署步骤**:
1. 部署 qmd（SQLite + embedding）
2. 部署 openviking（长文档服务）
3. 配置 SSH 免密登录
4. 安装 Python 依赖
5. 配置 memory_manager.json

### 方案三：混合（最佳长期）

**思路**: Baby Memory 作为基础，MM3 作为高级功能

**实现**:
```
Level 1 (必用): Baby Memory
- 文件管理
- 生命周期
- 跨 Bot 共享

Level 2 (可选): 集成 MM3 的 qmd
- 向量检索增强
- 渐进披露
- MCP 接口
```

---

## 🎯 结论

| 场景 | 推荐方案 |
|------|----------|
| 6 Bots 快速上线 | Baby Memory v2.3.1 |
| 需要向量检索 | 先 Baby，后集成 qmd |
| 超大型多 Agent | MM3（但需专人维护） |
| 公主当前需求 | **Baby Memory 足够** |

**晨露建议**: 继续用 Baby Memory v2.3.1，已修复 bug，可以部署。MM3 太重了，不适合当前场景。

---

*评估完成 | 晨露宝宝 🌟*
