# OpenClaw 配置 Kimi Coding 模型指南

> 适用于需要在 OpenClaw 中配置 Kimi Coding（Kimi K2.5）模型的同事

---

## 一、配置概览

在 `openclaw.json` 的 `models.providers` 中添加 Kimi Coding 配置：

```json
{
  "models": {
    "providers": {
      "kimi-coding": {
        "baseUrl": "https://api.kimi.com/coding/v1",
        "apiKey": "sk-kimi-xxxxxxxxxxxxxxxx",
        "api": "anthropic-messages",
        "models": [
          {
            "id": "kimi-for-coding",
            "name": "Kimi K2.5",
            "reasoning": true,
            "input": ["text"],
            "contextWindow": 200000,
            "maxTokens": 16000,
            "cost": {
              "input": 0,
              "output": 0,
              "cacheRead": 0,
              "cacheWrite": 0
            }
          }
        ]
      }
    }
  },
  "agents": {
    "defaults": {
      "model": {
        "primary": "kimi-coding/kimi-for-coding",
        "fallbacks": ["其他备用模型"]
      }
    }
  }
}
```

---

## 二、关键配置项说明

### 1. baseUrl（必填）

```json
"baseUrl": "https://api.kimi.com/coding/v1"
```

**注意**：
- 必须是 `/coding/v1` 结尾
- 不要写成 `api.moonshot.cn`（那是普通 Kimi API）

### 2. apiKey（必填）

```json
"apiKey": "sk-kimi-xxxxxxxxxxxxxxxx"
```

**格式要求**：
- ✅ 正确：`sk-kimi-...` 开头
- ❌ 错误：`19cdac6d...` 格式（这是普通 Kimi Key）

**获取方式**：
- 在 Kimi 开放平台申请 **Coding 专用 API Key**
- 与普通 Kimi API Key 不通用

### 3. api（必填）

```json
"api": "anthropic-messages"
```

**这是最容易出错的地方！**

| 配置值 | 适用场景 |
|--------|----------|
| `"anthropic-messages"` | ✅ Kimi Coding **必须用这个** |
| `"openai-completions"` | ❌ 普通 OpenAI 兼容 API |
| `"google-generative-ai"` | ❌ Gemini 模型 |

### 4. 模型 ID

```json
"id": "kimi-for-coding"
```

- 使用 `kimi-for-coding` 作为模型标识
- 不是 `kimi-k2.5` 或其他名称

---

## 三、常见报错及解决方案

### 报错 1："非标准 API 格式"

**原因**：`api` 字段配置错误

**解决**：
```json
// 错误 ❌
"api": "openai-completions"

// 正确 ✅
"api": "anthropic-messages"
```

### 报错 2：API Key 无效

**原因**：使用了普通 Kimi Key

**解决**：
- 重新申请 **Kimi Coding 专用 Key**（`sk-kimi-` 开头）
- 不要与普通 Kimi Key 混淆

### 报错 3：模型不可用

**原因**：模型 ID 写错

**解决**：
```json
// 错误 ❌
"id": "kimi-k2.5"

// 正确 ✅
"id": "kimi-for-coding"
```

---

## 四、完整配置示例

```json
{
  "meta": {
    "lastTouchedVersion": "2026.3.13"
  },
  "models": {
    "providers": {
      "kimi-coding": {
        "baseUrl": "https://api.kimi.com/coding/v1",
        "apiKey": "sk-kimi-xxxxxxxxxxxxxxxx",
        "api": "anthropic-messages",
        "models": [
          {
            "id": "kimi-for-coding",
            "name": "Kimi K2.5",
            "reasoning": true,
            "input": ["text"],
            "contextWindow": 200000,
            "maxTokens": 16000,
            "cost": {
              "input": 0,
              "output": 0,
              "cacheRead": 0,
              "cacheWrite": 0
            }
          }
        ]
      }
    }
  },
  "agents": {
    "defaults": {
      "model": {
        "primary": "kimi-coding/kimi-for-coding",
        "fallbacks": []
      }
    },
    "list": [
      {
        "id": "main",
        "name": "YourBot",
        "workspace": "/path/to/workspace",
        "model": "kimi-coding/kimi-for-coding"
      }
    ]
  },
  "gateway": {
    "port": 18794,
    "mode": "local"
  }
}
```

---

## 五、配置检查清单

修改配置后，按以下顺序检查：

- [ ] `baseUrl` 是 `https://api.kimi.com/coding/v1`
- [ ] `apiKey` 是 `sk-kimi-` 开头
- [ ] `api` 是 `anthropic-messages`
- [ ] `models[0].id` 是 `kimi-for-coding`
- [ ] `agents.defaults.model.primary` 是 `kimi-coding/kimi-for-coding`

---

## 六、重启生效

修改配置后需要重启 Gateway：

```bash
# 如果使用 systemd
systemctl --user restart openclaw-gateway-xxxx

# 或者直接重启
openclaw gateway restart
```

---

## 七、验证配置

重启后验证模型是否加载成功：

```bash
openclaw models list
```

应该能看到 `kimi-coding/kimi-for-coding` 在列表中。

---

**最后更新**：2026-04-02

如有其他问题，可以参考 OpenClaw 官方文档或询问团队内已配置成功的同事。
