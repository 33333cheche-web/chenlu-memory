# OpenClaw Agent 配置整理方案

> 当前状态检查及优化建议
> 创建时间：2026-03-21
> 创建者：晨露

---

## 一、当前配置状态

### 1.1 现有的 Workspace
```
~/.openclaw/
├── workspace                  # 默认（基本不用）
├── workspace-chenlu          # 晨露 ✅ 在用
├── workspace-rainbow         # Rainbow ✅ 在用
├── workspace-sunny           # Sunny ✅ 在用
└── workspace-backup-*.tar.gz # 备份文件
```

### 1.2 当前的 openclaw.json 配置

**Agents 配置片段：**
```json
"agents": {
  "defaults": {
    "workspace": "/home/cheche/.openclaw/workspace-sunny"  // ❌ 指向 Sunny
  },
  "list": [
    {
      "id": "main",
      "name": "Sunny",
      "workspace": "/home/cheche/.openclaw/workspace-sunny"
      // ❌ 晨露和 Rainbow 不在 list 中
    }
  ]
}
```

### 1.3 存在的问题

| 问题 | 说明 | 风险 |
|------|------|------|
| 默认值指向 Sunny | defaults.workspace = workspace-sunny | 新实例可能误入 Sunny 的配置 |
| 晨露/Rainbow 未注册 | 只在 agents.list 中有 Sunny | 靠运行时环境变量确定，不稳定 |
| 配置不明确 | 谁用哪个 workspace 不清晰 | 容易混乱，难以维护 |

---

## 二、整理方案（推荐）

### 2.1 目标
- ✅ 每个 AI 都有明确的独立配置
- ✅ 谁用哪个 workspace 一目了然
- ✅ 不再依赖"运行时环境变量"
- ✅ 配置稳定，不易出错

### 2.2 修改内容

**修改 openclaw.json 的 agents 部分：**

```json
"agents": {
  "defaults": {
    "model": {
      "primary": "kimi-code/kimi-for-coding",
      "fallbacks": [
        "custom-code-newcli-com/claude-sonnet-4-6",
        "moonshot/kimi-k2-5"
      ]
    },
    "imageModel": "custom-code-newcli-com/claude-sonnet-4-6",
    "workspace": "/home/cheche/.openclaw/workspace-chenlu",  // 默认给晨露
    "compaction": {
      "mode": "safeguard"
    },
    "heartbeat": {
      "every": "2h"
    },
    "maxConcurrent": 4
  },
  "list": [
    {
      "id": "sunny",
      "name": "Sunny",
      "workspace": "/home/cheche/.openclaw/workspace-sunny",
      "agentDir": "/home/cheche/.openclaw/workspace-sunny/.openclaw/agents/main",
      "model": {
        "primary": "kimi-coding/k2p5",
        "fallbacks": [
          "custom-code-newcli-com/claude-sonnet-4-6",
          "moonshot/kimi-k2-5"
        ]
      }
    },
    {
      "id": "chenlu",
      "name": "晨露",
      "workspace": "/home/cheche/.openclaw/workspace-chenlu",
      "agentDir": "/home/cheche/.openclaw/workspace-chenlu/.openclaw/agents/main",
      "model": {
        "primary": "kimi-coding/k2p5",
        "fallbacks": [
          "custom-code-newcli-com/claude-sonnet-4-6",
          "moonshot/kimi-k2-5"
        ]
      }
    },
    {
      "id": "rainbow",
      "name": "Rainbow",
      "workspace": "/home/cheche/.openclaw/workspace-rainbow",
      "agentDir": "/home/cheche/.openclaw/workspace-rainbow/.openclaw/agents/main",
      "model": {
        "primary": "kimi-coding/k2p5",
        "fallbacks": [
          "custom-code-newcli-com/claude-sonnet-4-6",
          "moonshot/kimi-k2-5"
        ]
      }
    }
  ]
}
```

### 2.3 修改后的效果

| AI | Workspace | 配置来源 | 状态 |
|----|-----------|----------|------|
| **Sunny** | workspace-sunny | agents.list 明确配置 | ✅ 独立稳定 |
| **晨露** | workspace-chenlu | agents.list 明确配置 | ✅ 独立稳定 |
| **Rainbow** | workspace-rainbow | agents.list 明确配置 | ✅ 独立稳定 |
| **默认** | workspace-chenlu | agents.defaults | ✅ 给晨露 |

---

## 三、操作步骤（如需执行）

### 3.1 备份（重要！）
```bash
# 备份当前配置
cp ~/.openclaw/openclaw.json ~/.openclaw/openclaw.json.backup-$(date +%Y%m%d-%H%M%S)
```

### 3.2 修改配置文件
```bash
# 编辑 openclaw.json
nano ~/.openclaw/openclaw.json

# 找到 "agents" 部分，替换为上面的方案
```

### 3.3 重启 Gateway
```bash
openclaw gateway restart
```

### 3.4 验证
```bash
# 检查配置是否正确
openclaw status

# 检查各个 workspace 是否正常工作
```

---

## 四、风险提示

### 4.1 修改前注意
- ✅ 已备份原配置
- ✅ 已保存此方案文档
- ⚠️ 需要在低峰期操作（避免影响正在进行的对话）
- ⚠️ 修改后需要重启 Gateway

### 4.2 可能的问题
- 如果配置格式错误，Gateway 可能无法启动
- 如果 workspace 路径错误，AI 可能无法找到配置
- 重启期间可能会有短暂的服务中断

### 4.3 回滚方案
如果出问题，可以快速回滚：
```bash
# 恢复原配置
cp ~/.openclaw/openclaw.json.backup-xxx ~/.openclaw/openclaw.json
openclaw gateway restart
```

---

## 五、当前状态（未修改前）

- **晨露**：正常工作 ✅
- **Rainbow**：正常工作 ✅
- **Sunny**：正常工作 ✅
- **配置状态**：可用但不够清晰

**建议**：可以先保持现状，等合适时机再修改。

---

## 六、附录：完整的 openclaw.json agents 部分

（如需完整配置，请参考上面的 2.2 节）

---

**文档维护**：晨露
**最后更新**：2026-03-21

**公主决定后再执行！** 🎀
