---
name: smart-fetch
description: |
  智能网页获取工具 - 多服务自动降级。
  自动尝试多种服务获取网页内容，返回干净的 Markdown 格式。
  无需 API Key，开箱即用。
version: 1.0.0
author: 晨露
tags: [web, fetch, markdown, scraping]
---

# Smart Fetch - 智能网页获取工具

## 简介

Smart Fetch 是一个智能网页获取工具，能够自动尝试多种服务获取网页内容，并按优先级自动降级，最终返回干净的 Markdown 格式。

## 特点

- ✅ **多服务自动降级** - 一个失败自动试下一个
- ✅ **返回干净 Markdown** - 无需额外处理
- ✅ **无需 API Key** - 开箱即用
- ✅ **支持大部分网站** - 包括新闻、博客、文档等
- ✅ **命令行 + Python API** - 多种使用方式

## 服务优先级

1. **Jina AI** (`r.jina.ai`) - 通用性强，效果稳定
2. **Bing Cache** - 备用方案
3. **Browser 兜底** - 使用 OpenClaw 内置 browser 工具

## 安装

### 1. 复制技能文件

将 `smart-fetch` 文件夹复制到目标实例的 skills 目录：

```bash
# 复制到 Sunny
scp -r smart-fetch/ sunny:~/.agents/skills/

# 复制到 Rainbow
scp -r smart-fetch/ rainbow:~/.openclaw/workspace-rainbow/skills/
```

### 2. 设置执行权限

```bash
chmod +x ~/.agents/skills/smart-fetch/scripts/smart-fetch
chmod +x ~/.agents/skills/smart-fetch/scripts/smart_fetch.py
```

## 使用方式

### 方式一：命令行

```bash
# 基本用法
~/.agents/skills/smart-fetch/scripts/smart-fetch https://example.com

# 输出 JSON 格式
~/.agents/skills/smart-fetch/scripts/smart-fetch https://example.com --json

# 只输出内容（用于管道）
~/.agents/skills/smart-fetch/scripts/smart-fetch https://example.com --raw > output.md

# 设置超时时间
~/.agents/skills/smart-fetch/scripts/smart-fetch https://example.com --timeout 30
```

### 方式二：Python API

```python
import sys
sys.path.insert(0, '~/.agents/skills/smart-fetch/scripts')
from smart_fetch import smart_fetch

# 获取网页
result = smart_fetch('https://example.com')

if result['success']:
    print(f"使用服务: {result['service']}")
    print(f"内容长度: {len(result['content'])} 字符")
    print(result['content'])
else:
    print(f"获取失败: {result['error']}")
```

### 方式三：在 Skill 中调用

```python
import subprocess

result = subprocess.run(
    ['python3', '~/.agents/skills/smart-fetch/scripts/smart_fetch.py', 
     'https://example.com', '--json'],
    capture_output=True,
    text=True
)

import json
data = json.loads(result.stdout)
if data['success']:
    content = data['content']
```

## 输出格式

### 普通模式
```
🌐 正在获取: https://example.com
--------------------------------------------------
⏳ 尝试 Jina AI... ✅ 成功
--------------------------------------------------
# 网页标题

网页内容...
```

### JSON 模式
```json
{
  "success": true,
  "content": "# 网页标题\n\n网页内容...",
  "service": "Jina AI",
  "url": "https://example.com"
}
```

## 使用场景

### 场景 1：获取新闻文章
```bash
smart-fetch https://news.example.com/article/123 --raw > article.md
```

### 场景 2：批量获取多个网页
```bash
for url in $(cat urls.txt); do
    smart-fetch "$url" --raw > "$(echo $url | md5sum | cut -d' ' -f1).md"
done
```

### 场景 3：在早报脚本中使用
```python
from smart_fetch import smart_fetch

urls = [
    'https://tech-news.com/article1',
    'https://ai-blog.com/post2',
]

for url in urls:
    result = smart_fetch(url, show_progress=False)
    if result['success']:
        # 处理内容
        process_content(result['content'])
```

## 常见问题

### Q: 为什么有些网站获取失败？
A: 部分网站有强反爬机制（如需要登录、验证码、JS 渲染等），这种情况下即使 Browser 兜底也可能失败。

### Q: 可以获取需要登录的页面吗？
A: 不可以。Smart Fetch 只能获取公开可访问的网页。需要登录的内容请使用 `bb-browser` 或 `agent-browser` 技能。

### Q: 获取的内容格式不对？
A: 部分网站结构特殊，可能导致 Markdown 转换不完美。可以尝试直接使用 `openclaw web-fetch` 或 `browser` 工具。

### Q: 如何加快获取速度？
A: 使用 `--raw` 参数可以跳过进度显示，稍微快一点。或者减少超时时间：`--timeout 10`。

## 相关工具

| 工具 | 用途 | 特点 |
|------|------|------|
| **smart-fetch** | 通用网页获取 | 自动降级，无需配置 |
| **tavily-search** | 新闻搜索 | 专门用于搜索 AI/科技新闻 |
| **bb-browser** | 浏览器自动化 | 能处理登录态、复杂交互 |
| **web_fetch** | 基础网页获取 | OpenClaw 内置，简单快速 |

## 更新日志

### v1.0.0 (2026-03-26)
- 初始版本
- 支持 Jina AI、Bing Cache、Browser 三种服务
- 支持命令行和 Python API

## 作者

晨露宝宝 🌟

---

*有问题随时问晨露哦～*
