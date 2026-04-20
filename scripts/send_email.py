#!/usr/bin/env python3
"""
晨露邮件发送工具 - Newsletter 版本
支持 HTML 邮件，newsletter 排版
用法: python3 send_email.py --report /path/to/report.txt
"""

import smtplib
import os
import re
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.header import Header
from datetime import datetime
from pathlib import Path

def load_env_file():
    """加载环境变量文件"""
    env_file = Path(__file__).parent.parent / '.env.mail'
    if env_file.exists():
        with open(env_file, 'r') as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith('#') and '=' in line:
                    key, value = line.split('=', 1)
                    os.environ[key] = value

load_env_file()

SMTP_CONFIG = {
    'host': os.getenv('SMTP_HOST', 'smtp.qq.com'),
    'port': int(os.getenv('SMTP_PORT', '587')),
    'sender': os.getenv('SMTP_SENDER', 'your_email@qq.com'),
    'password': os.getenv('SMTP_PASSWORD', ''),
    'sender_name': os.getenv('SMTP_SENDER_NAME', '晨露早报'),
    'recipient': os.getenv('RECIPIENT_EMAIL', '')
}

# Newsletter HTML 模板
HTML_TEMPLATE = """<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title}</title>
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Noto+Sans+SC:wght@400;500;700&display=swap');
        
        body {{
            margin: 0;
            padding: 0;
            font-family: 'Noto Sans SC', -apple-system, BlinkMacSystemFont, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
        }}
        
        .container {{
            max-width: 600px;
            margin: 0 auto;
            padding: 20px;
        }}
        
        .header {{
            text-align: center;
            padding: 30px 20px;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            border-radius: 16px 16px 0 0;
        }}
        
        .header h1 {{
            margin: 0;
            font-size: 28px;
            font-weight: 700;
            letter-spacing: 2px;
        }}
        
        .header .date {{
            margin-top: 10px;
            font-size: 14px;
            opacity: 0.9;
        }}
        
        .content {{
            background: white;
            padding: 30px;
            border-radius: 0 0 16px 16px;
            box-shadow: 0 10px 40px rgba(0,0,0,0.1);
        }}
        
        .section {{
            margin-bottom: 30px;
        }}
        
        .section-title {{
            font-size: 18px;
            font-weight: 700;
            color: #333;
            margin-bottom: 15px;
            padding-bottom: 10px;
            border-bottom: 2px solid #667eea;
            display: flex;
            align-items: center;
            gap: 8px;
        }}
        
        .section-content {{
            font-size: 14px;
            line-height: 1.8;
            color: #555;
        }}
        
        .section-content p {{
            margin: 10px 0;
        }}
        
        .tag {{
            display: inline-block;
            padding: 4px 12px;
            background: #f0f0f0;
            border-radius: 20px;
            font-size: 12px;
            color: #666;
            margin-right: 8px;
            margin-bottom: 8px;
        }}
        
        .highlight {{
            background: linear-gradient(120deg, #a8edea 0%, #fed6e3 100%);
            padding: 15px;
            border-radius: 12px;
            margin: 15px 0;
        }}
        
        .highlight-title {{
            font-weight: 700;
            color: #333;
            margin-bottom: 8px;
        }}
        
        .footer {{
            text-align: center;
            padding: 20px;
            color: #999;
            font-size: 12px;
        }}
        
        .footer a {{
            color: #667eea;
            text-decoration: none;
        }}
        
        .emoji {{
            font-size: 20px;
        }}
        
        ul {{
            padding-left: 20px;
        }}
        
        li {{
            margin: 8px 0;
        }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>📰 晨露早报</h1>
            <div class="date">{date}</div>
        </div>
        
        <div class="content">
            {content}
        </div>
        
        <div class="footer">
            <p>由 晨露宝宝 自动生成 🌟</p>
            <p>📄 <a href="{doc_url}">查看完整文档</a></p>
        </div>
    </div>
</body>
</html>"""

def encode_header(text):
    """编码邮件头"""
    return Header(text, 'utf-8').encode()

def parse_content_to_html(text):
    """解析文本内容为 HTML"""
    sections = []
    current_section = None
    current_content = []
    
    lines = text.strip().split('\n')
    
    for line in lines:
        line = line.strip()
        if not line:
            continue
            
        # 检测标题行（包含国旗或特殊标记）
        if any(flag in line for flag in ['🇨🇳', '🌍', '💡', '🎯', '🛠️', '📊']):
            if current_section:
                sections.append((current_section, '\n'.join(current_content)))
            current_section = line
            current_content = []
        elif line.startswith('===') or line.startswith('---'):
            continue
        elif current_section:
            current_content.append(line)
    
    if current_section:
        sections.append((current_section, '\n'.join(current_content)))
    
    # 生成 HTML
    html_parts = []
    for title, content in sections:
        emoji = ''
        if '🇨🇳' in title:
            emoji = '🇨🇳'
            title_clean = '国内热门'
        elif '🌍' in title:
            emoji = '🌍'
            title_clean = '国际趋势'
        elif '💡' in title:
            emoji = '💡'
            title_clean = '晨露推荐'
        elif '🎯' in title:
            emoji = '🎯'
            title_clean = '游戏方向'
        elif '🛠️' in title:
            emoji = '🛠️'
            title_clean = '工具方向'
        elif '📊' in title:
            emoji = '📊'
            title_clean = '技术建议'
        else:
            title_clean = title
        
        # 转换内容为 HTML
        content_html = content.replace('\n', '<br>')
        content_html = re.sub(r'•\s*', '• ', content_html)
        
        section_html = f'''
        <div class="section">
            <div class="section-title"><span class="emoji">{emoji}</span> {title_clean}</div>
            <div class="section-content">
                {content_html}
            </div>
        </div>
        '''
        html_parts.append(section_html)
    
    return '\n'.join(html_parts)

def send_newsletter(subject, text_content, html_content, to_email=None):
    """发送 Newsletter 邮件"""
    
    if to_email is None:
        to_email = SMTP_CONFIG['recipient'] or SMTP_CONFIG['sender']
    
    msg = MIMEMultipart('alternative')
    msg['From'] = f"{encode_header(SMTP_CONFIG['sender_name'])} <{SMTP_CONFIG['sender']}>"
    msg['To'] = to_email
    msg['Subject'] = encode_header(subject)
    
    # 纯文本版本（兼容旧邮箱）
    msg.attach(MIMEText(text_content, 'plain', 'utf-8'))
    
    # HTML 版本
    msg.attach(MIMEText(html_content, 'html', 'utf-8'))
    
    try:
        server = smtplib.SMTP(SMTP_CONFIG['host'], SMTP_CONFIG['port'])
        server.starttls()
        server.login(SMTP_CONFIG['sender'], SMTP_CONFIG['password'])
        server.sendmail(SMTP_CONFIG['sender'], to_email, msg.as_string())
        server.quit()
        
        print(f"✅ Newsletter 发送成功！")
        print(f"   收件人: {to_email}")
        print(f"   主题: {subject}")
        return True
        
    except Exception as e:
        print(f"❌ 发送失败: {e}")
        return False

def send_morning_report(text_content, doc_url=""):
    """发送早报 Newsletter"""
    
    today = datetime.now().strftime("%Y年%m月%d日")
    subject = f"📰 晨露早报 - {today}"
    
    # 生成 HTML 内容
    content_html = parse_content_to_html(text_content)
    
    # 生成完整 HTML
    html = HTML_TEMPLATE.format(
        title=subject,
        date=today,
        content=content_html,
        doc_url=doc_url or "https://www.feishu.cn/docx/BtdGdkdIFoDYhGxDn5zcoy3lnge"
    )
    
    return send_newsletter(subject, text_content, html)

if __name__ == '__main__':
    import argparse
    
    parser = argparse.ArgumentParser(description='晨露邮件发送工具')
    parser.add_argument('--report', help='报告文件路径', default=None)
    parser.add_argument('--doc-url', help='飞书文档链接', default='')
    
    args = parser.parse_args()
    
    if args.report and os.path.exists(args.report):
        with open(args.report, 'r', encoding='utf-8') as f:
            content = f.read()
        send_morning_report(content, args.doc_url)
    else:
        # 测试模式
        test_content = """🇨🇳 【国内热门小游戏/小程序】

🎮 B站热门游戏视频：
• 使用备用数据源...

📱 微信小程序热门：
• 休闲类：合成大西瓜、羊了个羊类
• 工具类：AI修图、语音转文字

🌍 【国际热门 - 已翻译】

🔥 Product Hunt 今日热门：
• AI 视频生成工具
• 语音克隆小程序

💡 【晨露建议可以做的方向】

🎯 小游戏方向：
• 合成类小游戏
• AI生成类工具
"""
        send_morning_report(test_content)
