#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
微信公众号文章抓取工具 v2.0
融合 r.jina.ai + Playwright 浏览器自动化
"""

import sys
import re
import asyncio
from datetime import datetime

# 尝试导入 Playwright
try:
    from playwright.async_api import async_playwright
    PLAYWRIGHT_AVAILABLE = True
except ImportError:
    PLAYWRIGHT_AVAILABLE = False
    print("⚠️ Playwright 未安装，浏览器模式不可用", file=sys.stderr)


# ============================================================
# 策略 1: r.jina.ai (轻量级，可能失效)
# ============================================================

def fetch_via_jina(url: str) -> dict:
    """使用 r.jina.ai 提取文章内容"""
    import requests
    
    jina_url = f"https://r.jina.ai/{url}"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
        "X-Return-Format": "markdown",
        "X-With-Links-Summary": "true",
    }
    
    try:
        response = requests.get(jina_url, headers=headers, timeout=30)
        response.raise_for_status()
        content = response.text.strip()
        
        if content and "环境异常" not in content and "验证码" not in content and len(content) > 100:
            return {
                "success": True,
                "method": "jina.ai",
                "content": content,
                "html": None  # jina.ai 不返回 HTML
            }
        return {"success": False, "method": "jina.ai", "error": "内容被拦截或为空"}
    except Exception as e:
        return {"success": False, "method": "jina.ai", "error": str(e)}


# ============================================================
# 策略 2: Playwright 浏览器自动化 (反爬能力强)
# ============================================================

async def fetch_via_playwright(url: str) -> dict:
    """使用 Playwright 模拟浏览器抓取"""
    if not PLAYWRIGHT_AVAILABLE:
        return {"success": False, "method": "playwright", "error": "Playwright 未安装"}
    
    try:
        async with async_playwright() as p:
            # 启动浏览器（使用 Chromium）
            browser = await p.chromium.launch(headless=True)
            context = await browser.new_context(
                user_agent="Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
                viewport={"width": 1280, "height": 800},
                locale="zh-CN"
            )
            
            # 设置额外的请求头
            await context.set_extra_http_headers({
                "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
                "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8",
                "Accept-Encoding": "gzip, deflate, br",
                "DNT": "1",
                "Connection": "keep-alive",
                "Upgrade-Insecure-Requests": "1"
            })
            
            page = await context.new_page()
            
            # 访问页面
            print("🦊 Playwright: 正在打开页面...", file=sys.stderr)
            await page.goto(url, wait_until="domcontentloaded", timeout=30000)
            
            # 等待正文加载
            try:
                await page.wait_for_selector("#js_content", timeout=10000)
                print("🦊 Playwright: 正文已加载", file=sys.stderr)
            except:
                print("🦊 Playwright: 等待正文超时，继续尝试...", file=sys.stderr)
            
            # 额外等待确保 JS 执行完毕
            await asyncio.sleep(2)
            
            # 获取 HTML 内容
            html = await page.content()
            
            await browser.close()
            
            # 检查是否被拦截
            if "环境异常" in html or "验证码" in html or "biz.tabbar.js" in html:
                return {"success": False, "method": "playwright", "error": "触发了验证码"}
            
            return {
                "success": True,
                "method": "playwright",
                "html": html
            }
            
    except Exception as e:
        return {"success": False, "method": "playwright", "error": str(e)}


# ============================================================
# HTML 解析 (类似 jackwener 的实现)
# ============================================================

def extract_timestamp_from_html(html: str) -> str:
    """从 HTML 中提取发布时间"""
    # 尝试多种格式
    patterns = [
        r'create_time\s*:\s*JsDecode\(["\']?(\d+)["\']?\)',
        r'create_time\s*:\s*["\']?(\d+)["\']?',
        r'create_time\s*=\s*["\']?(\d+)["\']?',
        r'publish_time\s*[=:]\s*["\']?(\d+)["\']?',
    ]
    
    for pattern in patterns:
        match = re.search(pattern, html)
        if match:
            try:
                ts = int(match.group(1))
                if ts > 1000000000:  # 合理的 Unix 时间戳
                    dt = datetime.fromtimestamp(ts)
                    return dt.strftime("%Y-%m-%d %H:%M:%S")
            except:
                continue
    
    return ""


def extract_metadata_from_html(html: str) -> dict:
    """从 HTML 中提取文章元数据"""
    from bs4 import BeautifulSoup
    
    soup = BeautifulSoup(html, "html.parser")
    
    # 提取标题
    title = "未知标题"
    title_el = soup.select_one("#activity-name")
    if title_el:
        title = title_el.get_text(strip=True)
    else:
        # 备用方案
        title_match = re.search(r'<title>(.*?)</title>', html, re.IGNORECASE)
        if title_match:
            title = title_match.group(1).strip()
    
    # 提取公众号名
    author = ""
    author_el = soup.select_one("#js_name")
    if author_el:
        author = author_el.get_text(strip=True)
    
    # 提取发布时间
    publish_time = extract_timestamp_from_html(html)
    
    return {
        "title": title,
        "author": author,
        "publish_time": publish_time
    }


def extract_content_from_html(html: str) -> tuple:
    """提取正文内容，返回 (content_html, code_blocks)"""
    from bs4 import BeautifulSoup
    
    soup = BeautifulSoup(html, "html.parser")
    content_el = soup.select_one("#js_content")
    
    if not content_el:
        return None, []
    
    # 1. 处理图片：data-src -> src (微信懒加载)
    for img in content_el.find_all("img"):
        data_src = img.get("data-src")
        if data_src:
            img["src"] = data_src
    
    # 2. 处理代码块
    code_blocks = []
    for el in content_el.select(".code-snippet__fix"):
        # 移除行号
        for line_idx in el.select(".code-snippet__line-index"):
            line_idx.decompose()
        
        pre = el.select_one("pre[data-lang]")
        lang = pre.get("data-lang", "") if pre else ""
        
        lines = []
        for code_tag in el.find_all("code"):
            text = code_tag.get_text()
            # 跳过 CSS counter 垃圾行
            if re.match(r"^[ce]?ounter\(line", text):
                continue
            lines.append(text)
        
        if not lines:
            lines.append(el.get_text())
        
        placeholder = f"CODEBLOCK-PLACEHOLDER-{len(code_blocks)}"
        code_blocks.append({"lang": lang, "code": "\n".join(lines)})
        el.replace_with(soup.new_tag("p", string=placeholder))
    
    # 3. 移除噪声元素
    for sel in ("script", "style", ".qr_code_pc", ".reward_area", ".rich_media_tool"):
        for tag in content_el.select(sel):
            tag.decompose()
    
    return str(content_el), code_blocks


# ============================================================
# Markdown 转换
# ============================================================

def html_to_markdown(content_html: str, code_blocks: list) -> str:
    """将 HTML 转换为 Markdown"""
    try:
        import markdownify
    except ImportError:
        # 备用方案：简单去除 HTML 标签
        print("⚠️ markdownify 未安装，使用简化转换", file=sys.stderr)
        text = re.sub(r'<[^>]+>', '\n', content_html)
        text = re.sub(r'\n{3,}', '\n\n', text)
        return text.strip()
    
    md = markdownify.markdownify(
        content_html,
        heading_style="ATX",
        bullets="-",
        convert=["p", "h1", "h2", "h3", "h4", "h5", "h6",
                 "strong", "em", "a", "img", "ul", "ol", "li",
                 "blockquote", "br", "hr", "table", "thead",
                 "tbody", "tr", "th", "td", "pre", "code"],
    )
    
    # 还原代码块占位符
    for i, block in enumerate(code_blocks):
        placeholder = f"CODEBLOCK-PLACEHOLDER-{i}"
        fenced = f"\n```{block['lang']}\n{block['code']}\n```\n"
        md = md.replace(placeholder, fenced)
    
    # 清理
    md = md.replace("\u00a0", " ")
    md = re.sub(r"\n{4,}", "\n\n\n", md)
    md = re.sub(r"[ \t]+$", "", md, flags=re.MULTILINE)
    
    return md


# ============================================================
# 主流程
# ============================================================

def format_markdown(title: str, content: str, url: str, publish_time: str = "", account: str = "") -> str:
    """格式化为 Markdown"""
    lines = [f"# {title}", ""]
    
    meta_parts = []
    if account:
        meta_parts.append(f"公众号: {account}")
    if publish_time:
        meta_parts.append(f"发布时间: {publish_time}")
    meta_parts.append(f"原文链接: {url}")
    
    for part in meta_parts:
        lines.append(f"> {part}")
    
    lines.extend(["", "---", ""])
    lines.append(content)
    
    return "\n".join(lines)


async def wechat_article_async(url: str) -> dict:
    """异步主函数：抓取微信公众号文章"""
    
    if not url or "mp.weixin.qq.com" not in url:
        return {"success": False, "error": "无效的微信公众号文章链接"}
    
    result = None
    html = None
    method = None
    
    # 策略 1: jina.ai
    print("📡 尝试 jina.ai...", file=sys.stderr)
    result = fetch_via_jina(url)
    if result["success"]:
        print("✅ jina.ai 成功", file=sys.stderr)
        method = "jina.ai"
        # jina.ai 返回的是 markdown，不需要再解析 HTML
        from bs4 import BeautifulSoup
        parsed = extract_metadata_from_html(result.get("html", "") or result["content"])
        content = result["content"]
        img_urls = []
        
        return {
            "success": True,
            "method": method,
            "title": parsed["title"],
            "content": content,
            "author": parsed["author"],
            "publish_time": parsed["publish_time"],
            "url": url
        }
    
    # 策略 2: Playwright 浏览器
    print("📡 尝试 Playwright 浏览器...", file=sys.stderr)
    result = await fetch_via_playwright(url)
    if result["success"]:
        print("✅ Playwright 成功", file=sys.stderr)
        html = result["html"]
        method = "playwright"
    
    if not html:
        return {"success": False, "error": "所有提取方式都失败了"}
    
    # 解析 HTML
    meta = extract_metadata_from_html(html)
    content_html, code_blocks = extract_content_from_html(html)
    
    if not content_html:
        return {"success": False, "error": "未能提取到正文内容"}
    
    # 转换为 Markdown
    md_content = html_to_markdown(content_html, code_blocks)
    
    return {
        "success": True,
        "method": method,
        "title": meta["title"],
        "content": md_content,
        "author": meta["author"],
        "publish_time": meta["publish_time"],
        "url": url
    }


def wechat_article(url: str, output_dir: str = None) -> str:
    """
    同步入口函数
    返回 Markdown 字符串或错误信息
    """
    # 运行异步抓取
    result = asyncio.run(wechat_article_async(url))
    
    if not result["success"]:
        return f"❌ 抓取失败：{result.get('error', '未知错误')}"
    
    # 直接返回 Markdown，不下载图片
    return format_markdown(
        title=result["title"],
        content=result["content"],
        url=result["url"],
        publish_time=result.get("publish_time", ""),
        account=result.get("author", "")
    )


def main():
    if len(sys.argv) < 2:
        print("用法：python3 wechat_article.py '<公众号文章链接>'")
        print("示例：python3 wechat_article.py 'https://mp.weixin.qq.com/s/xxx'")
        sys.exit(1)
    
    url = sys.argv[1]
    
    # 检查依赖
    try:
        from bs4 import BeautifulSoup
    except ImportError:
        print("❌ 缺少依赖: beautifulsoup4。请运行: pip install beautifulsoup4", file=sys.stderr)
        sys.exit(1)
    
    # 抓取
    output = wechat_article(url)
    print(output)


if __name__ == "__main__":
    main()
