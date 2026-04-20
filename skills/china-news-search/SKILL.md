---
name: china-news-search
description: |
  国内中文新闻搜索。使用方法：
  `node skills/china-news-search/scripts/search.js "关键词" [-n 数量] [-d 天数]`
  
  示例：
  - `node skills/china-news-search/scripts/search.js "AI新闻"`
  - `node skills/china-news-search/scripts/search.js "人工智能" -n 10 -d 3`
  
  专注中国新闻网站：新浪、网易、搜狐、腾讯、凤凰网、人民网、新华网等。
metadata:
  openclaw:
    emoji: "🇨🇳"
    requires:
      env: ["TAVILY_API_KEY"]
---

# 国内新闻搜索

## 快速使用

```bash
# 基本搜索（默认5条，1天内）
node skills/china-news-search/scripts/search.js "AI新闻"

# 指定数量
node skills/china-news-search/scripts/search.js "人工智能" -n 10

# 指定时间范围（3天内）
node skills/china-news-search/scripts/search.js "科技动态" -d 3

# 组合使用
node skills/china-news-search/scripts/search.js "经济报告" -n 10 -d 7
```

## 参数说明

| 参数 | 说明 | 默认值 |
|------|------|--------|
| `-n, --number` | 结果数量 | 5 |
| `-d, --days` | 时间范围（天） | 1 |

## 搜索源

- 新浪 (sina.com.cn)
- 网易 (163.com)
- 搜狐 (sohu.com)
- 腾讯 (qq.com)
- 凤凰网 (ifeng.com)
- 人民网 (people.com.cn)
- 新华网 (xinhuanet.com)

## 特点

- ✅ 专注国内新闻源
- ✅ 中文内容优化
- ✅ 使用 Tavily API Key（已配置）
- ✅ 支持时间过滤
