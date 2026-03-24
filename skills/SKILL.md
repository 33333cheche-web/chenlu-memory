---
name: wechat-article
description: 抓取微信公众号文章，提取标题和内容并输出为 Markdown 格式。支持浏览器自动化绕过反爬。
metadata: { "openclaw": { "emoji": "📰", "requires": { "bins": ["python3"], "env": [] } } }
---

# 微信公众号文章抓取 v2.0

通过公众号链接获取文章的标题和内容，输出为 Markdown 格式。

**特性：**
- ✅ Playwright 浏览器自动化（绕过微信反爬）
- ✅ 代码块保留语言标识
- ✅ r.jina.ai 备用方案

## 安装依赖

```bash
pip3 install beautifulsoup4 markdownify playwright
playwright install chromium
```

## Usage

```bash
python3 skills/scripts/wechat_article.py '<公众号文章链接>'
```

## 输出示例

```markdown
# 文章标题

> 公众号: 某某公众号
> 发布时间: 2026-03-04 10:00:00
> 原文链接: https://mp.weixin.qq.com/s/xxx

---

文章正文内容...
```

## 提取策略（按优先级）

1. **r.jina.ai** - 第三方内容提取服务（最快）
2. **Playwright** - 模拟真实浏览器（最强反爬能力）

## 示例

```bash
# 基本使用
python3 skills/scripts/wechat_article.py "https://mp.weixin.qq.com/s/xxx"

# 输出到文件
python3 skills/scripts/wechat_article.py "https://mp.weixin.qq.com/s/xxx" > article.md
```

## 注意事项

- 首次运行会自动下载 Chromium（约 100MB）
- 部分文章可能需要验证码，这种情况无法自动处理
- 图片保留原始链接，不会下载到本地
