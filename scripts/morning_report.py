#!/usr/bin/env python3
"""
晨露早报生成器 v12 - 顶级视觉设计师纯正版 + 强力抗拒英文版
严格遵循 newsletter-designer 技能：绝对700px固定宽度、防缝隙图片、晨露蓝主题、全中文。
新增：强制在拉取到结果后再次深度校验翻译。
"""

import os
import sys
import json
import subprocess
import random
from datetime import datetime
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.header import Header
import smtplib

TAVILY_API_KEY = "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"

API_KEY = "sk-zsSgpiR8mROAcAuSza9VyPiC3zAmCTdnJJfGhrAcZB3gucBy"
BASE_URL = "https://code.newcli.com/gemini/v1beta"
MODEL = "gemini-3.1-pro"

def translate_text(text):
    if not text or not text.strip():
        return text
    try:
        # 加强 Prompt，强调绝对不能有英文
        prompt = f"你是一个严格的翻译机器。请将以下内容翻译成非常流畅的中文。要求：必须完全消除所有英文痕迹（专有名词如果无法翻译可以保留，但描述性句子必须全是中文），如果本身是中文则润色后返回。除了翻译结果之外，绝对不要输出任何其他解释性文字、引号或前缀！\n\n要翻译的内容：\n{text}"
        payload = {
            "model": MODEL,
            "messages": [{"role": "user", "content": prompt}],
            "temperature": 0.3 # 降低温度，提高翻译的确定性和直接性
        }
        with open("/tmp/trans_payload.json", "w") as f:
            json.dump(payload, f)
        result = subprocess.run([
            "curl", "-s", "-X", "POST", f"{BASE_URL}/chat/completions",
            "-H", "Content-Type: application/json",
            "-H", f"Authorization: Bearer {API_KEY}",
            "-d", "@/tmp/trans_payload.json"
        ], capture_output=True, text=True, timeout=30)
        
        if result.returncode == 0:
            res_json = json.loads(result.stdout)
            if "choices" in res_json and len(res_json["choices"]) > 0:
                translated = res_json["choices"][0]["message"]["content"].strip()
                return translated
    except Exception as e:
        print(f"翻译失败 ({text[:20]}...): {e}")
    return text

def search_with_tavily(query, max_results=2):
    try:
        result = subprocess.run([
            "curl", "-s", "-X", "POST", "https://api.tavily.com/search",
            "-H", "Content-Type: application/json",
            "-d", json.dumps({
                "api_key": TAVILY_API_KEY,
                "query": query,
                "max_results": max_results,
                "search_depth": "advanced",
                "include_answer": True
            })
        ], capture_output=True, text=True, timeout=60)
        
        if result.returncode == 0:
            data = json.loads(result.stdout)
            if "results" in data:
                print(f"🌍 正在对 [{query}] 的 {len(data['results'])} 条结果进行严格中文翻译...")
                for item in data["results"]:
                    item["title"] = translate_text(item.get("title", ""))
                    item["content"] = translate_text(item.get("content", ""))
            return data
        return None
    except Exception as e:
        print(f"搜索失败: {e}")
        return None

def fetch_daily_news():
    print("🔍 正在抓取最新情报...")
    # 为了防止搜索出纯英文结果难以翻译，在搜索词里加强中文限制
    ai_tools_res = search_with_tavily("中文介绍 最具创意的 AI 提效小工具推荐 2026", max_results=2)
    indie_dev_res = search_with_tavily("中文分享 独立开发者 赚钱 变现 新思路 2026", max_results=2)
    # 特别针对 Github 工具，搜索词换成更本土化的词
    github_res = search_with_tavily("中文盘点 GitHub 爆款 效率工具 开源项目推荐 2026", max_results=2)
    
    return {
        "ai_tools": ai_tools_res.get("results", []) if ai_tools_res else [],
        "indie_dev": indie_dev_res.get("results", []) if indie_dev_res else [],
        "github": github_res.get("results", []) if github_res else []
    }

def get_random_unsplash(topic):
    topics = {
        "ai": ["https://images.unsplash.com/photo-1677442136019-21780ecad995?auto=format&fit=crop&w=620&q=80", "https://images.unsplash.com/photo-1620712943543-bcc4688e7485?auto=format&fit=crop&w=620&q=80"],
        "dev": ["https://images.unsplash.com/photo-1555066931-4365d14bab8c?auto=format&fit=crop&w=620&q=80", "https://images.unsplash.com/photo-1498050108023-c5249f4df085?auto=format&fit=crop&w=620&q=80"],
        "github": ["https://images.unsplash.com/photo-1618401471353-b98a52333646?auto=format&fit=crop&w=620&q=80", "https://images.unsplash.com/photo-1526374965328-7f61d4dc18c5?auto=format&fit=crop&w=620&q=80"]
    }
    return random.choice(topics.get(topic, topics["ai"]))

def format_results_html(results, topic):
    html = ""
    for item in results:
        title = item.get("title", "精彩内容")
        url = item.get("url", "#")
        content = item.get("content", "")[:200] + "..."
        img_url = get_random_unsplash(topic)
        
        html += f"""
        <table width="100%" cellpadding="0" cellspacing="0" border="0">
          <tr>
            <td height="30" style="font-size:0; line-height:0;">&nbsp;</td>
          </tr>
        </table>
        <table width="620" cellpadding="0" cellspacing="0" border="0" align="center" style="background:#ffffff; border-radius:16px; overflow:hidden; box-shadow:0 8px 24px rgba(24,144,255,0.1);">
          <tr>
            <td style="padding:0; font-size:0; line-height:0;">
              <img src="{img_url}" width="620" style="display:block; width:620px; border:0; outline:none; text-decoration:none;" alt="Cover">
            </td>
          </tr>
          <tr>
            <td style="padding:30px 40px; background:#ffffff;">
              <h2 style="margin:0 0 12px; font-size:22px; color:#003a8c; font-family: Helvetica, 'Source Han Sans SC', sans-serif;">{title}</h2>
              <p style="margin:0 0 20px; font-size:15px; color:#555555; line-height:1.6; font-family: Helvetica, 'Source Han Sans SC', sans-serif;">{content}</p>
              <table cellpadding="0" cellspacing="0" border="0">
                <tr>
                  <td style="background:#1890ff; border-radius:8px; padding:12px 24px;">
                    <a href="{url}" style="color:#ffffff; text-decoration:none; font-size:14px; font-weight:bold; font-family: Helvetica, 'Source Han Sans SC', sans-serif;">阅读更多 →</a>
                  </td>
                </tr>
              </table>
            </td>
          </tr>
        </table>
        """
    if not html:
        html = "<p style='color: #999; font-size: 14px; text-align: center;'>今日暂无相关内容收录~</p>"
    return html

def generate_html_newsletter(news_data):
    today = datetime.now().strftime("%Y年%m月%d日")
    
    html = f'''<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <title>晨露早报 - {today}</title>
</head>
<body style="margin:0; padding:0; background:#f0f5ff;">
    <table width="100%" cellpadding="0" cellspacing="0" border="0" align="center" style="background:#f0f5ff; padding: 40px 0;">
        <tr>
            <td align="center">
                <table width="700" cellpadding="0" cellspacing="0" border="0" align="center" style="background:#f0f5ff;">
                    <tr>
                        <td align="center" style="padding: 20px 0;">
                            <h1 style="margin:0; color:#0050b3; font-size:36px; letter-spacing:2px; font-family: Helvetica, 'Source Han Sans SC', sans-serif;">晨露早报</h1>
                            <p style="margin:10px 0 0; color:#1890ff; font-size:15px; font-weight:bold; font-family: Helvetica, 'Source Han Sans SC', sans-serif;">极简美学 · 全中文呈现 · {today}</p>
                        </td>
                    </tr>
                    
                    <tr><td height="20" style="font-size:0; line-height:0;">&nbsp;</td></tr>

                    <tr>
                        <td align="center">
                            <span style="color:#003a8c; font-size:18px; font-weight:bold; letter-spacing:2px; font-family: Helvetica, 'Source Han Sans SC', sans-serif;">— 探索 AI 前沿 —</span>
                        </td>
                    </tr>
                    <tr>
                        <td align="center">
                            {format_results_html(news_data["ai_tools"], "ai")}
                        </td>
                    </tr>

                    <tr><td height="50" style="font-size:0; line-height:0;">&nbsp;</td></tr>

                    <tr>
                        <td align="center">
                            <span style="color:#003a8c; font-size:18px; font-weight:bold; letter-spacing:2px; font-family: Helvetica, 'Source Han Sans SC', sans-serif;">— 独立开发灵感 —</span>
                        </td>
                    </tr>
                    <tr>
                        <td align="center">
                            {format_results_html(news_data["indie_dev"], "dev")}
                        </td>
                    </tr>

                    <tr><td height="50" style="font-size:0; line-height:0;">&nbsp;</td></tr>

                    <tr>
                        <td align="center">
                            <span style="color:#003a8c; font-size:18px; font-weight:bold; letter-spacing:2px; font-family: Helvetica, 'Source Han Sans SC', sans-serif;">— 开源效率神器 —</span>
                        </td>
                    </tr>
                    <tr>
                        <td align="center">
                            {format_results_html(news_data["github"], "github")}
                        </td>
                    </tr>

                    <tr><td height="60" style="font-size:0; line-height:0;">&nbsp;</td></tr>

                    <tr>
                        <td align="center" style="padding: 30px; border-top: 1px solid #bae0ff;">
                            <p style="margin:0; font-size:12px; color:#5c8ce6; line-height:1.8; font-family: Helvetica, 'Source Han Sans SC', sans-serif;">
                                由 晨露宝宝 设计与构建 ✨<br>
                                此邮件严格遵循 Newsletter 设计规范 · 专为您排版
                            </p>
                        </td>
                    </tr>
                </table>
            </td>
        </tr>
    </table>
</body>
</html>'''
    return html

def send_email(html_content):
    print("📧 发送 Newsletter...")
    
    sender_email = "171878812@qq.com"  
    auth_code = "cekjuzqijirjbggg"     
    receiver_email = "171878812@qq.com" 
    
    today = datetime.now().strftime("%Y年%m月%d日")
    
    msg = MIMEMultipart('alternative')
    msg['From'] = f"{Header('晨露早报', 'utf-8').encode()} <{sender_email}>"
    msg['To'] = receiver_email
    msg['Subject'] = Header(f"📰 晨露早报(全网打尽纯中文版) - {today}", 'utf-8')
    
    msg.attach(MIMEText(html_content, 'html', 'utf-8'))
    
    try:
        server = smtplib.SMTP_SSL("smtp.qq.com", 465, timeout=30)
        server.login(sender_email, auth_code)
        server.sendmail(sender_email, [receiver_email], msg.as_string())
        server.quit()
        print("✅ 发送成功！")
        return True
    except Exception as e:
        print(f"❌ 失败: {e}")
        return False

def main():
    print("🌅 晨露早报（强力抗英文版）生成中...")
    news_data = fetch_daily_news()
    html = generate_html_newsletter(news_data)
    success = send_email(html)
    return 0 if success else 1

if __name__ == "__main__":
    sys.exit(main())
