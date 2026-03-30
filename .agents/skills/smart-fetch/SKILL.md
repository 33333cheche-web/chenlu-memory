---
name: smart-fetch
description: |
  智能网页获取工具 - 多服务自动降级。
  自动尝试 markdown.new / r.jina.ai / browser 等方式获取网页内容，
  返回干净的 Markdown 格式。
version: 1.0.0
---

# Smart Fetch - 智能网页获取

## 功能
自动尝试多种服务获取网页内容，按优先级降级：
1. **markdown.new/** - Cloudflare 的 Markdown 转换（对 CF 站点效果好）
2. **r.jina.ai/** - Jina AI 的网页提取（通用性强）
3. **Browser 兜底** - 使用 OpenClaw 内置 browser 工具

## 使用方式

### 命令行
```bash
# 直接运行
~/.agents/skills/smart-fetch/scripts/smart-fetch https://example.com

# 或使用 Python
python3 ~/.agents/skills/smart-fetch/scripts/smart_fetch.py https://example.com
```

### 在 Skill 中调用
```python
import subprocess

result = subprocess.run(
    ['python3', 'skills/smart-fetch/scripts/smart_fetch.py', url],
    capture_output=True,
    text=True
)
content = result.stdout
```

## 特点
- ✅ 自动降级，一个失败自动试下一个
- ✅ 返回干净 Markdown
- ✅ 支持大部分网站
- ✅ 无需 API Key

## 限制
- 部分强反爬网站可能 still 失败
- 需要网络连接
