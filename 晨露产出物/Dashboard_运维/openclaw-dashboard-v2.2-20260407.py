#!/usr/bin/env python3
"""
OpenClaw Bot 监控看板 - 赛博朋克霓虹风格 v2.1
紧凑布局 + 统一任务面板 + 移动端优化
"""

import http.server
import socketserver
import json
import subprocess
import os
from datetime import datetime

PORT = 8080

BOTS = {
    'sunny': {
        'name': 'SUNNY',
        'emoji': '☀️',
        'neon_color': '#00f5ff',
        'port': 18780,
        'service': 'openclaw-gateway-bot2.service',
        'desc': 'Chief of Staff',
        'model': 'Gemini',
        'output_dir': '/home/cheche/Sunny产出物',
        'name_cn': 'Sunny',
        'persona': 'Chief of Staff'
    },
    'rainbow': {
        'name': 'RAINBOW',
        'emoji': '🌈',
        'neon_color': '#9d00ff',
        'port': 18790,
        'service': 'openclaw-gateway-rainbow.service',
        'desc': 'Brand Architect',
        'model': 'Gemini',
        'output_dir': '/home/cheche/rainbow产出物',
        'name_cn': 'Rainbow',
        'persona': 'Brand Architect'
    },
    'main': {
        'name': 'CHENLU',
        'emoji': '☁️',
        'neon_color': '#4488ff',
        'port': 18794,
        'service': 'openclaw-gateway-main.service',
        'desc': 'Product Engineer',
        'model': 'Kimi',
        'output_dir': '/home/cheche/晨露产出物',
        'name_cn': '晨露',
        'persona': 'Product Engineer'
    },
    'mumu': {
        'name': 'MUMU',
        'emoji': '🍁',
        'neon_color': '#ff8844',
        'port': 18795,
        'service': 'openclaw-gateway-mumu.service',
        'desc': 'Solutions Strategist',
        'model': 'Kimi',
        'output_dir': '/home/cheche/.openclaw/workspace-mumu/沐木产出物',
        'name_cn': '沐木',
        'persona': 'Solutions Strategist'
    },
    'melody': {
        'name': 'MELODY',
        'emoji': '🎧',
        'neon_color': '#ff00ff',
        'port': 18810,
        'service': 'openclaw-gateway-melody.service',
        'desc': 'Creative Director',
        'model': 'Kimi',
        'output_dir': '/home/cheche/.openclaw/workspace-melody/melody产出物',
        'name_cn': 'Melody',
        'persona': 'Creative Director'
    },
    'sean': {
        'name': 'SEAN',
        'emoji': '🪐',
        'neon_color': '#ff4444',
        'port': 18820,
        'service': 'openclaw-gateway-baby.service',
        'desc': 'Emotional Wellness',
        'model': 'GPT',
        'output_dir': '/home/cheche/.openclaw/workspace-baby/Sean产出物',
        'name_cn': 'Sean',
        'persona': 'Emotional Wellness Consultant'
    }
}


def run_command(cmd):
    try:
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=10)
        return result.stdout.strip(), result.returncode
    except:
        return '', -1


def get_bot_status(bot_id, bot_info):
    port_out, _ = run_command(f"ss -tlnp 2>/dev/null | grep ':{bot_info['port']} '")
    online = bool(port_out)
    
    # 获取内存使用
    mem = '--'
    if online:
        pid_out, _ = run_command(f"ss -tlnp 2>/dev/null | grep ':{bot_info['port']} ' | grep -o 'pid=[0-9]*' | cut -d'=' -f2")
        if pid_out:
            try:
                pid = pid_out.strip().split()[0]
                mem_out, _ = run_command(f"ps -p {pid} -o rss= 2>/dev/null")
                if mem_out:
                    mem_kb = int(mem_out.strip())
                    mem = f"{mem_kb // 1024}MB"
            except:
                pass
    
    return {'online': online, 'mem': mem}


def get_output_files(bot_id):
    """获取产出物文件夹中最新的3个文件，智能去重"""
    bot_info = BOTS.get(bot_id)
    if not bot_info:
        return []
    
    output_dir = bot_info['output_dir']
    if not os.path.exists(output_dir):
        return []
    
    files = []
    
    # 遍历产出物文件夹
    for root, dirs, filenames in os.walk(output_dir):
        # 跳过隐藏目录
        dirs[:] = [d for d in dirs if not d.startswith('.')]
        
        for filename in filenames:
            # 跳过隐藏文件
            if filename.startswith('.'):
                continue
                
            filepath = os.path.join(root, filename)
            try:
                stat = os.stat(filepath)
                files.append({
                    'name': filename,
                    'path': filepath,
                    'time': datetime.fromtimestamp(stat.st_mtime).strftime('%m-%d %H:%M'),
                    'timestamp': stat.st_mtime
                })
            except:
                pass
    
    # 按时间排序，最新的在前
    files.sort(key=lambda x: x['timestamp'], reverse=True)
    
    # 智能去重：提取基础文件名（去掉版本后缀），保留最新的
    version_keywords = ['最终版', '最新版', '美化版', '修改版', '完成版', 'v1', 'v2', 'v3', 'v4', 'v5', 
                       'final', 'latest', 'update', 'rev', '版本', 'version', 'copy', '副本', 
                       '（', '()', '[]', '_', '-']
    
    def get_base_name(filename):
        """提取基础文件名（去掉扩展名和版本后缀）"""
        name = os.path.splitext(filename)[0]
        # 按常见分隔符分割，取第一部分
        for sep in ['_v', '-v', '（', '(', '_', '-', ' ']:
            if sep in name:
                name = name.split(sep)[0]
        return name.lower().strip()
    
    # 按基础文件名分组，只保留每组最新的
    file_groups = {}
    for f in files:
        base = get_base_name(f['name'])
        if base not in file_groups:
            file_groups[base] = f
        elif f['timestamp'] > file_groups[base]['timestamp']:
            file_groups[base] = f
    
    # 返回最新的10个（按时间排序），用于面板统计
    result = list(file_groups.values())
    result.sort(key=lambda x: x['timestamp'], reverse=True)
    return result[:10]


def get_output_files_count(bot_id):
    """获取产出物真实总数（用于面板显示）"""
    bot_info = BOTS.get(bot_id)
    if not bot_info:
        return 0
    
    output_dir = bot_info['output_dir']
    if not os.path.exists(output_dir):
        return 0
    
    count = 0
    for root, dirs, filenames in os.walk(output_dir):
        dirs[:] = [d for d in dirs if not d.startswith('.')]
        for filename in filenames:
            if not filename.startswith('.'):
                count += 1
    return count


def get_all_tasks():
    """任务显示：
    - 在线 Bot：显示角色相关的具体工作内容
    - 产出物：显示最近的文件作为已完成任务
    """
    all_tasks = []
    
    # 每个角色的默认"进行中"任务
    default_tasks = {
        'sunny': 'Daily newsletter & admin tasks',
        'rainbow': 'Weekly AI report & brand strategy',
        'main': 'Coding & product development',
        'mumu': 'Business proposals & solutions',
        'melody': 'UI design & visual creation',
        'sean': 'Emotional support & wellness'
    }
    
    for bot_id, bot_info in BOTS.items():
        bot_status = get_bot_status(bot_id, bot_info)
        files = get_output_files(bot_id)
        
        # 1. 如果在线，显示角色相关的具体任务
        if bot_status['online']:
            task_text = default_tasks.get(bot_id, 'Working')
            all_tasks.append({
                'status': 'active',
                'text': task_text,
                'bot': bot_id,
                'bot_name': bot_info['name'],
                'bot_color': bot_info['neon_color']
            })
        
        # 2. 读取最近的产出物文件名作为已完成任务（只取3个用于显示）
        for f in files[:3]:
            task_name = f['name'].replace('_', ' ').replace('-', ' ')
            task_name = os.path.splitext(task_name)[0]
            if len(task_name) > 30:
                task_name = task_name[:30] + '...'
            
            all_tasks.append({
                'status': 'completed',
                'text': f'Delivered: {task_name}',
                'bot': bot_id,
                'bot_name': bot_info['name'],
                'bot_color': bot_info['neon_color']
            })
    
    return all_tasks


def get_logs(bot_id):
    if bot_id == 'system':
        logs = []
        for bid, info in BOTS.items():
            out, _ = run_command(f"journalctl --user -u {info['service']} -n 5 --no-pager 2>&1 | tail -5")
            logs.append(f">>> {info['name']}\n{out}\n")
        return '\n'.join(logs)
    
    if bot_id not in BOTS:
        return 'ERROR'
    
    service = BOTS[bot_id]['service']
    out, _ = run_command(f"journalctl --user -u {service} -n 10 --no-pager 2>&1 | tail -10")
    return out


def restart_bot(bot_id):
    if bot_id == 'all':
        _, code = run_command('/home/cheche/bot-restart-safe.sh all')
        return code == 0, 'All bots restarted!' if code == 0 else 'Restart failed'
    
    if bot_id not in BOTS:
        return False, '找不到 Bot'
    
    _, code = run_command(f'/home/cheche/bot-restart-safe.sh {bot_id}')
    
    if code == 0:
        return True, f"{BOTS[bot_id]['name']} restarted!"
    else:
        return False, f"{BOTS[bot_id]['name']} restart failed"


class DashboardHandler(http.server.BaseHTTPRequestHandler):
    def log_message(self, format, *args):
        pass

    def do_GET(self):
        path = self.path
        
        if path == '/api/status':
            self.send_json({
                'bots': {k: get_bot_status(k, v) for k, v in BOTS.items()}
            })
            return
        
        if path == '/api/files':
            self.send_json({
                'files': {k: get_output_files(k) for k in BOTS.keys()}
            })
            return
        
        if path == '/api/tasks':
            self.send_json({'tasks': get_all_tasks()})
            return
        
        if path.startswith('/api/logs/'):
            bot_id = path.split('/')[-1]
            self.send_json({'logs': get_logs(bot_id)})
            return
        
        if path.startswith('/api/restart/'):
            bot_id = path.split('/')[-1]
            success, msg = restart_bot(bot_id)
            self.send_json({'success': success, 'message': msg})
            return
        
        self.send_html(self.generate_dashboard())

    def send_json(self, data):
        self.send_response(200)
        self.send_header('Content-Type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()
        self.wfile.write(json.dumps(data).encode())

    def send_html(self, html):
        self.send_response(200)
        self.send_header('Content-Type', 'text/html; charset=utf-8')
        self.end_headers()
        self.wfile.write(html.encode())

    def generate_dashboard(self):
        bots = {k: get_bot_status(k, v) for k, v in BOTS.items()}
        all_tasks = get_all_tasks()
        
        # 统计任务
        pending_count = sum(1 for t in all_tasks if t['status'] == 'pending')
        active_count = sum(1 for t in all_tasks if t['status'] == 'active')
        completed_count = sum(1 for t in all_tasks if t['status'] == 'completed')
        
        # 生成 Bot 卡片（紧凑版）
        cards_html = []
        for bid, bot in BOTS.items():
            s = bots[bid]
            status_class = 'online' if s['online'] else 'offline'
            files = get_output_files(bid)
            files_count = get_output_files_count(bid)  # 真实总数
            
            # 产出物 HTML（最多3个）
            files_html = ''
            for f in files[:3]:  # 只显示3个
                files_html += f'''
                <div class="file-item" onclick="copyPath('{f['path']}', '{f['name']}')">
                    <span class="file-icon">{self.get_file_icon(f['name'])}</span>
                    <span class="file-name">{f['name'][:20]}{'...' if len(f['name']) > 20 else ''}</span>
                    <span class="file-time">{f['time']}</span>
                </div>
                '''
            
            # 卡片信息区域 - 更宽松的布局
            status_text = 'Online' if s['online'] else 'Offline'
            info_html = f'''
                <div class="bot-info">
                    <!-- 第一行：头像 + 名字 + 操作按钮 -->
                    <div class="bot-header-row">
                        <div class="bot-avatar">{bot['emoji']}</div>
                        <div class="bot-titles">
                            <div class="bot-name">{bot['name']}</div>
                            <div class="bot-model-row">
                                <span class="model-tag">{bot['model']}</span>
                                <span class="status-pill {status_class}">● {status_text}</span>
                            </div>
                        </div>
                        <div class="bot-actions">
                            <button class="icon-btn restart" onclick="restartBot('{bid}', '{bot['name']}')" title="Restart">↻</button>
                            <button class="icon-btn logs" onclick="showLogs('{bid}', '{bot['name']}')" title="Logs">📋</button>
                        </div>
                    </div>
                    
                    <!-- 第二行：角色定位 -->
                    <div class="bot-persona">{bot.get('persona', '')}</div>
                    
                    <!-- 第三行：资源信息 -->
                    <div class="bot-stats-bar">
                        <div class="stat-box">
                            <span class="stat-label">💾 Memory</span>
                            <span class="stat-value" id="mem-{bid}">{s['mem']}</span>
                        </div>
                        <div class="stat-divider"></div>
                        <div class="stat-box">
                            <span class="stat-label">📦 Outputs</span>
                            <span class="stat-value">{files_count} 个</span>
                        </div>
                        <div class="stat-divider"></div>
                        <div class="stat-box">
                            <span class="stat-label">📝 Tasks</span>
                            <span class="stat-value">{files_count + (1 if s['online'] else 0)} 个</span>
                        </div>
                    </div>
                </div>
            '''
            
            card = f'''
            <div class="bot-card {bid}">
                <div class="card-main">
                    {info_html}
                </div>
                {f'<div class="file-list">{files_html}</div>' if files_html else '<div class="file-list empty"><div class="empty-text">暂无产出物</div></div>'}
            </div>
            '''
            cards_html.append(card)
        
        # 任务列表 HTML
        tasks_html = ''
        # 先显示进行中，再待办，最后已完成
        sorted_tasks = sorted(all_tasks, key=lambda x: {'active': 0, 'pending': 1, 'completed': 2}[x['status']])
        
        for task in sorted_tasks[:10]:  # 显示10个任务
            status_icon = {'active': '▶️', 'pending': '⏸️', 'completed': '✅'}[task['status']]
            status_class = task['status']
            tasks_html += f'''
            <div class="task-item {status_class}">
                <span class="task-icon">{status_icon}</span>
                <span class="task-bot" style="color:{task['bot_color']}">{task['bot_name']}</span>
                <span class="task-text">{task['text'][:40]}{'...' if len(task['text']) > 40 else ''}</span>
            </div>
            '''
        
        if not tasks_html:
            tasks_html = '<div class="task-item" style="opacity:0.5;text-align:center;padding:20px">No tasks</div>'
        
        return f'''<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
    <title>⚡ OPENCLAW</title>
    <link href="https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700;900&display=swap" rel="stylesheet">
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        
        :root {{
            --cyan: #00f5ff;
            --pink: #ff00ff;
            --purple: #9d00ff;
            --green: #00ff88;
            --orange: #ff8844;
            --red: #ff4444;
            --bg: #0a0a0f;
            --card: rgba(20, 20, 30, 0.9);
        }}
        
        body {{
            background: var(--bg);
            color: #fff;
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
            min-height: 100vh;
            padding: 15px;
            font-size: 14px;
        }}
        
        /* 移动端优先 */
        .container {{ max-width: 100%; margin: 0 auto; max-width: 1400px; }}
        
        /* 标题 */
        .header {{
            text-align: center;
            padding: 25px 20px;
            margin-bottom: 25px;
            border: 1px solid var(--cyan);
            background: linear-gradient(135deg, rgba(0,245,255,0.1), rgba(157,0,255,0.1));
            border-radius: 12px;
        }}
        
        .header h1 {{
            font-family: 'Orbitron', sans-serif;
            font-size: 20px;
            font-weight: 900;
            letter-spacing: 4px;
            background: linear-gradient(90deg, var(--cyan), var(--pink));
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
        }}
        
        .header-sub {{
            font-size: 10px;
            color: rgba(255,255,255,0.5);
            letter-spacing: 6px;
            margin-top: 5px;
        }}
        
        /* Bot 网格 - 移动端单列，桌面3列 */
        .bot-grid {{
            display: flex;
            flex-direction: column;
            gap: 10px;
            margin-bottom: 15px;
        }}
        
        .bot-card {{
            width: 100%;
        }}
        
        @media (min-width: 768px) {{
            .bot-grid {{ 
                display: grid;
                grid-template-columns: repeat(2, 1fr); 
                gap: 20px; 
            }}
            .header h1 {{ font-size: 28px; }}
            body {{ padding: 30px; }}
        }}
        
        @media (min-width: 1024px) {{
            .bot-grid {{ 
                grid-template-columns: repeat(3, 1fr); 
                gap: 25px; 
            }}
            .header h1 {{ font-size: 36px; }}
            body {{ padding: 40px; font-size: 16px; }}
        }}
        
        /* Bot 卡片 - 设计感 */
        .bot-card {{
            background: linear-gradient(145deg, rgba(25,25,35,0.95), rgba(15,15,25,0.95));
            border: 1px solid;
            border-radius: 16px;
            overflow: hidden;
            transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
            position: relative;
        }}
        
        .bot-card::before {{
            content: '';
            position: absolute;
            top: 0;
            left: -100%;
            width: 100%;
            height: 100%;
            background: linear-gradient(90deg, transparent, rgba(255,255,255,0.05), transparent);
            transition: left 0.6s;
        }}
        
        .bot-card:hover::before {{
            left: 100%;
        }}
        
        .bot-card:hover {{ 
            transform: translateY(-8px); 
            box-shadow: 0 25px 50px -12px rgba(0,0,0,0.5);
        }}
        
        .bot-card.sunny {{ border-color: var(--cyan); box-shadow: 0 0 0 1px var(--cyan), 0 4px 20px rgba(0,245,255,0.1); }}
        .bot-card.sunny:hover {{ box-shadow: 0 0 0 1px var(--cyan), 0 20px 60px rgba(0,245,255,0.25); }}
        .bot-card.rainbow {{ border-color: var(--purple); box-shadow: 0 0 0 1px var(--purple), 0 4px 20px rgba(157,0,255,0.1); }}
        .bot-card.rainbow:hover {{ box-shadow: 0 0 0 1px var(--purple), 0 20px 60px rgba(157,0,255,0.25); }}
        .bot-card.main {{ border-color: #4488ff; box-shadow: 0 0 0 1px #4488ff, 0 4px 20px rgba(68,136,255,0.1); }}
        .bot-card.main:hover {{ box-shadow: 0 0 0 1px #4488ff, 0 20px 60px rgba(68,136,255,0.25); }}
        .bot-card.mumu {{ border-color: var(--orange); box-shadow: 0 0 0 1px var(--orange), 0 4px 20px rgba(255,136,68,0.1); }}
        .bot-card.mumu:hover {{ box-shadow: 0 0 0 1px var(--orange), 0 20px 60px rgba(255,136,68,0.25); }}
        .bot-card.melody {{ border-color: var(--pink); box-shadow: 0 0 0 1px var(--pink), 0 4px 20px rgba(255,0,255,0.1); }}
        .bot-card.melody:hover {{ box-shadow: 0 0 0 1px var(--pink), 0 20px 60px rgba(255,0,255,0.25); }}
        .bot-card.sean {{ border-color: var(--red); box-shadow: 0 0 0 1px var(--red), 0 4px 20px rgba(255,68,68,0.1); }}
        .bot-card.sean:hover {{ box-shadow: 0 0 0 1px var(--red), 0 20px 60px rgba(255,68,68,0.25); }}
        
        .card-main {{
            padding: 16px;
        }}
        
        .bot-info {{
            display: flex;
            flex-direction: column;
            gap: 10px;
        }}
        
        .bot-header-row {{
            display: flex;
            align-items: center;
            gap: 10px;
        }}
        
        .bot-titles {{
            flex: 1;
            min-width: 0;
            display: flex;
            flex-direction: column;
            gap: 4px;
        }}
        
        .bot-model-row {{
            display: flex;
            align-items: center;
            gap: 8px;
            flex-wrap: wrap;
        }}
        
        .model-tag {{
            font-size: 10px;
            padding: 2px 8px;
            border-radius: 4px;
            background: rgba(255,255,255,0.1);
            color: rgba(255,255,255,0.7);
        }}
        
        .status-pill {{
            font-size: 11px;
            padding: 2px 8px;
            border-radius: 12px;
            font-weight: 500;
        }}
        
        .status-pill.online {{
            background: rgba(0,255,136,0.15);
            color: var(--green);
        }}
        
        .status-pill.offline {{
            background: rgba(255,68,68,0.15);
            color: var(--red);
        }}
        
        .bot-persona {{
            font-size: 12px;
            color: rgba(255,255,255,0.5);
            line-height: 1.4;
            padding: 6px 0;
            border-top: 1px solid rgba(255,255,255,0.05);
            border-bottom: 1px solid rgba(255,255,255,0.05);
        }}
        
        .bot-avatar {{
            width: 44px;
            height: 44px;
            border-radius: 12px;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 24px;
            background: rgba(0,0,0,0.4);
            border: 2px solid rgba(255,255,255,0.1);
            transition: all 0.3s;
        }}
        
        .bot-card:hover .bot-avatar {{
            transform: scale(1.1) rotate(5deg);
        }}
        
        .bot-card.sunny .bot-avatar {{ box-shadow: 0 0 15px rgba(0,245,255,0.3); }}
        .bot-card.rainbow .bot-avatar {{ box-shadow: 0 0 15px rgba(157,0,255,0.3); }}
        .bot-card.main .bot-avatar {{ box-shadow: 0 0 15px rgba(68,136,255,0.3); }}
        .bot-card.mumu .bot-avatar {{ box-shadow: 0 0 15px rgba(255,136,68,0.3); }}
        .bot-card.melody .bot-avatar {{ box-shadow: 0 0 15px rgba(255,0,255,0.3); }}
        .bot-card.sean .bot-avatar {{ box-shadow: 0 0 15px rgba(255,68,68,0.3); }}
        
        .bot-info {{ flex: 1; min-width: 0; }}
        
        .bot-name-row {{
            display: flex;
            align-items: center;
            gap: 6px;
            margin-bottom: 3px;
        }}
        
        .bot-name {{
            font-family: 'Orbitron', sans-serif;
            font-size: 16px;
            font-weight: 700;
            letter-spacing: 1px;
        }}
        
        .bot-card.sunny .bot-name {{ color: var(--cyan); }}
        .bot-card.rainbow .bot-name {{ color: var(--purple); }}
        .bot-card.main .bot-name {{ color: #66aaff; }}
        .bot-card.mumu .bot-name {{ color: var(--orange); }}
        .bot-card.melody .bot-name {{ color: var(--pink); }}
        .bot-card.sean .bot-name {{ color: var(--red); }}
        
        .bot-model {{
            font-size: 12px;
            color: rgba(255,255,255,0.4);
            margin-top: 3px;
        }}
        
        .status-badge {{
            padding: 4px 10px;
            border-radius: 20px;
            font-size: 11px;
            font-weight: 600;
            border: 1px solid;
        }}
        
        .status-badge.online {{
            background: rgba(0, 255, 136, 0.15);
            border-color: var(--green);
            color: var(--green);
        }}
        
        .status-badge.offline {{
            background: rgba(255, 68, 68, 0.15);
            border-color: var(--red);
            color: var(--red);
        }}
        
        .bot-stats-bar {{
            display: flex;
            align-items: center;
            justify-content: space-between;
            background: rgba(0,0,0,0.3);
            border-radius: 8px;
            padding: 10px 12px;
            margin-top: 2px;
        }}
        
        .stat-box {{
            display: flex;
            flex-direction: column;
            align-items: center;
            gap: 4px;
            flex: 1;
        }}
        
        .stat-divider {{
            width: 1px;
            height: 30px;
            background: rgba(255,255,255,0.1);
        }}
        
        .stat-label {{
            font-size: 10px;
            color: rgba(255,255,255,0.4);
            letter-spacing: 1px;
        }}
        
        .stat-value {{
            font-family: 'Orbitron', monospace;
            font-size: 14px;
            font-weight: 600;
            color: #fff;
        }}
        
        .status-dot {{
            width: 8px;
            height: 8px;
            border-radius: 50%;
        }}
        
        .status-dot.online {{
            background: var(--green);
            box-shadow: 0 0 10px var(--green);
            animation: pulse 2s infinite;
        }}
        
        .status-dot.offline {{
            background: var(--red);
        }}
        
        .file-list.empty {{
            padding: 20px;
            text-align: center;
        }}
        
        .empty-text {{
            font-size: 12px;
            color: rgba(255,255,255,0.3);
            font-style: italic;
        }}
        
        @keyframes pulse {{
            0%, 100% {{ opacity: 1; }}
            50% {{ opacity: 0.4; }}
        }}
        
        .bot-actions {{
            display: flex;
            gap: 5px;
        }}
        
        .icon-btn {{
            width: 38px;
            height: 38px;
            border: 1px solid rgba(255,255,255,0.2);
            background: rgba(0,0,0,0.3);
            color: #fff;
            border-radius: 8px;
            cursor: pointer;
            font-size: 16px;
            display: flex;
            align-items: center;
            justify-content: center;
            transition: all 0.2s;
        }}
        
        .icon-btn:hover {{ transform: scale(1.1); }}
        .icon-btn.restart:hover {{ border-color: var(--red); color: var(--red); }}
        .icon-btn.logs:hover {{ border-color: var(--cyan); color: var(--cyan); }}
        
        /* 文件列表 */
        .file-list {{
            border-top: 1px solid rgba(255,255,255,0.08);
            padding: 12px 16px;
            background: rgba(0,0,0,0.2);
        }}
        
        .file-item {{
            display: flex;
            align-items: center;
            gap: 10px;
            padding: 8px 0;
            cursor: pointer;
            transition: all 0.2s;
            font-size: 13px;
            border-radius: 6px;
        }}
        
        .file-item:hover {{
            background: rgba(255,255,255,0.05);
            padding: 10px 12px;
            margin: 0 -12px;
        }}
        
        .file-item:hover {{ opacity: 0.8; transform: translateX(3px); }}
        
        .file-icon {{ font-size: 14px; }}
        
        .file-name {{
            flex: 1;
            white-space: nowrap;
            overflow: hidden;
            text-overflow: ellipsis;
            color: rgba(255,255,255,0.9);
        }}
        
        .file-time {{
            font-size: 10px;
            color: rgba(255,255,255,0.4);
            white-space: nowrap;
        }}
        
        /* 任务面板 */
        .task-panel {{
            background: linear-gradient(145deg, rgba(25,25,35,0.95), rgba(15,15,25,0.95));
            border: 1px solid var(--cyan);
            border-radius: 20px;
            padding: 35px;
            box-shadow: 0 0 0 1px rgba(0,245,255,0.2), 0 20px 60px rgba(0,245,255,0.08);
            position: relative;
            overflow: hidden;
        }}
        
        .task-panel::before {{
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            right: 0;
            height: 1px;
            background: linear-gradient(90deg, transparent, var(--cyan), transparent);
        }}
        
        .task-header {{
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 20px;
            padding-bottom: 15px;
            border-bottom: 1px solid rgba(0,245,255,0.2);
        }}
        
        .task-title {{
            font-family: 'Orbitron', sans-serif;
            font-size: 20px;
            color: var(--cyan);
            letter-spacing: 2px;
        }}
        
        .task-stats {{
            display: flex;
            gap: 15px;
            font-size: 12px;
        }}
        
        .task-stat {{
            display: flex;
            align-items: center;
            gap: 4px;
        }}
        
        .task-stat-value {{
            font-weight: 700;
            font-family: 'Orbitron', sans-serif;
        }}
        
        .task-stat.active .task-stat-value {{ color: var(--cyan); }}
        .task-stat.pending .task-stat-value {{ color: #ffaa00; }}
        .task-stat.completed .task-stat-value {{ color: var(--green); }}
        
        .task-stat-label {{ color: rgba(255,255,255,0.5); }}
        
        /* 任务列表 */
        .task-list {{
            max-height: 350px;
            overflow-y: auto;
        }}
        
        .task-item {{
            display: flex;
            align-items: center;
            gap: 12px;
            padding: 14px;
            margin-bottom: 8px;
            background: rgba(0,0,0,0.3);
            border-radius: 8px;
            font-size: 14px;
        }}
        
        .task-item.active {{ border-left: 3px solid var(--cyan); }}
        .task-item.pending {{ border-left: 3px solid #ffaa00; }}
        .task-item.completed {{ border-left: 3px solid var(--green); opacity: 0.6; }}
        
        .task-icon {{ font-size: 14px; }}
        
        .task-bot {{
            font-size: 11px;
            font-weight: 600;
            white-space: nowrap;
            min-width: 60px;
        }}
        
        .task-text {{
            flex: 1;
            color: rgba(255,255,255,0.9);
            overflow: hidden;
            text-overflow: ellipsis;
            white-space: nowrap;
        }}
        
        /* Modal */
        .modal {{
            display: none;
            position: fixed;
            top: 0; left: 0; right: 0; bottom: 0;
            background: rgba(0,0,0,0.9);
            z-index: 2000;
            align-items: center;
            justify-content: center;
            padding: 20px;
        }}
        
        .modal.active {{ display: flex; }}
        
        .modal-box {{
            background: var(--card);
            border: 1px solid var(--cyan);
            border-radius: 12px;
            padding: 20px;
            max-width: 500px;
            width: 100%;
        }}
        
        .modal-title {{
            font-family: 'Orbitron', sans-serif;
            font-size: 18px;
            color: var(--cyan);
            margin-bottom: 15px;
        }}
        
        .modal-text {{ color: rgba(255,255,255,0.7); margin-bottom: 20px; font-size: 14px; }}
        
        .modal-actions {{
            display: flex;
            gap: 10px;
            justify-content: flex-end;
        }}
        
        .btn {{
            padding: 10px 20px;
            border: 1px solid;
            background: transparent;
            color: #fff;
            border-radius: 6px;
            cursor: pointer;
            font-size: 13px;
            transition: all 0.2s;
        }}
        
        .btn-cancel {{ border-color: rgba(255,255,255,0.3); }}
        .btn-cancel:hover {{ border-color: #fff; }}
        .btn-confirm {{ border-color: var(--red); color: var(--red); }}
        .btn-confirm:hover {{ background: var(--red); color: #fff; }}
        
        /* 路径显示框 */
        .path-box {{
            background: rgba(0,0,0,0.5);
            border: 1px solid rgba(0,245,255,0.3);
            padding: 12px;
            border-radius: 6px;
            font-family: monospace;
            font-size: 12px;
            word-break: break-all;
            color: var(--cyan);
            margin-bottom: 15px;
            user-select: all;
        }}
        
        .logs-content {{
            background: rgba(0,0,0,0.5);
            border: 1px solid rgba(0,245,255,0.2);
            padding: 15px;
            border-radius: 6px;
            font-family: monospace;
            font-size: 11px;
            color: var(--green);
            max-height: 300px;
            overflow-y: auto;
            white-space: pre-wrap;
            line-height: 1.6;
        }}
        
        /* Toast */
        .toast {{
            position: fixed;
            bottom: 20px;
            left: 50%;
            transform: translateX(-50%) translateY(100px);
            background: var(--card);
            border: 1px solid var(--green);
            color: var(--green);
            padding: 12px 24px;
            border-radius: 8px;
            font-size: 13px;
            z-index: 3000;
            transition: transform 0.3s;
            box-shadow: 0 10px 30px rgba(0,0,0,0.5);
        }}
        
        .toast.show {{ transform: translateX(-50%) translateY(0); }}
        .toast.error {{ border-color: var(--red); color: var(--red); }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>⚡ OPENCLAW</h1>
            <div class="header-sub">BOT COMMAND CENTER</div>
        </div>
        
        <div class="bot-grid">
            {''.join(cards_html)}
        </div>
        
        <div class="task-panel">
            <div class="task-header">
                <div class="task-title">🎯 TASKS</div>
                <div class="task-stats">
                    <div class="task-stat active">
                        <span class="task-stat-value">{active_count}</span>
                        <span class="task-stat-label">进行中</span>
                    </div>
                    <div class="task-stat pending">
                        <span class="task-stat-value">{pending_count}</span>
                        <span class="task-stat-label">待办</span>
                    </div>
                    <div class="task-stat completed">
                        <span class="task-stat-value">{completed_count}</span>
                        <span class="task-stat-label">已完成</span>
                    </div>
                </div>
            </div>
            <div class="task-list">
                {tasks_html}
            </div>
        </div>
    </div>
    
    <!-- 重启确认 Modal -->
    <div class="modal" id="restartModal">
        <div class="modal-box">
            <div class="modal-title">⚠️ Confirm Restart</div>
            <div class="modal-text">Restart <span id="restart-bot-name" style="color:var(--cyan);font-weight:bold"></span> ?</div>
            <div class="modal-actions">
                <button class="btn btn-cancel" onclick="closeModal('restartModal')">Cancel</button>
                <button class="btn btn-confirm" onclick="confirmRestart()">Confirm</button>
            </div>
        </div>
    </div>
    
    <!-- 路径复制 Modal -->
    <div class="modal" id="pathModal">
        <div class="modal-box">
            <div class="modal-title">📋 文件路径</div>
            <div class="path-box" id="path-content"></div>
            <div class="modal-text" style="font-size:12px">点击上方文本框即可全选复制，或使用 Ctrl+C</div>
            <div class="modal-actions">
                <button class="btn btn-cancel" onclick="closeModal('pathModal')">Close</button>
                <button class="btn btn-confirm" onclick="tryCopy()" style="border-color:var(--green);color:var(--green)">Copy</button>
            </div>
        </div>
    </div>
    
    <!-- 日志 Modal -->
    <div class="modal" id="logsModal">
        <div class="modal-box" style="max-width:600px">
            <div class="modal-title">📋 <span id="logs-bot-name"></span> Logs</div>
            <div class="logs-content" id="logs-content">加载中...</div>
            <div class="modal-actions">
                <button class="btn btn-cancel" onclick="closeModal('logsModal')">Close</button>
                <button class="btn btn-confirm" onclick="refreshLogs()" style="border-color:var(--cyan);color:var(--cyan)">Refresh</button>
            </div>
        </div>
    </div>
    
    <div class="toast" id="toast"></div>
    
    <script>
        let currentBot = null;
        let currentPath = '';
        
        function showToast(msg, isError) {{
            const t = document.getElementById('toast');
            t.textContent = msg;
            t.className = isError ? 'toast error' : 'toast';
            t.classList.add('show');
            setTimeout(() => t.classList.remove('show'), 3000);
        }}
        
        // 复制路径 - 显示 Modal
        function copyPath(path, name) {{
            currentPath = path;
            document.getElementById('path-content').textContent = path;
            document.getElementById('pathModal').classList.add('active');
            
            // 尝试自动选择文本
            setTimeout(() => {{
                const box = document.getElementById('path-content');
                const range = document.createRange();
                range.selectNodeContents(box);
                const sel = window.getSelection();
                sel.removeAllRanges();
                sel.addRange(range);
            }}, 100);
        }}
        
        // 尝试复制
        function tryCopy() {{
            const box = document.getElementById('path-content');
            
            // 方法1: Clipboard API
            if (navigator.clipboard && navigator.clipboard.writeText) {{
                navigator.clipboard.writeText(currentPath).then(() => {{
                    showToast('✅ Copied!');
                    closeModal('pathModal');
                }}).catch(() => {{
                    // 方法2: execCommand
                    fallbackCopy();
                }});
            }} else {{
                fallbackCopy();
            }}
        }}
        
        function fallbackCopy() {{
            const textarea = document.createElement('textarea');
            textarea.value = currentPath;
            textarea.style.position = 'fixed';
            textarea.style.opacity = '0';
            document.body.appendChild(textarea);
            textarea.select();
            
            try {{
                document.execCommand('copy');
                showToast('✅ Copied!');
                closeModal('pathModal');
            }} catch (e) {{
                showToast('❌ 复制失败，请手动选择复制', true);
            }}
            
            document.body.removeChild(textarea);
        }}
        
        // 重启相关
        function restartBot(id, name) {{
            currentBot = id;
            document.getElementById('restart-bot-name').textContent = name;
            document.getElementById('restartModal').classList.add('active');
        }}
        
        function confirmRestart() {{
            closeModal('restartModal');
            showToast('Restarting...');
            
            fetch('/api/restart/' + currentBot)
                .then(r => r.json())
                .then(data => {{
                    showToast(data.message, !data.success);
                    if (data.success) setTimeout(() => location.reload(), 2000);
                }})
                .catch(() => showToast('请求失败', true));
        }}
        
        // 日志相关
        function showLogs(id, name) {{
            currentBot = id;
            document.getElementById('logs-bot-name').textContent = name;
            document.getElementById('logs-content').textContent = '加载中...';
            document.getElementById('logsModal').classList.add('active');
            
            fetch('/api/logs/' + id)
                .then(r => r.json())
                .then(data => {{
                    document.getElementById('logs-content').textContent = data.logs || 'No logs';
                }})
                .catch(() => {{
                    document.getElementById('logs-content').textContent = '加载失败';
                }});
        }}
        
        function refreshLogs() {{
            document.getElementById('logs-content').textContent = 'Refreshing...';
            fetch('/api/logs/' + currentBot)
                .then(r => r.json())
                .then(data => {{
                    document.getElementById('logs-content').textContent = data.logs || 'No logs';
                }});
        }}
        
        function closeModal(id) {{
            document.getElementById(id).classList.remove('active');
        }}
        
        // 点击遮罩关闭
        document.querySelectorAll('.modal').forEach(m => {{
            m.addEventListener('click', function(e) {{
                if (e.target === this) this.classList.remove('active');
            }});
        }});
        
        // 定期刷新状态
        setInterval(() => {{
            fetch('/api/status')
                .then(r => r.json())
                .then(data => {{
                    for (const [id, status] of Object.entries(data.bots)) {{
                        const dot = document.querySelector('.bot-card.' + id + ' .status-dot');
                        if (dot) {{
                            dot.className = 'status-dot ' + (status.online ? 'online' : 'offline');
                        }}
                    }}
                }})
                .catch(() => {{}});
        }}, 3600000);  // 60分钟刷新一次
    </script>
</body>
</html>'''

    def get_file_icon(self, filename):
        ext = os.path.splitext(filename)[1].lower()
        icons = {
            '.html': '🌐', '.htm': '🌐',
            '.md': '📝', '.txt': '📝',
            '.py': '🐍', '.js': '⚡', '.sh': '⌨️',
            '.png': '🖼️', '.jpg': '🖼️', '.jpeg': '🖼️', '.gif': '🖼️', '.svg': '🖼️',
            '.zip': '📦', '.tar': '📦', '.gz': '📦',
            '.pdf': '📄', '.doc': '📄', '.docx': '📄',
            '.ppt': '📊', '.pptx': '📊',
        }
        return icons.get(ext, '📎')


class ThreadedHTTPServer(socketserver.ThreadingMixIn, socketserver.TCPServer):
    allow_reuse_address = True


if __name__ == '__main__':
    print(f"⚡ OpenClaw Dashboard v2.1 - http://0.0.0.0:{PORT}")
    with ThreadedHTTPServer(('0.0.0.0', PORT), DashboardHandler) as httpd:
        httpd.serve_forever()
