#!/usr/bin/env python3
"""
Smart Fetch - 智能网页获取工具
多服务自动降级，返回干净 Markdown

用法:
    python3 smart_fetch.py <URL> [选项]
    
选项:
    --json          输出 JSON 格式
    --raw           只输出内容，不显示进度
    --timeout N     设置超时时间（默认 15 秒）
    
示例:
    python3 smart_fetch.py https://example.com
    python3 smart_fetch.py https://example.com --json
"""

import sys
import urllib.request
import urllib.error
import ssl
import json
import subprocess
import time
import argparse
from urllib.parse import quote

# 服务配置（按优先级排序）
SERVICES = [
    ("https://r.jina.ai/http://", "Jina AI"),
    ("https://r.jina.ai/", "Jina AI (HTTPS)"),
    ("https://r.jina.ai/http://cc.bingj.com/cache.aspx?d=455-1277-1704&u=", "Bing Cache"),
]

def create_ssl_context():
    """创建忽略证书验证的 SSL 上下文"""
    ctx = ssl.create_default_context()
    ctx.check_hostname = False
    ctx.verify_mode = ssl.CERT_NONE
    return ctx

def fetch_with_service(url, service_url, timeout=15):
    """使用指定服务获取网页内容"""
    target = f"{service_url}{quote(url, safe=':/?#[]@!$&\'()*+,;=')}"
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36'
    }
    
    try:
        ctx = create_ssl_context()
        req = urllib.request.Request(target, headers=headers)
        with urllib.request.urlopen(req, timeout=timeout, context=ctx) as response:
            content = response.read().decode('utf-8', errors='ignore')
            # 检查内容是否有效（至少 500 字符且包含实际内容）
            if len(content) > 500 and not content.startswith('{'):
                return content
            return None
    except Exception:
        return None

def fetch_with_browser(url, timeout=30):
    """使用 web_fetch 工具兜底"""
    try:
        result = subprocess.run(
            ['openclaw', 'web-fetch', url],
            capture_output=True,
            text=True,
            timeout=timeout
        )
        if result.returncode == 0 and result.stdout:
            return result.stdout
        return None
    except Exception:
        return None

def smart_fetch(url, show_progress=True, timeout=15):
    """
    智能获取网页内容
    
    Args:
        url: 目标网页 URL
        show_progress: 是否显示进度信息
        timeout: 每个服务的超时时间
        
    Returns:
        dict: 包含 success, content, service 的字典
    """
    if show_progress:
        print(f"🌐 正在获取: {url}", file=sys.stderr)
        print("-" * 50, file=sys.stderr)
    
    # 尝试各个服务
    for service_url, name in SERVICES:
        if show_progress:
            print(f"⏳ 尝试 {name}...", end=" ", flush=True, file=sys.stderr)
        
        content = fetch_with_service(url, service_url, timeout)
        
        if content:
            if show_progress:
                print(f"✅ 成功", file=sys.stderr)
            return {
                "success": True,
                "content": content,
                "service": name,
                "url": url
            }
        
        if show_progress:
            print(f"❌ 失败", file=sys.stderr)
        time.sleep(0.3)
    
    # 最后尝试 browser 兜底
    if show_progress:
        print(f"⏳ 尝试 Browser 兜底...", end=" ", flush=True, file=sys.stderr)
    
    content = fetch_with_browser(url, timeout)
    
    if content:
        if show_progress:
            print(f"✅ 成功", file=sys.stderr)
        return {
            "success": True,
            "content": content,
            "service": "Browser",
            "url": url
        }
    
    if show_progress:
        print(f"❌ 失败", file=sys.stderr)
    
    return {
        "success": False,
        "content": None,
        "service": None,
        "url": url,
        "error": "所有服务都失败了"
    }

def main():
    parser = argparse.ArgumentParser(
        description='智能网页获取工具 - 多服务自动降级',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  python3 smart_fetch.py https://example.com
  python3 smart_fetch.py https://example.com --json
  python3 smart_fetch.py https://example.com --raw > output.md
        """
    )
    parser.add_argument('url', help='目标网页 URL')
    parser.add_argument('--json', action='store_true', help='输出 JSON 格式')
    parser.add_argument('--raw', action='store_true', help='只输出内容，不显示进度')
    parser.add_argument('--timeout', type=int, default=15, help='超时时间（秒）')
    
    args = parser.parse_args()
    
    # 确保 URL 有协议
    url = args.url
    if not url.startswith(('http://', 'https://')):
        url = 'https://' + url
    
    # 获取内容
    result = smart_fetch(url, show_progress=not args.raw, timeout=args.timeout)
    
    # 输出结果
    if args.json:
        print(json.dumps(result, ensure_ascii=False, indent=2))
    elif args.raw:
        if result['success']:
            print(result['content'])
        else:
            print(f"Error: {result['error']}", file=sys.stderr)
            sys.exit(1)
    else:
        print("-" * 50)
        if result['success']:
            print(result['content'])
        else:
            print(f"\n❌ {result['error']}")
            sys.exit(1)

if __name__ == "__main__":
    main()
