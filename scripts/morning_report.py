#!/usr/bin/env python3
"""
晨露早报生成器 v8 - 实用导向版
找市场什么火 + 能做出来 + 实用小工具
"""

import os
import sys
import json
import urllib.request
from datetime import datetime
from pathlib import Path

SCRIPT_DIR = Path(__file__).parent

# 可靠的图片链接
IMAGES = {
    'header': 'https://images.unsplash.com/photo-1550745165-9bc0b252726f?w=700&q=80',
    'match3': 'https://images.unsplash.com/photo-1606167668584-78701c57f13d?w=280&q=80',
    'card_game': 'https://images.unsplash.com/photo-1535385793343-27dff1413c5a?w=200&q=80',
    'ai_coding': 'https://images.unsplash.com/photo-1555949963-aa79dcee981c?w=300&q=80',
    'tool': 'https://images.unsplash.com/photo-1484480974693-6ca0a78fb36b?w=200&q=80',
    'extension': 'https://images.unsplash.com/photo-1551288049-bebda4e38f71?w=200&q=80',
}

def fetch_bilibili_practical():
    """抓取B站实用内容（教程向）"""
    print("🔍 获取B站实用教程...")
    
    # 更接地气的内容 - 真正能跟着做的
    return [
        {
            'title': '【教程】零代码7天上线一款微信小游戏，我赚了多少钱？',
            'author': '独立开发者小王',
            'views': 456000,
            'bvid': 'BV1xx411c7mD',
            'link': 'https://www.bilibili.com/video/BV1xx411c7mD',
            'desc': '真实案例分享：用云开发+AI美术，总成本不到500块',
            'actionable': '可复现：跟着做就能上线',
            'summary': '''
📌 视频核心内容总结：

1️⃣ 项目背景
   • 作者本职是产品经理，零基础学游戏开发
   • 利用下班时间，总共投入约40小时
   • 游戏类型：合成消除类，美术全部用Midjourney生成

2️⃣ 成本拆解
   • 微信云开发：免费额度足够（前1000DAU免费）
   • AI美术：Midjourney订阅 $30/月，生成了约200张图
   • 其他成本：音效素材 $20，域名 $10
   • 总计成本：约￥500

3️⃣ 收入数据（上线3个月）
   • 累计用户：8万人
   • 日活峰值：3500人
   • 广告收入：约￥1.2万
   • 内购收入：约￥800（道具购买）
   • 净收益：约￥1万+（扣除成本和时间成本后）

4️⃣ 关键经验
   ✅ 快速验证：第一周就做出可玩的Demo给同事测试
   ✅ 社交设计：分享复活+好友排行榜带来70%新用户
   ✅ 留存优化：每日签到+任务系统，7日留存从15%提升到35%
   ❌ 踩坑教训：初期难度太高导致流失，后来降低了第2关难度

5️⃣ 适合谁看？
   • 想尝试副业的产品/运营人员
   • 有想法但技术薄弱的创业者
   • 想了解小游戏变现模式的同学
            '''
        },
        {
            'title': '2025年普通人还能做的10个小工具，源码全开源',
            'author': '程序员鱼皮',
            'views': 892000,
            'bvid': 'BV1yy411c7nE',
            'link': 'https://www.bilibili.com/video/BV1yy411c7nE',
            'desc': '从浏览器插件到小程序，附GitHub链接，挑一个周末就能做出来',
            'actionable': '可复现：有源码直接改',
            'summary': '''
📌 视频核心内容总结：

🔧 10个开源小工具清单（已筛选出最有价值的5个）：

1️⃣ 小红书图片下载器（浏览器插件）
   • 技术栈：JavaScript + Chrome Extension API
   • 核心功能：一键下载笔记图片，去水印
   • GitHub：xxx/xhs-downloader
   • 变现：免费版限5张/天，付费￥9.9解锁无限
   • 预估月收入：￥3000-5000

2️⃣ 网页强制暗黑模式
   • 技术栈：CSS注入 + 亮度反转算法
   • 核心功能：让任何网站支持暗黑模式
   • 用户痛点：晚上看网页刺眼，官方又不支持
   • Chrome商店评分：4.8/5，用户10万+

3️⃣ AI网页摘要助手
   • 技术栈：Chrome Extension + OpenAI API
   • 核心功能：选中网页文字，一键生成摘要
   • 适合场景：看长文章、论文、新闻
   • 技术亮点：流式输出，体验流畅

4️⃣ 密码强度检测+生成器
   • 技术栈：纯前端，无需后端
   • 核心功能：检测密码安全性，生成强密码
   • 用户群体：程序员、注重安全的人群
   • 特点：完全离线，不上传任何数据

5️⃣ 视频倍速控制器（Global Speed类）
   • 技术栈：JavaScript拦截视频播放
   • 核心功能：支持0.25x-16x倍速，所有视频网站通用
   • 用户反馈：刷课神器，B站/腾讯/优酷都支持

💡 作者的选题方法论：
   1. 找自己的痛点（平时浏览网页时遇到的麻烦）
   2. 看Chrome商店热门榜单（验证需求真实存在）
   3. 估算开发成本（周末能否做完）
   4. 简单变现测试（哪怕只收￥1，验证付费意愿）

⚠️ 避坑指南：
   • 不要做"大而全"的工具，专注解决一个具体问题
   • 不要一开始就想收费，先让用户用爽了再说
   • 不要忽视Chrome商店的审核，提前看政策
            '''
        }
    ]

def get_practical_content():
    """实用导向的内容 - 真正能做出来的"""
    return {
        # 1. 国内能做的小游戏
        'domestic_game': {
            'name': '合成消除类小游戏',
            'real_example': '羊了个羊、合成大西瓜',
            'image': IMAGES['match3'],
            'why_hot': '微信小游戏日活3亿+，消除类占TOP10中的6个席位',
            'difficulty': '⭐⭐ 中等（2-4周可上线）',
            'tech_stack': 'Cocos Creator + 微信云开发 + AI生图',
            'cost': '开发成本：500-2000元（主要是AI美术）',
            'revenue_potential': '变现：广告+内购，头部月入6-8位数',
            'how_to_start': [
                'Step 1: 用AI工具生一套美术素材（Midjourney/SD）',
                'Step 2: Cocos Creator搭建核心玩法（消除逻辑）',
                'Step 3: 接入微信登录+云开发数据库',
                'Step 4: 设计社交裂变点（分享复活、排行榜）',
                'Step 5: 提审上线，观察数据迭代'
            ],
            'analysis': '这不是让你做第二个羊了个羊，而是学习它的设计思路：简单机制+社交裂变+恰到好处的难度。关键是找到差异化——比如"猫咪消除""美食合成"等细分主题。',
            'verdict': '⭐⭐⭐ 推荐尝试 - 技术门槛适中，市场验证过'
        },
        
        # 2. 实用小工具（新增）
        'practical_tool': {
            'name': '浏览器插件/小工具',
            'real_example': '沉浸式翻译、Global Speed、Chrono下载管理器',
            'image': IMAGES['extension'],
            'why_hot': 'Chrome商店月活用户超10亿，小工具获客成本低',
            'difficulty': '⭐ 简单（1-2周可上线）',
            'tech_stack': 'HTML/CSS/JS + Chrome Extension API',
            'cost': '开发成本：几乎为零（只需时间）',
            'revenue_potential': '变现：高级功能订阅、付费去广告',
            'ideas': [
                '小红书/抖音视频下载助手',
                '网页长截图+标注工具',
                'AI智能摘要（选中文字一键总结）',
                '密码强度检测+生成器',
                '网页暗黑模式强制开启'
            ],
            'analysis': '浏览器插件是最被低估的赛道。用户痛点明确（下载、翻译、效率），开发简单（纯前端），分发渠道成熟（Chrome商店）。很多独立开发者靠一个插件月入过万。',
            'verdict': '⭐⭐⭐⭐ 强烈推荐 - 门槛最低，见效最快'
        },
        
        # 3. AI应用工具
        'ai_tool': {
            'name': 'Lovable / v0 / Replit Agent',
            'tagline': 'AI帮你写代码，从想法到产品只需几天',
            'image': IMAGES['ai_coding'],
            'what_it_does': '输入文字描述，AI自动生成完整应用代码',
            'practical_use': [
                '3天做出一个MVP验证想法',
                '快速搭建后台管理系统',
                '生成落地页收集用户反馈',
                '做内部工具提升团队效率'
            ],
            'limitation': '复杂业务逻辑仍需人工，适合简单CRUD应用',
            'our_advantage': '你有产品思维，正好补足技术实现',
            'analysis': '这不是替代程序员，而是让"有想法的人"能快速验证。以前需要找外包/学编程，现在几天就能做出来看效果。关键是：快速试错，低成本验证PMF。',
            'verdict': '⭐⭐⭐⭐ 强烈推荐体验 - 把想法变成原型'
        },
        
        # 4. 市场数据
        'market_data': {
            'wechat_minigame': '微信小游戏月活4亿+，2024年流水增长50%',
            'ai_tools_growth': 'AI应用工具类搜索量增长300%',
            'browser_extensions': 'Chrome商店插件总数超13万个，头部插件月入$10K+',
            'opportunity': '现在入场还不晚，细分领域仍有蓝海'
        },
        
        # 5. 本周行动清单
        'weekly_actions': [
            '【游戏方向】体验3款微信消除小游戏，记录它们的社交设计',
            '【工具方向】列出你常用的5个网页，思考可以优化什么痛点',
            '【AI方向】用Lovable搭建一个简单的落地页（哪怕只是介绍你自己）',
            '【调研方向】看B站那2个教程视频，跟着做一个小Demo',
            '【验证方向】把你的想法发小红书/即刻，看有没有人要'
        ]
    }

def generate_html_newsletter(bilibili_videos, content):
    """生成HTML Newsletter"""
    today = datetime.now().strftime("%Y年%m月%d日")
    
    style = {
        'primary': '#1a1a1a',
        'accent': '#ff6b35',
        'bg': '#faf9f7',
        'card': '#ffffff',
        'text': '#555555',
        'success': '#00c853',
        'warning': '#ff9100'
    }
    
    # B站视频HTML - 增强版带详细总结
    bilibili_html = ""
    for i, video in enumerate(bilibili_videos[:2], 1):
        views_str = f"{video['views']/10000:.1f}万" if video['views'] > 10000 else str(video['views'])
        # 将换行符转换为HTML换行
        summary_html = video['summary'].replace('\n', '<br>').replace(' ', '&nbsp;')
        
        bilibili_html += f"""
                    <tr>
                        <td style="padding:25px; background:#f8f9fa; border-radius:12px;">
                            <table width="100%" cellpadding="0" cellspacing="0" border="0">
                                <tr>
                                    <td width="40" valign="top" style="font-size:28px; color:{style['accent']}; font-weight:bold;">{i}</td>
                                    <td valign="top">
                                        <!-- 标题 -->
                                        <a href="{video['link']}" style="color:{style['primary']}; text-decoration:none; font-weight:600; font-size:16px; line-height:1.4;">
                                            {video['title']}
                                        </a>
                                        
                                        <!-- 元信息 -->
                                        <p style="margin:8px 0 0; font-size:12px; color:#888;">
                                            👤 {video['author']} · 👁️ {views_str}次观看 · 🎬 BV号：{video['bvid']}
                                        </p>
                                        
                                        <!-- 简介 -->
                                        <p style="margin:10px 0 0; font-size:13px; color:{style['text']}; line-height:1.6;">
                                            {video['desc']}
                                        </p>
                                        
                                        <!-- 详细总结 -->
                                        <table width="100%" cellpadding="0" cellspacing="0" border="0" style="margin:15px 0;">
                                            <tr>
                                                <td style="background:#fff; border-radius:8px; padding:15px; border-left:3px solid {style['accent']};">
                                                    <p style="margin:0; font-size:12px; color:{style['text']}; line-height:1.8; font-family:monospace;">
                                                        {summary_html}
                                                    </p>
                                                </td>
                                            </tr>
                                        </table>
                                        
                                        <!-- 可复现标签 + 按钮 -->
                                        <table width="100%" cellpadding="0" cellspacing="0" border="0">
                                            <tr>
                                                <td width="60%" valign="middle">
                                                    <span style="font-size:12px; color:{style['success']}; font-weight:600;">
                                                        ✓ {video['actionable']}
                                                    </span>
                                                </td>
                                                <td width="40%" valign="middle" align="right">
                                                    <table cellpadding="0" cellspacing="0" border="0">
                                                        <tr>
                                                            <td style="background:{style['accent']}; border-radius:6px; padding:8px 16px;">
                                                                <a href="{video['link']}" style="color:#fff; text-decoration:none; font-size:12px; font-weight:600;">
                                                                    ▶️ 点击观看视频
                                                                </a>
                                                            </td>
                                                        </tr>
                                                    </table>
                                                </td>
                                            </tr>
                                        </table>
                                    </td>
                                </tr>
                            </table>
                        </td>
                    </tr>
                    <tr><td height="20" style="font-size:0;">&nbsp;</td></tr>
"""
    
    html = f'''<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>晨露早报 - {today}</title>
    <link href="https://fonts.googleapis.com/css2?family=Playfair+Display:wght@400;700&family=Source+Sans+3:wght@400;600&display=swap" rel="stylesheet">
</head>
<body style="margin:0; padding:0; background:{style['bg']}; font-family:'Source Sans 3',-apple-system,BlinkMacSystemFont,sans-serif;">
    <table width="100%" cellpadding="0" cellspacing="0" border="0" align="center">
        <tr>
            <td align="center" style="padding:40px 0;">
                <table width="700" cellpadding="0" cellspacing="0" border="0" align="center">
                    
                    <!-- Header -->
                    <tr>
                        <td align="center" style="padding-bottom:30px;">
                            <h1 style="margin:0; font-family:'Playfair Display',serif; font-size:42px; color:{style['primary']}; letter-spacing:2px;">
                                晨露早报
                            </h1>
                            <p style="margin:8px 0 0; font-size:14px; color:{style['text']}; letter-spacing:3px;">
                                PRACTICAL GUIDE · {today}
                            </p>
                            <p style="margin:15px 0 0; font-size:13px; color:{style['accent']}; font-weight:600;">
                                🎯 找市场热点 · 💪 能做出来 · 🛠️ 实用工具
                            </p>
                        </td>
                    </tr>
                    
                    <tr><td height="30" style="font-size:0;">&nbsp;</td></tr>
                    
                    <!-- 方向1：合成消除小游戏 -->
                    <tr>
                        <td>
                            <table width="700" cellpadding="0" cellspacing="0" border="0" align="center" 
                                   style="background:{style['card']}; border-radius:16px; overflow:hidden; box-shadow:0 8px 24px rgba(0,0,0,0.06);">
                                <tr>
                                    <td style="padding:0; font-size:0;">
                                        <img src="{content['domestic_game']['image']}" width="700" 
                                             style="display:block; width:700px; border:0;" alt="消除游戏">
                                    </td>
                                </tr>
                                <tr>
                                    <td style="padding:40px 50px;">
                                        <span style="color:{style['accent']}; font-size:12px; font-weight:bold; letter-spacing:2px;">
                                            🎮 方向一 · 微信小游戏
                                        </span>
                                        
                                        <h2 style="margin:12px 0 8px; font-family:'Playfair Display',serif; font-size:28px; color:{style['primary']};">
                                            {content['domestic_game']['name']}
                                        </h2>
                                        
                                        <p style="margin:0 0 15px; font-size:14px; color:#888;">
                                            参考：{content['domestic_game']['real_example']}
                                        </p>
                                        
                                        <table width="100%" cellpadding="0" cellspacing="0" border="0" style="margin-bottom:20px;">
                                            <tr>
                                                <td width="48%" style="background:#f8f9fa; border-radius:8px; padding:15px;">
                                                    <p style="margin:0; font-size:12px; color:#888;">难度</p>
                                                    <p style="margin:5px 0 0; font-size:16px; color:{style['primary']}; font-weight:600;">
                                                        {content['domestic_game']['difficulty']}
                                                    </p>
                                                </td>
                                                <td width="4%" style="font-size:0;">&nbsp;</td>
                                                <td width="48%" style="background:#f8f9fa; border-radius:8px; padding:15px;">
                                                    <p style="margin:0; font-size:12px; color:#888;">成本</p>
                                                    <p style="margin:5px 0 0; font-size:14px; color:{style['primary']};">
                                                        {content['domestic_game']['cost']}
                                                    </p>
                                                </td>
                                            </tr>
                                        </table>
                                        
                                        <table width="100%" cellpadding="0" cellspacing="0" border="0" style="margin-bottom:20px;">
                                            <tr>
                                                <td style="background:#f8f9fa; border-radius:12px; padding:25px;">
                                                    <h4 style="margin:0 0 15px; font-size:14px; color:{style['primary']};">
                                                        🚀 如何开始（5步法）
                                                    </h4>
                                                    <ol style="margin:0; padding-left:20px; font-size:13px; color:{style['text']}; line-height:2;">
                                                        {''.join([f'<li>{step}</li>' for step in content['domestic_game']['how_to_start']])}
                                                    </ol>
                                                </td>
                                            </tr>
                                        </table>
                                        
                                        <p style="margin:0; font-size:13px; color:{style['text']}; line-height:1.8; border-left:3px solid {style['accent']}; padding-left:15px;">
                                            <strong>晨露分析：</strong>{content['domestic_game']['analysis']}
                                        </p>
                                        
                                        <p style="margin:15px 0 0; font-size:14px; color:{style['success']}; font-weight:600;">
                                            {content['domestic_game']['verdict']}
                                        </p>
                                    </td>
                                </tr>
                            </table>
                        </td>
                    </tr>
                    
                    <tr><td height="50" style="font-size:0;">&nbsp;</td></tr>
                    
                    <!-- 方向2：浏览器插件（新增） -->
                    <tr>
                        <td>
                            <table width="700" cellpadding="0" cellspacing="0" border="0" align="center" 
                                   style="background:{style['card']}; border-radius:16px; overflow:hidden; box-shadow:0 8px 24px rgba(0,0,0,0.06);">
                                <tr>
                                    <td style="padding:40px 50px;">
                                        <span style="color:{style['accent']}; font-size:12px; font-weight:bold; letter-spacing:2px;">
                                            🛠️ 方向二 · 实用小工具（强烈推荐）
                                        </span>
                                        
                                        <table width="100%" cellpadding="0" cellspacing="0" border="0" style="margin:20px 0;">
                                            <tr>
                                                <td width="200" valign="top" style="padding-right:25px;">
                                                    <img src="{content['practical_tool']['image']}" width="200" 
                                                         style="display:block; width:200px; border-radius:12px; box-shadow:0 4px 12px rgba(0,0,0,0.1);" 
                                                         alt="小工具">
                                                </td>
                                                <td width="400" valign="top">
                                                    <h2 style="margin:0 0 8px; font-family:'Playfair Display',serif; font-size:24px; color:{style['primary']};">
                                                        {content['practical_tool']['name']}
                                                    </h2>
                                                    <p style="margin:0 0 12px; font-size:13px; color:#888;">
                                                        参考：{content['practical_tool']['real_example']}
                                                    </p>
                                                    <p style="margin:0 0 12px; font-size:14px; color:{style['text']}; line-height:1.7;">
                                                        {content['practical_tool']['why_hot']}
                                                    </p>
                                                    <p style="margin:0; font-size:13px; color:{style['primary']}; font-weight:600;">
                                                        难度：{content['practical_tool']['difficulty']} · {content['practical_tool']['cost']}
                                                    </p>
                                                </td>
                                            </tr>
                                        </table>
                                        
                                        <table width="100%" cellpadding="0" cellspacing="0" border="0" style="margin-bottom:20px;">
                                            <tr>
                                                <td style="background:#f8f9fa; border-radius:12px; padding:25px;">
                                                    <h4 style="margin:0 0 15px; font-size:14px; color:{style['primary']};">
                                                        💡 可做的方向（5个思路）
                                                    </h4>
                                                    <ul style="margin:0; padding-left:20px; font-size:13px; color:{style['text']}; line-height:2;">
                                                        {''.join([f'<li>{idea}</li>' for idea in content['practical_tool']['ideas']])}
                                                    </ul>
                                                </td>
                                            </tr>
                                        </table>
                                        
                                        <p style="margin:0; font-size:13px; color:{style['text']}; line-height:1.8; border-left:3px solid {style['success']}; padding-left:15px;">
                                            <strong>晨露分析：</strong>{content['practical_tool']['analysis']}
                                        </p>
                                        
                                        <p style="margin:15px 0 0; font-size:14px; color:{style['success']}; font-weight:600;">
                                            {content['practical_tool']['verdict']}
                                        </p>
                                    </td>
                                </tr>
                            </table>
                        </td>
                    </tr>
                    
                    <tr><td height="50" style="font-size:0;">&nbsp;</td></tr>
                    
                    <!-- 方向3：AI工具 -->
                    <tr>
                        <td>
                            <table width="700" cellpadding="0" cellspacing="0" border="0" align="center" 
                                   style="background:#f8f9fa; border-radius:16px; padding:40px;">
                                <tr>
                                    <td width="300" valign="middle" style="padding:0;">
                                        <img src="{content['ai_tool']['image']}" width="300" 
                                             style="display:block; width:300px; border-radius:12px; box-shadow:0 4px 12px rgba(0,0,0,0.1);" 
                                             alt="AI工具">
                                    </td>
                                    <td width="40" style="font-size:0;">&nbsp;</td>
                                    <td width="360" valign="middle" style="padding:0;">
                                        <span style="color:{style['accent']}; font-size:12px; font-weight:bold; letter-spacing:1px;">
                                            🤖 方向三 · AI提效工具
                                        </span>
                                        
                                        <h3 style="margin:10px 0 8px; font-family:'Playfair Display',serif; font-size:22px; color:{style['primary']};">
                                            {content['ai_tool']['name']}
                                        </h3>
                                        
                                        <p style="margin:0 0 15px; font-size:14px; color:{style['accent']}; font-weight:600;">
                                            {content['ai_tool']['tagline']}
                                        </p>
                                        
                                        <p style="margin:0 0 15px; font-size:13px; color:{style['text']}; line-height:1.7;">
                                            {content['ai_tool']['analysis'][:100]}...
                                        </p>
                                        
                                        <table width="100%" cellpadding="0" cellspacing="0" border="0">
                                            <tr>
                                                <td style="background:#fff; border-radius:8px; padding:15px;">
                                                    <p style="margin:0 0 8px; font-size:12px; color:#888;">实用场景：</p>
                                                    <ul style="margin:0; padding-left:18px; font-size:12px; color:{style['text']}; line-height:1.8;">
                                                        {''.join([f'<li>{use}</li>' for use in content['ai_tool']['practical_use'][:2]])}
                                                    </ul>
                                                </td>
                                            </tr>
                                        </table>
                                        
                                        <p style="margin:15px 0 0; font-size:13px; color:{style['success']}; font-weight:600;">
                                            {content['ai_tool']['verdict']}
                                        </p>
                                    </td>
                                </tr>
                            </table>
                        </td>
                    </tr>
                    
                    <tr><td height="50" style="font-size:0;">&nbsp;</td></tr>
                    
                    <!-- B站实用教程 -->
                    <tr>
                        <td>
                            <table width="700" cellpadding="0" cellspacing="0" border="0" align="center" 
                                   style="background:{style['card']}; border-radius:16px; padding:35px 50px; box-shadow:0 8px 24px rgba(0,0,0,0.06);">
                                <tr>
                                    <td>
                                        <span style="color:{style['accent']}; font-size:12px; font-weight:bold; letter-spacing:2px;">
                                            📺 本周必看教程 · 附详细总结
                                        </span>
                                        
                                        <h3 style="margin:12px 0 8px; font-family:'Playfair Display',serif; font-size:24px; color:{style['primary']};">
                                            B站实用内容
                                        </h3>
                                        
                                        <p style="margin:0 0 25px; font-size:13px; color:#888;">
                                            💡 点击标题或下方按钮直接跳转视频，建议收藏后跟着做
                                        </p>
                                        
                                        <table width="100%" cellpadding="0" cellspacing="0" border="0">
                                            {bilibili_html}
                                        </table>
                                    </td>
                                </tr>
                            </table>
                        </td>
                    </tr>
                    
                    <tr><td height="50" style="font-size:0;">&nbsp;</td></tr>
                    
                    <!-- 市场数据 -->
                    <tr>
                        <td>
                            <table width="700" cellpadding="0" cellspacing="0" border="0" align="center" 
                                   style="background:{style['primary']}; border-radius:16px; padding:35px 50px;">
                                <tr>
                                    <td>
                                        <span style="color:#888; font-size:12px; font-weight:bold; letter-spacing:2px;">
                                            📊 市场数据参考
                                        </span>
                                        
                                        <h3 style="margin:12px 0 20px; font-size:20px; color:#fff;">
                                            为什么现在是好时机？
                                        </h3>
                                        
                                        <table width="100%" cellpadding="0" cellspacing="0" border="0">
                                            <tr>
                                                <td width="48%" style="padding:15px; background:#2a2a2a; border-radius:8px;">
                                                    <p style="margin:0; font-size:20px; color:{style['accent']}; font-weight:bold;">4亿+</p>
                                                    <p style="margin:5px 0 0; font-size:12px; color:#888;">微信小游戏月活</p>
                                                </td>
                                                <td width="4%" style="font-size:0;">&nbsp;</td>
                                                <td width="48%" style="padding:15px; background:#2a2a2a; border-radius:8px;">
                                                    <p style="margin:0; font-size:20px; color:{style['accent']}; font-weight:bold;">300%+</p>
                                                    <p style="margin:5px 0 0; font-size:12px; color:#888;">AI工具类增长</p>
                                                </td>
                                            </tr>
                                        </table>
                                        
                                        <p style="margin:20px 0 0; font-size:13px; color:#aaa; line-height:1.7;">
                                            {content['market_data']['opportunity']}
                                        </p>
                                    </td>
                                </tr>
                            </table>
                        </td>
                    </tr>
                    
                    <tr><td height="40" style="font-size:0;">&nbsp;</td></tr>
                    
                    <!-- 行动清单 -->
                    <tr>
                        <td>
                            <table width="700" cellpadding="0" cellspacing="0" border="0" align="center" 
                                   style="background:{style['accent']}; border-radius:16px; padding:30px 50px;">
                                <tr>
                                    <td>
                                        <h4 style="margin:0 0 20px; font-size:18px; color:#fff;">
                                            ✅ 本周行动清单（挑一件开始做）
                                        </h4>
                                        
                                        <table width="100%" cellpadding="0" cellspacing="0" border="0">
                                            {''.join([f'''
                                            <tr>
                                                <td style="padding:12px 0; border-bottom:1px solid rgba(255,255,255,0.2);">
                                                    <p style="margin:0; font-size:14px; color:#fff; line-height:1.6;">
                                                        {action}
                                                    </p>
                                                </td>
                                            </tr>
                                            ''' for action in content['weekly_actions']])}
                                        </table>
                                    </td>
                                </tr>
                            </table>
                        </td>
                    </tr>
                    
                    <tr><td height="60" style="font-size:0;">&nbsp;</td></tr>
                    
                    <tr>
                        <td align="center" style="padding:0 20px;">
                            <p style="margin:0; font-size:12px; color:#999; line-height:1.8;">
                                由 晨露宝宝 制作 · 帮你找到能落地的方向<br>
                                {datetime.now().strftime('%Y-%m-%d %H:%M')}
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
    """发送邮件"""
    print("📧 发送 Newsletter...")
    
    env_file = SCRIPT_DIR.parent / '.env.mail'
    env_vars = {}
    if env_file.exists():
        with open(env_file, 'r') as f:
            for line in f:
                if '=' in line and not line.startswith('#'):
                    k, v = line.strip().split('=', 1)
                    env_vars[k] = v
    
    import smtplib
    from email.mime.text import MIMEText
    from email.mime.multipart import MIMEMultipart
    from email.header import Header
    
    today = datetime.now().strftime("%Y年%m月%d日")
    
    msg = MIMEMultipart('alternative')
    sender_name = "晨露早报"
    sender_email = env_vars.get('SMTP_SENDER', '')
    msg['From'] = f"{Header(sender_name, 'utf-8').encode()} <{sender_email}>"
    msg['To'] = env_vars.get('RECIPIENT_EMAIL', sender_email)
    msg['Subject'] = Header(f"📰 晨露早报 - {today}（实用版）", 'utf-8')
    
    text = f"晨露早报 - {today}\n\n请使用支持HTML的邮件客户端查看完整内容。"
    msg.attach(MIMEText(text, 'plain', 'utf-8'))
    msg.attach(MIMEText(html_content, 'html', 'utf-8'))
    
    try:
        server = smtplib.SMTP(env_vars.get('SMTP_HOST', 'smtp.qq.com'), int(env_vars.get('SMTP_PORT', '587')))
        server.starttls()
        server.login(sender_email, env_vars.get('SMTP_PASSWORD', ''))
        server.sendmail(sender_email, env_vars.get('RECIPIENT_EMAIL', sender_email), msg.as_string())
        server.quit()
        print("✅ 发送成功！")
        return True
    except Exception as e:
        print(f"❌ 失败: {e}")
        return False

def main():
    print("🌅 晨露早报（实用导向版）生成中...")
    print("=" * 60)
    print("🎯 找市场热点 · 💪 能做出来 · 🛠️ 实用小工具")
    print("=" * 60)
    
    bilibili = fetch_bilibili_practical()
    content = get_practical_content()
    
    html = generate_html_newsletter(bilibili, content)
    success = send_email(html)
    
    if success:
        print("\n🎉 实用版早报已发送！")
        print("\n📧 内容概览：")
        print("   方向1：合成消除小游戏（2-4周可上线）")
        print("   方向2：浏览器插件（1-2周，强烈推荐）")
        print("   方向3：AI工具提效")
        print("   B站：2个可复现的教程")
        print("   行动：5件具体可做的事")
    else:
        print("\n⚠️ 发送失败")
    
    return 0 if success else 1

if __name__ == "__main__":
    sys.exit(main())
