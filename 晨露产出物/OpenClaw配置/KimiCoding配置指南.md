# Kimi Coding 在 OpenClaw 中的配置指南

> 适用版本：OpenClaw 2026.4.x 及更高版本

---

## 一、配置文件位置

### 推荐方式：Agent 级别配置（仅影响当前 agent）

```
~/.openclaw/agents/main/agent/models.json
```

### 备选方式：全局配置（影响所有 agent）

```
~/.openclaw/config.json
```

> ⚠️ **优先级**：Agent 级别配置 > 全局配置。如果两者同时存在，Agent 配置会覆盖全局配置。

---

## 二、配置内容

在 `models.json` 中添加以下 provider：

```json
{
  "providers": {
    "kimi-coding": {
      "baseUrl": "https://api.kimi.com/coding/v1",
      "apiKey": "你的_API_Key_这里",
      "api": "anthropic-messages",
      "models": [
        {
          "id": "kimi-for-coding",
          "name": "Kimi for Coding",
          "reasoning": false,
          "input": ["text"],
          "cost": {
            "input": 0,
            "output": 0,
            "cacheRead": 0,
            "cacheWrite": 0
          },
          "contextWindow": 200000,
          "maxTokens": 8192,
          "api": "anthropic-messages"
        }
      ]
    }
  }
}
```

---

## 三、关键参数说明

| 参数 | 说明 | 值 |
|------|------|-----|
| `baseUrl` | Kimi API 地址 | `https://api.kimi.com/coding/v1` |
| `api` | 协议格式 | `anthropic-messages`（Kimi Coding 用 Anthropic 兼容格式） |
| `apiKey` | 鉴权密钥 | 从 Kimi 开放平台获取 |
| `id` | 模型标识 | `kimi-for-coding`（当前固定值） |
| `contextWindow` | 上下文长度 | 200000（200K tokens） |
| `maxTokens` | 最大输出 token | 8192 |

---

## 四、获取 API Key

1. 访问 [Kimi 开放平台](https://platform.moonshot.cn/)
2. 注册/登录账号
3. 进入「API Key 管理」
4. 创建新 Key，格式：`sk-kimi-xxxxxxxx...`

---

## 五、验证配置

配置完成后，运行以下命令检查状态：

```bash
openclaw status
```

期望看到类似输出：

```
Sessions: 1 active · default kimi-for-coding (200k ctx)
```

---

## 六、常见问题

### Q1: 配置后不生效？

- 检查文件路径是否正确：`~/.openclaw/agents/main/agent/models.json`
- 检查 JSON 格式是否合法（可用 `jsonlint` 验证）
- 重启 OpenClaw：`openclaw gateway restart`

### Q2: 与其他模型冲突？

- 确保 `providers` 下的 key 唯一（如 `kimi-coding`）
- 如果全局和 agent 都有配置，以 agent 级别为准

### Q3: API 调用报错？

- 确认 API Key 有效且有额度
- 确认网络可以访问 `api.kimi.com`
- 查看日志：`openclaw logs --follow`

---

## 七、参考配置示例（完整版）

包含多个 provider 的完整 `models.json`：

```json
{
  "providers": {
    "kimi-coding": {
      "baseUrl": "https://api.kimi.com/coding/v1",
      "apiKey": "sk-kimi-你的Key",
      "api": "anthropic-messages",
      "models": [
        {
          "id": "kimi-for-coding",
          "name": "Kimi for Coding",
          "reasoning": false,
          "input": ["text"],
          "cost": {
            "input": 0,
            "output": 0,
            "cacheRead": 0,
            "cacheWrite": 0
          },
          "contextWindow": 200000,
          "maxTokens": 8192,
          "api": "anthropic-messages"
        }
      ]
    },
    "moonshot": {
      "baseUrl": "https://api.moonshot.cn/v1",
      "apiKey": "sk-另一个Key",
      "api": "openai-completions",
      "models": [
        {
          "id": "kimi-k2.5",
          "name": "Kimi K2.5",
          "contextWindow": 256000
        }
      ]
    }
  }
}
```

---

## 八、版本说明

- **Kimi for Coding**: 当前模型 ID 固定为 `kimi-for-coding`
- **contextWindow**: 200K 上下文
- **适用场景**: 代码生成、代码审查、技术方案设计

---

> 本文档由 OpenClaw 配置导出，仅供参考。实际配置请以官方最新文档为准。
