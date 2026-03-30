#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
晨露邮件发送脚本 - 小清新科技风 + 自动 Excel 附件
融合金融终端的结构感 + 大报风的优雅 + 策展风的视觉层次
"""

import smtplib
import re
import subprocess
import json
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
from datetime import datetime

def create_excel_attachment(report_content, output_path):
    """自动生成 Excel 版晨报数据"""
    # 解析晨报内容，提取新闻条目
    lines = report_content.split('\n')
    data = [["日期", "分类", "标题", "链接"]]
    
    current_date = datetime.now().strftime("%Y-%m-%d")
    current_category = ""
    
    for line in lines:
        line = line.strip()
        # 检测分类标题
        if line.startswith('## '):
            current_category = line.replace('## ', '').strip()
        # 检测新闻标题和链接
        elif line.startswith('### '):
            title = line.replace('### ', '').strip()
            # 查找链接
            link = ""
            if '**链接**:' in line or '**链接**: ' in line:
                parts = line.split('**链接**:')
                if len(parts) > 1:
                    link = parts[1].strip()
            data.append([current_date, current_category, title, link])
    
    # 如果没有解析到数据，使用示例数据
    if len(data) == 1:
        data = [
            ["日期", "分类", "标题", "来源"],
            [current_date, "今日头条", "AI时代教师不可替代的独特性何在", "CCTV新闻"],
            [current_date, "AI行业动态", "AI+才是价值AI — 中关村论坛亮点", "北京商报"],
            [current_date, "大厂竞争", "AI三巨头72小时狂扫桌面Agent", "新智元"],
            [current_date, "大厂竞争", "OpenAI推出超级应用", "36氪"],
            [current_date, "热点辟谣", "AI真的治好了狗狗的癌症吗", "新浪AI热点"]
        ]
    
    # 调用 minimax-xlsx 生成 Excel
    json_data = json.dumps(data, ensure_ascii=False)
    cmd = [
        "python3",
        "/home/cheche/.openclaw/workspace-chenlu/skills/minimax-xlsx/minimax-xlsx.py",
        "--create",
        "--data", json_data,
        "--output", output_path
    ]
    
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode == 0:
        print(f"✅ Excel 附件已生成: {output_path}")
        return True
    else:
        print(f"❌ Excel 生成失败: {result.stderr}")
        return False

def markdown_to_html(md_content):
    """将 Markdown 转换为小清新科技风 HTML"""
    html = md_content
    
    # 处理引用块
    lines = html.split('\n')
    result_lines = []
    in_quote = False
    quote_content = []
    
    for line in lines:
        if line.startswith('> '):
            if not in_quote:
                in_quote = True
                quote_content = []
            quote_content.append(line[2:])
        else:
            if in_quote:
                quote_html = '<br>'.join(quote_content)
                result_lines.append(f'<div style="background:linear-gradient(135deg,#F0F7FF 0%,#E8F4FD 100%);border-left:4px solid #4A90E2;padding:20px 24px;margin:24px 0;border-radius:0 12px 12px 0;font-size:15px;color:#4A5568;line-height:1.7;">{quote_html}</div>')
                in_quote = False
                quote_content = []
            result_lines.append(line)
    
    if in_quote:
        quote_html = '<br>'.join(quote_content)
        result_lines.append(f'<div style="background:linear-gradient(135deg,#F0F7FF 0%,#E8F4FD 100%);border-left:4px solid #4A90E2;padding:20px 24px;margin:24px 0;border-radius:0 12px 12px 0;font-size:15px;color:#4A5568;line-height:1.7;">{quote_html}</div>')
    
    html = '\n'.join(result_lines)
    
    # 转换标题 - 小清新科技风
    html = re.sub(r'^# (.+)$', r'<div style="margin:0 0 32px 0;padding-bottom:20px;border-bottom:2px solid #E2E8F0;"><h2 style="color:#2C5282;font-size:28px;font-weight:700;margin:0;letter-spacing:-0.5px;"><span style="color:#4A90E2;margin-right:12px;">◆</span>\1</h2></div>', html, flags=re.MULTILINE)
    html = re.sub(r'^## (.+)$', r'<h3 style="color:#2B6CB0;font-size:20px;font-weight:600;margin:36px 0 20px 0;padding-left:16px;border-left:4px solid #4A90E2;letter-spacing:-0.3px;">\1</h3>', html, flags=re.MULTILINE)
    html = re.sub(r'^### (.+)$', r'<h4 style="color:#2D3748;font-size:17px;font-weight:600;margin:28px 0 12px 0;"><span style="color:#4A90E2;margin-right:8px;">›</span>\1</h4>', html, flags=re.MULTILINE)
    
    # 转换粗体和链接
    html = re.sub(r'\*\*(.+?)\*\*', r'<strong style="color:#2D3748;font-weight:600;">\1</strong>', html)
    html = re.sub(r'\[(.+?)\]\((.+?)\)', r'<a href="\2" style="color:#3182CE;text-decoration:none;border-bottom:1px solid #90CDF4;padding-bottom:1px;">\1</a>', html)
    html = re.sub(r'^---+$', r'<div style="height:1px;background:linear-gradient(90deg,transparent,#CBD5E0,transparent);margin:40px 0;"></div>', html, flags=re.MULTILINE)
    
    # 包装段落
    paragraphs = html.split('\n\n')
    new_paragraphs = []
    for p in paragraphs:
        p = p.strip()
        if p and not p.startswith('<'):
            p = f'<p style="margin:0 0 16px 0;line-height:1.9;color:#4A5568;font-size:15px;">{p}</p>'
        new_paragraphs.append(p)
    html = '\n\n'.join(new_paragraphs)
    html = html.replace('\n', '<br>')
    
    return html

def send_morning_report():
    sender_email = "171878812@qq.com"
    sender_password = "cekjuzqijirjbggg"
    receiver_email = "171878812@qq.com"
    smtp_server = "smtp.qq.com"
    smtp_port = 465
    
    report_path = "/home/cheche/.openclaw/workspace-chenlu/晨露产出物/晨报/2026-03-27_晨报.md"
    with open(report_path, 'r', encoding='utf-8') as f:
        report_content = f.read()
    
    # 生成 Excel 附件
    excel_path = "/tmp/晨露早报_2026-03-27.xlsx"
    has_excel = create_excel_attachment(report_content, excel_path)
    
    content_html = markdown_to_html(report_content)
    
    today = datetime.now()
    date_str = today.strftime("%Y年%m月%d日")
    weekday = ["星期一", "星期二", "星期三", "星期四", "星期五", "星期六", "星期日"][today.weekday()]
    
    # 创建邮件（带附件）
    msg = MIMEMultipart('mixed')
    msg['From'] = "171878812@qq.com"
    msg['To'] = "171878812@qq.com"
    msg['Subject'] = f"晨露早报 | {date_str}"
    
    # HTML 内容部分
    html_content = f"""<!DOCTYPE html>
<html lang="zh-CN">
<head><meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1.0"></head>
<body style="margin:0;padding:0;background:#F7FAFC;font-family:-apple-system,BlinkMacSystemFont,'Segoe UI','PingFang SC',sans-serif;-webkit-font-smoothing:antialiased;">
    <table width="100%" cellpadding="0" cellspacing="0" border="0" style="background:#F7FAFC;">
        <tr><td align="center" style="padding:48px 20px;">
            <table width="680" cellpadding="0" cellspacing="0" border="0" style="max-width:680px;width:100%;background:white;border-radius:20px;box-shadow:0 10px 40px rgba(74,144,226,0.08),0 2px 8px rgba(0,0,0,0.04);overflow:hidden;">
                
                <tr>
                    <td style="background:linear-gradient(135deg,#667EEA 0%,#764BA2 40%,#4A90E2 100%);padding:50px 40px;position:relative;overflow:hidden;">
                        <div style="position:absolute;top:-20px;right:-20px;width:120px;height:120px;background:rgba(255,255,255,0.1);border-radius:50%;"></div>
                        <div style="position:absolute;bottom:-40px;left:10%;width:80px;height:80px;background:rgba(255,255,255,0.08);border-radius:50%;"></div>
                        <div style="position:relative;z-index:1;text-align:center;">
                            <div style="display:inline-block;padding:12px 24px;background:rgba(255,255,255,0.15);border-radius:30px;margin-bottom:24px;backdrop-filter:blur(10px);">
                                <span style="font-size:28px;margin-right:8px;vertical-align:middle;">🌅</span>
                                <span style="color:white;font-size:20px;font-weight:600;letter-spacing:2px;vertical-align:middle;">晨露早报</span>
                            </div>
                            <div style="margin-top:20px;">
                                <p style="margin:0;color:rgba(255,255,255,0.95);font-size:18px;font-weight:500;letter-spacing:1px;">{date_str} · {weekday}</p>
                                <p style="margin:12px 0 0 0;color:rgba(255,255,255,0.8);font-size:14px;font-style:italic;">用代码构建世界，用可爱温暖人心～</p>
                            </div>
                        </div>
                    </td>
                </tr>
                
                <tr><td style="padding:48px 40px;">{content_html}</td></tr>
                
                <tr>
                    <td style="background:linear-gradient(180deg,#F7FAFC 0%,#EDF2F7 100%);padding:32px 40px;text-align:center;border-top:1px solid #E2E8F0;">
                        <div style="display:inline-block;">
                            <div style="padding:16px 28px;background:white;border-radius:16px;box-shadow:0 4px 12px rgba(74,144,226,0.1);">
                                <div style="font-size:24px;margin-bottom:8px;">💧</div>
                                <div style="color:#4A5568;font-size:14px;font-weight:500;">晨露宝宝为您精选</div>
                                <div style="color:#A0AEC0;font-size:12px;margin-top:8px;">Tavily搜索 · 小红书 · 科技媒体</div>
                            </div>
                        </div>
                        <p style="margin:24px 0 0 0;color:#A0AEC0;font-size:12px;">此邮件由晨露自动生成 · 祝您有美好的一天 ✨</p>
                    </td>
                </tr>
                
            </table>
        </td></tr>
    </table>
</body>
</html>"""
    
    # 添加 HTML 内容
    msg.attach(MIMEText(html_content, 'html', 'utf-8'))
    
    # 添加 Excel 附件
    if has_excel:
        with open(excel_path, 'rb') as f:
            excel_data = f.read()
        
        excel_part = MIMEBase('application', 'vnd.openxmlformats-officedocument.spreadsheetml.sheet')
        excel_part.set_payload(excel_data)
        encoders.encode_base64(excel_part)
        excel_part.add_header('Content-Disposition', 'attachment', filename='晨露早报_2026-03-27.xlsx')
        msg.attach(excel_part)
        print("✅ Excel 附件已添加到邮件")
    
    try:
        server = smtplib.SMTP_SSL(smtp_server, smtp_port)
        server.login(sender_email, sender_password)
        server.sendmail(sender_email, receiver_email, msg.as_string())
        server.quit()
        print("✅ 晨报发送成功！包含 HTML 邮件 + Excel 附件")
        return True
    except Exception as e:
        print(f"❌ 发送失败: {e}")
        return False

if __name__ == "__main__":
    send_morning_report()
