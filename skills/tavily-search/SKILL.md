---
name: tavily-search
description: |
  通用网页搜索（Tavily）。使用方法：
  `node skills/tavily-search/scripts/search.js "query" [-n 数量] [--deep]`
  
  示例：
  - `node skills/tavily-search/scripts/search.js "AI news"`
  - `node skills/tavily-search/scripts/search.js "OpenAI" -n 10 --deep`
  
  适合国外资讯、英文内容、学术研究。
homepage: https://tavily.com
metadata:
  openclaw:
    emoji: "🔍"
    requires:
      bins: ["node"]
      env: ["TAVILY_API_KEY"]
    primaryEnv: "TAVILY_API_KEY"
---

# Tavily Search

## 快速使用

```bash
# 基本搜索
node skills/tavily-search/scripts/search.js "python async patterns"

# 更多结果
node skills/tavily-search/scripts/search.js "React hooks" -n 10

# 深度搜索
node skills/tavily-search/scripts/search.js "machine learning" --deep

# 新闻搜索
node skills/tavily-search/scripts/search.js "AI news" --topic news
```

## 参数说明

| 参数 | 说明 | 默认值 |
|------|------|--------|
| `-n <count>` | 结果数量 (1-20) | 10 |
| `--depth <mode>` | 深度: ultra-fast, fast, basic, advanced | basic |
| `--topic <topic>` | 主题: general, news | general |
| `--time-range <range>` | 时间: day, week, month, year | - |
| `--include-domains` | 限定域名 | - |
| `--raw-content` | 包含完整内容 | false |

## 搜索深度

| 深度 | 延迟 | 适用场景 |
|------|------|---------|
| `ultra-fast` | 最低 | 实时聊天 |
| `fast` | 低 | 快速响应 |
| `basic` | 中等 | 通用搜索 |
| `advanced` | 较高 | 深度研究 |