#!/usr/bin/env python3
"""
OpenClaw Bot 监控看板 - v5 浅色杂志风格
静态模板 + API 端点
"""

import http.server
import socketserver
import json
import subprocess
import os
import re
from datetime import datetime
import time

PORT = 8080

BOTS = {
    'sunny': {
        'name': 'CHARLES',
        'emoji': '🦊',
        'neon_color': '#00f5ff',
        'port': 18780,
        'service': 'openclaw-gateway-bot2.service',
        'desc': 'Chief of Staff',
        'model': 'Opus',
        'output_dir': '/home/cheche/.openclaw/workspace-sunny/sunny产出物',
        'name_cn': 'Charles',
        'persona': 'Chief of Staff'
    },
    'rainbow': {
        'name': 'ASIN',
        'emoji': '🥕',
        'neon_color': '#9d00ff',
        'port': 18790,
        'service': 'openclaw-gateway-rainbow.service',
        'desc': 'Brand Architect',
        'model': 'Gemini',
        'output_dir': '/home/cheche/.openclaw/workspace-rainbow/Rainbow产出物',
        'name_cn': 'Asin',
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
        'output_dir': '/home/cheche/.openclaw/workspace-chenlu/晨露产出物',
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
        'model': 'Gemini',
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
        'name_cn': 'Baby',
        'persona': 'Emotional Wellness Consultant'
    },
    'wanganyu': {
        'name': 'WANGANYU',
        'emoji': '🌸',
        'neon_color': '#ff6b9d',
        'port': 18830,
        'service': 'openclaw-gateway-wanganyu.service',
        'desc': 'Celebrity Companion',
        'model': 'GPT',
        'output_dir': '/home/cheche/.openclaw/workspace-wanganyu/wanganyu产出物',
        'name_cn': '王安宇',
        'persona': 'Celebrity Companion'
    },
    'wanganyu': {
        'name': 'WANGANYU',
        'emoji': '🌸',
        'neon_color': '#ff6b9d',
        'port': 18830,
        'service': 'openclaw-gateway-wanganyu.service',
        'desc': 'Celebrity Companion',
        'model': 'GPT',
        'output_dir': '/home/cheche/.openclaw/workspace-wanganyu/wanganyu产出物',
        'name_cn': '王安宇',
        'persona': 'Celebrity Companion'
    }
}


def run_command(cmd):
    try:
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=10)
        return result.stdout.strip(), result.returncode
    except:
        return '', -1


# 简单的密码验证
DASHBOARD_PASSWORD = 'iloveyou'

def check_auth(handler):
    """检查请求是否通过密码验证"""
    auth_header = handler.headers.get('Authorization', '')
    if auth_header.startswith('Bearer '):
        token = auth_header[7:]
        if token == DASHBOARD_PASSWORD:
            return True
    return False


def get_bot_status(bot_id, bot_info):
    port_out, _ = run_command(f"ss -tlnp 2>/dev/null | grep ':{bot_info['port']} '")
    online = bool(port_out)
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
    bot_info = BOTS.get(bot_id)
    if not bot_info:
        return []
    output_dir = bot_info['output_dir']
    if not os.path.exists(output_dir):
        return []
    
    # 排除的目录名
    skip_dirs = {'node_modules', '.git', 'build', 'dist', 'out', 'target', '__pycache__', '.next', '.nuxt', 'vendor', 'libs', 'lib', 'src', 'source'}
    # 排除的文件扩展名（代码/配置/中间文件）
    skip_exts = {'.js', '.ts', '.jsx', '.tsx', '.css', '.scss', '.sass', '.less', '.json', '.yaml', '.yml', '.xml', '.map', '.npmignore', '.editorconfig', '.gitignore', '.dockerignore', '.eslintrc', '.prettierrc', '.babelrc'}
    # 排除的文件名前缀/关键词
    skip_prefixes = ['版本记录', '版本说明', '00-版本说明', 'readme', 'README', 'package-lock', 'yarn.lock', 'pnpm-lock', ' Gemfile', 'Cargo.lock', 'poetry.lock']
    # 只保留的"交付物"扩展名（白名单模式更严格）
    allow_exts = {'.html', '.htm', '.pdf', '.doc', '.docx', '.ppt', '.pptx', '.xls', '.xlsx', '.md', '.txt', '.png', '.jpg', '.jpeg', '.webp', '.gif', '.mp4', '.mp3', '.wav', '.zip', '.tar', '.gz', '.7z'}
    
    files = []
    for root, dirs, filenames in os.walk(output_dir):
        # 过滤目录
        dirs[:] = [d for d in dirs if not d.startswith('.') 
                   and d not in skip_dirs
                   and '日报' not in d and '周报' not in d]
        
        for filename in filenames:
            if filename.startswith('.'):
                continue
            if '日报' in filename or '周报' in filename:
                continue
            
            # 检查文件名前缀
            if any(filename.lower().startswith(s.lower()) for s in skip_prefixes):
                continue
            
            # 检查扩展名
            ext = os.path.splitext(filename)[1].lower()
            if ext in skip_exts:
                continue
            
            # 白名单：只统计交付物类型
            if ext not in allow_exts:
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
    
    files.sort(key=lambda x: x['timestamp'], reverse=True)
    
    # 按基础名称去重（同名系列按版本号保留最新的）
    import re
    def get_base_name(filename):
        """提取主题名（去除版本号、功能词后缀）"""
        name = os.path.splitext(filename)[0]
        
        # 1. 统一 slide 系列
        name = re.sub(r'slide\d+[_\-]', 'slide_', name, flags=re.IGNORECASE)
        
        # 2. 先去除末尾版本号标记 _v1.0 / V2.1 / -01 等
        #    （必须在去除功能词之前，因为版本号通常在功能词之后）
        name = re.sub(r'[_\-]v?\d+(\.\d+)?$', '', name, flags=re.IGNORECASE)
        name = re.sub(r'[（(]\d+[)）]$', '', name)
        
        # 3. 再去除常见功能词后缀（方案/计划/规划等）
        #    这些表示同一主题的不同文档类型，应视为同一系列
        func_words = ['方案', '计划', '规划', '设计稿', '清单', '记录', '勾选', '候选', '执行', '复盘', '总结', '进展']
        for word in func_words:
            if name.endswith(word):
                name = name[:-len(word)]
                break
        
        # 4. 去除其他分隔符后的内容（兜底）
        for sep in ['_v', '-v', '（', '(', '_', '-', ' ']:
            if sep in name:
                parts = name.split(sep)
                if parts[0].strip():
                    name = parts[0]
                    break
        
        return name.lower().strip()
    
    def get_version(filename):
        """提取版本号，用于比较大小"""
        name = os.path.splitext(filename)[0]
        # 匹配 v1.0 / V2.1 / _3 / -4 等版本号
        patterns = [
            r'[_\-]v?(\d+(?:\.\d+)*)$',  # _v1.0 / -2.1 / V3
            r'[（(](\d+(?:\.\d+)*)[)）]$',  # （1.0）/ (2)
        ]
        for pattern in patterns:
            match = re.search(pattern, name, re.IGNORECASE)
            if match:
                ver_str = match.group(1)
                # 转成可比较的格式：1.0 -> [1, 0], 2.1 -> [2, 1]
                parts = ver_str.split('.')
                try:
                    return [int(p) for p in parts]
                except:
                    continue
        # 如果没有版本号，返回空列表（表示最低优先级）
        return []
    
    def compare_versions(v1, v2):
        """比较版本号，返回较大的那个"""
        if not v1 and not v2:
            return 0  # 相同
        if not v1:
            return -1  # v2 更大
        if not v2:
            return 1   # v1 更大
        # 逐位比较
        for i in range(max(len(v1), len(v2))):
            n1 = v1[i] if i < len(v1) else 0
            n2 = v2[i] if i < len(v2) else 0
            if n1 > n2:
                return 1
            elif n1 < n2:
                return -1
        return 0  # 相同
    
    file_groups = {}
    for f in files:
        base = get_base_name(f['name'])
        ver = get_version(f['name'])
        
        if base not in file_groups:
            file_groups[base] = {'file': f, 'version': ver}
        else:
            # 比较版本号，保留版本号更大的
            cmp = compare_versions(ver, file_groups[base]['version'])
            if cmp > 0:
                file_groups[base] = {'file': f, 'version': ver}
            elif cmp == 0:
                # 版本号相同，按时间戳保留最新的
                if f['timestamp'] > file_groups[base]['file']['timestamp']:
                    file_groups[base] = {'file': f, 'version': ver}
    
    result = [g['file'] for g in file_groups.values()]
    result.sort(key=lambda x: x['timestamp'], reverse=True)
    return result[:10]


def get_output_files_count(bot_id):
    """统计产出物总数（包含日报周报，用于计数）"""
    bot_info = BOTS.get(bot_id)
    if not bot_info:
        return 0
    output_dir = bot_info['output_dir']
    if not os.path.exists(output_dir):
        return 0
    
    # 排除目录和文件扩展名（同 get_output_files）
    skip_dirs = {'node_modules', '.git', 'build', 'dist', 'out', 'target', '__pycache__', '.next', '.nuxt', 'vendor', 'libs', 'lib', 'src', 'source'}
    skip_exts = {'.js', '.ts', '.jsx', '.tsx', '.css', '.scss', '.sass', '.less', '.json', '.yaml', '.yml', '.xml', '.map', '.npmignore', '.editorconfig', '.gitignore', '.dockerignore', '.eslintrc', '.prettierrc', '.babelrc'}
    skip_prefixes = ['版本记录', '版本说明', '00-版本说明', 'readme', 'README', 'package-lock', 'yarn.lock', 'pnpm-lock']
    
    count = 0
    for root, dirs, filenames in os.walk(output_dir):
        dirs[:] = [d for d in dirs if not d.startswith('.') 
                   and d not in skip_dirs]
        for filename in filenames:
            if filename.startswith('.'):
                continue
            # 排除版本记录和 readme
            if any(filename.lower().startswith(s.lower()) for s in skip_prefixes):
                continue
            # 排除代码/配置文件
            ext = os.path.splitext(filename)[1].lower()
            if ext in skip_exts:
                continue
            count += 1
    return count


def get_all_tasks():
    all_tasks = []
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
        if bot_status['online']:
            task_text = default_tasks.get(bot_id, 'Working')
            all_tasks.append({
                'status': 'active',
                'text': task_text,
                'bot': bot_id,
                'bot_name': bot_info['name'],
                'bot_color': bot_info['neon_color']
            })
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
    return False, f"{BOTS[bot_id]['name']} restart failed"


def beautify_filename(filename):
    name = os.path.splitext(filename)[0]
    name = re.sub(r'[_\-]', ' ', name)
    name = re.sub(r'\s+', ' ', name).strip()
    if len(name) > 24:
        name = name[:24] + '...'
    return name


def get_file_tag(filename):
    ext = os.path.splitext(filename)[1].lower()
    tags = {
        '.html': 'HTML', '.css': 'CSS', '.js': 'JS',
        '.py': 'PY', '.sh': 'SH',
        '.md': 'MD', '.txt': 'TXT',
        '.png': 'IMG', '.jpg': 'IMG', '.jpeg': 'IMG', '.webp': 'IMG', '.gif': 'IMG',
        '.mp3': 'AUD', '.mp4': 'VID', '.wav': 'AUD',
        '.pdf': 'PDF', '.doc': 'DOC', '.docx': 'DOC',
        '.zip': 'ZIP', '.tar': 'ZIP', '.gz': 'ZIP'
    }
    return tags.get(ext, ext[1:].upper() if ext else 'FILE')


def get_file_icon(filename):
    ext = os.path.splitext(filename)[1].lower()
    icons = {
        '.html': '🌐', '.css': '🎨', '.js': '⚡',
        '.py': '🐍', '.sh': '📜',
        '.md': '📝', '.txt': '📄',
        '.png': '🖼️', '.jpg': '🖼️', '.jpeg': '🖼️', '.webp': '🖼️', '.gif': '🖼️',
        '.mp3': '🎵', '.mp4': '🎬', '.wav': '🎵',
        '.pdf': '📕', '.doc': '📘', '.docx': '📘',
        '.zip': '📦', '.tar': '📦', '.gz': '📦'
    }
    return icons.get(ext, '📎')


class DashboardHandler(http.server.BaseHTTPRequestHandler):

    def generate_recent_activity(self):
        bot_name_map = {
            'sunny': 'Charles',
            'rainbow': 'Asin',
            'main': '晨露',
            'mumu': '沐木',
            'melody': 'Melody',
            'sean': 'Baby',
            'wanganyu': '王安宇'
        }
        bot_color_map = {
            'sunny': 'charles',
            'rainbow': 'asin',
            'main': 'chenlu',
            'mumu': 'mumu',
            'melody': 'melody',
            'sean': 'sean'
        }
        all_activities = []
        for bot_id, bot_info in BOTS.items():
            files = get_output_files(bot_id)
            for f in files[:2]:
                all_activities.append({
                    'time': f['time'],
                    'bot': bot_name_map.get(bot_id, bot_info['name']),
                    'bot_css': bot_color_map.get(bot_id, bot_id),
                    'text': '产出物更新: ' + f['name'],
                    'timestamp': f['timestamp']
                })
        all_activities.sort(key=lambda x: x['timestamp'], reverse=True)
        all_activities = all_activities[:8]
        lines = []
        for act in all_activities:
            lines.append('        <div class="activity-item">')
            lines.append(f'          <div class="activity-time">{act["time"]}</div>')
            lines.append('          <div class="activity-content">')
            lines.append(f'            <div class="activity-bot {act["bot_css"]}">{act["bot"]}</div>')
            lines.append(f'            <div class="activity-text">{act["text"]}</div>')
            lines.append('          </div>')
            lines.append('        </div>')
        return '\n'.join(lines)

    def log_message(self, format, *args):
        pass

    def do_GET(self):
        path = self.path
        
        # 登录页面
        if path == '/login' or path == '/login/':
            self.send_response(200)
            self.send_header('Content-Type', 'text/html; charset=utf-8')
            self.end_headers()
            self.wfile.write(self.generate_login_page().encode('utf-8'))
            return
        
        # 验证认证状态（仅对首页 / 需要）
        is_authed = self.check_auth_header()
        if path == '/':
            if not is_authed:
                # 未认证 → 返回登录页面
                self.send_response(200)
                self.send_header('Content-Type', 'text/html; charset=utf-8')
                self.end_headers()
                self.wfile.write(self.generate_login_page().encode('utf-8'))
                return
            # 已认证 → 返回 Kimi SPA
            self.serve_static_file('/home/cheche/openclaw-final-v3', 'index.html')
            return
        
        # 静态文件 assets（Kimi 版 JS/CSS/字体）
        if path.startswith('/assets/'):
            relative_path = path[1:]
            self.serve_static_file('/home/cheche/openclaw-final-v3', relative_path)
            return
        
        # 头像图片
        if path.startswith('/images/'):
            self.serve_static_file('/home/cheche/openclaw-final-v3', path[1:])
            return
        
        # API 接口
        if path.startswith('/api/'):
            is_authed = self.check_auth_header()
            if not is_authed:
                self.send_response(401)
                self.send_header('Content-Type', 'application/json')
                self.send_header('WWW-Authenticate', 'Bearer')
                self.end_headers()
                self.wfile.write(json.dumps({'error': 'Unauthorized'}).encode())
                return
            # API 路由处理
            if path == '/api/status':
                self.send_json({'bots': {k: get_bot_status(k, v) for k, v in BOTS.items()}})
                return
            if path == '/api/files':
                self.send_json({'files': {k: get_output_files(k) for k in BOTS.keys()}})
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
            return
        
        # 旧版 Dashboard（保留但不再默认使用）
        if path == '/old':
            self.send_html_file('/home/cheche/dashboard-v5.html')
            return
        
        # 新版 React SPA 预览
        if path.startswith('/preview/'):
            relative_path = path[9:]
            self.serve_static_file('/home/cheche/dashboard-design-v8', relative_path)
            return
        
        # 404
        self.send_response(404)
        self.end_headers()
        self.wfile.write(b'Not Found')

    def check_auth_header(self):
        """检查请求头中的 Authorization 密码"""
        if not hasattr(self, 'PASSWORD'):
            self.PASSWORD = 'cheche'
        auth = self.headers.get('Authorization', '')
        if auth.startswith('Bearer '):
            return auth[7:] == self.PASSWORD
        return False

    def serve_static_file(self, base_dir, relative_path):
        """服务静态文件"""
        import mimetypes
        if not relative_path or relative_path.endswith('/'):
            relative_path = 'index.html'
        file_path = os.path.join(base_dir, relative_path)
        file_path = os.path.normpath(file_path)
        # 安全检查：确保在 base_dir 内
        if not file_path.startswith(os.path.normpath(base_dir)):
            self.send_response(403)
            self.end_headers()
            return
        if not os.path.exists(file_path) or not os.path.isfile(file_path):
            self.send_response(404)
            self.end_headers()
            self.wfile.write(b'Not Found')
            return
        self.send_response(200)
        content_type, _ = mimetypes.guess_type(file_path)
        if content_type:
            self.send_header('Content-Type', content_type)
        self.end_headers()
        with open(file_path, 'rb') as f:
            self.wfile.write(f.read())

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

    def send_html_file(self, file_path):
        """从文件发送 HTML"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                html = f.read()
            self.send_response(200)
            self.send_header('Content-Type', 'text/html; charset=utf-8')
            self.end_headers()
            self.wfile.write(html.encode())
        except Exception as e:
            self.send_response(500)
            self.end_headers()
            self.wfile.write(f'Error: {str(e)}'.encode())

    def get_file_icon(self, filename):
        return get_file_icon(filename)

    def get_system_stats(self):
        """采集真实系统资源数据（CPU / 内存 / 磁盘 / 网络）"""
        stats = {}

        # ---- CPU ----
        def read_cpu():
            with open('/proc/stat', 'r') as f:
                fields = list(map(int, f.readline().split()[1:]))
                return sum(fields), fields[3]  # total, idle
        t1, i1 = read_cpu()
        time.sleep(0.3)
        t2, i2 = read_cpu()
        stats['cpu'] = int(((t2 - t1) - (i2 - i1)) / (t2 - t1) * 100) if t2 != t1 else 0

        # ---- Memory ----
        meminfo = {}
        with open('/proc/meminfo', 'r') as f:
            for line in f:
                if ':' in line:
                    k, v = line.split(':')
                    meminfo[k.strip()] = int(v.strip().split()[0])
        total = meminfo.get('MemTotal', 1)
        avail = meminfo.get('MemAvailable', meminfo.get('MemFree', 0))
        stats['mem'] = int((total - avail) / total * 100)

        # ---- Disk ----
        st = os.statvfs('/')
        total_b = st.f_blocks * st.f_frsize
        free_b = st.f_bavail * st.f_frsize
        stats['disk'] = int((total_b - free_b) / total_b * 100)

        # ---- Network (活跃度，基于 0.3 秒采样) ----
        def read_net():
            with open('/proc/net/dev', 'r') as f:
                for line in f:
                    if ':' in line and not line.strip().startswith('lo'):
                        iface, data = line.split(':')
                        iface = iface.strip()
                        if iface.startswith(('eth', 'ens', 'enp', 'wlan', 'wlp')):
                            vals = list(map(int, data.split()))
                            return vals[0] + vals[8]  # rx + tx bytes
            return 0
        b1 = read_net()
        time.sleep(0.3)
        b2 = read_net()
        speed_mbps = (b2 - b1) * 8 / 0.3 / 1024 / 1024  # Mbps
        # 映射 0~100 Mbps → 0~100%
        stats['net'] = int(min(speed_mbps, 100))

        return stats

    def generate_login_page(self):
        """生成登录页面（纯密码框）"""
        return '''<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>登录 — OpenClaw Dashboard</title>
<style>
  * { margin: 0; padding: 0; box-sizing: border-box; }
  body {
    font-family: 'Inter', -apple-system, sans-serif;
    background: #000;
    color: #fff;
    min-height: 100vh;
    display: flex;
    align-items: center;
    justify-content: center;
    padding: 24px;
  }
  .container {
    width: 400px;
    max-width: 100%;
  }
  .login-box {
    background: #0a0a0a;
    border: 1px solid rgba(255,255,255,0.08);
    border-radius: 20px;
    padding: 48px 40px 40px;
    text-align: center;
  }
  .login-box h1 {
    font-size: 28px;
    font-weight: 700;
    background: linear-gradient(135deg, #ff6b9d, #c084fc, #818cf8);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    margin-bottom: 8px;
  }
  .login-box p {
    color: #71717a;
    font-size: 14px;
    margin-bottom: 32px;
  }
  .login-box input {
    width: 100%;
    padding: 14px 16px;
    background: #111;
    border: 1px solid rgba(255,255,255,0.1);
    border-radius: 12px;
    color: #fff;
    font-size: 15px;
    margin-bottom: 16px;
    outline: none;
    transition: all 0.2s;
  }
  .login-box input:focus {
    border-color: rgba(255,107,157,0.5);
    box-shadow: 0 0 0 3px rgba(255,107,157,0.1);
  }
  .login-box button {
    width: 100%;
    padding: 14px;
    background: linear-gradient(135deg, #ff6b9d, #c084fc);
    border: none;
    border-radius: 12px;
    color: #fff;
    font-size: 15px;
    font-weight: 600;
    cursor: pointer;
    transition: all 0.2s;
  }
  .login-box button:hover {
    transform: translateY(-1px);
    box-shadow: 0 4px 20px rgba(255,107,157,0.3);
  }
  .error {
    color: #fb7185;
    font-size: 13px;
    margin-top: 12px;
    display: none;
  }
</style>
</head>
<body>
  <div class="container">
    <div class="login-box">
      <h1>OpenClaw</h1>
      <p>System Dashboard</p>
      <input type="password" id="pwd" placeholder="输入访问密码" autofocus>
      <button onclick="login()">进入系统</button>
      <div class="error" id="error">密码错误</div>
    </div>
  </div>
  <script>
    function login() {
      const pwd = document.getElementById('pwd').value;
      fetch('/', {
        headers: { 'Authorization': 'Bearer ' + pwd }
      }).then(r => {
        if (r.ok) {
          localStorage.setItem('dashboard_auth', pwd);
          r.text().then(html => {
            document.open();
            document.write(html);
            document.close();
          });
        } else {
          document.getElementById('error').style.display = 'block';
        }
      }).catch(e => {
        document.getElementById('error').textContent = '\\u7f51\\u7edc\\u9519\\u8bef: ' + e.message;
        document.getElementById('error').style.display = 'block';
      });
    }
    document.getElementById('pwd').addEventListener('keypress', e => {
      if (e.key === 'Enter') login();
    });
    const saved = localStorage.getItem('dashboard_auth');
    if (saved) {
      fetch('/', { headers: { 'Authorization': 'Bearer ' + saved } })
        .then(r => {
          if (r.ok) {
            r.text().then(html => {
              document.open();
              document.write(html);
              document.close();
            });
          } else {
            localStorage.removeItem('dashboard_auth');
          }
        });
    }
  </script>
</body>
</html>'''

    def generate_dashboard(self):
        bots = {k: get_bot_status(k, v) for k, v in BOTS.items()}
        all_tasks = get_all_tasks()
        pending_count = sum(1 for t in all_tasks if t['status'] == 'pending')
        active_count = sum(1 for t in all_tasks if t['status'] == 'active')
        completed_count = sum(1 for t in all_tasks if t['status'] == 'completed')
        
        # 读取模板
        template_path = '/home/cheche/dashboard-v5.html'
        try:
            with open(template_path, 'r', encoding='utf-8') as f:
                html = f.read()
        except:
            return '<html><body>Error loading template</body></html>'
        
        # 替换 Baby 产出物（Baby = WangAnyu）
        baby_files = get_output_files('wanganyu')
        baby_files_html = ''
        for f in baby_files[:2]:
            baby_files_html += f'''<div class="file-item" onclick="copyPath('{f['path']}', '{f['name']}' )">
                <span class="file-icon">{self.get_file_icon(f['name'])}</span>
                <span class="file-name">{beautify_filename(f['name'])}</span>
                <span class="file-tag">{get_file_tag(f['name'])}</span>
            </div>'''
        
        # 替换模板中的占位符
        html = html.replace('{{BABY_FILES}}', baby_files_html)
        html = html.replace('{{BABY_COUNT}}', str(get_output_files_count('wanganyu')))

        
        # 生成真实的 Recent Activity
        recent_activity_html = self.generate_recent_activity()
        html = html.replace('{{RECENT_ACTIVITY}}', recent_activity_html)

        html = html.replace('{{ACTIVE_BOTS}}', str(sum(1 for b in bots.values() if b['online'])))
        html = html.replace('{{TASKS_TODAY}}', str(len(all_tasks)))
        html = html.replace('{{DELIVERABLES}}', str(sum(get_output_files_count(bid) for bid in BOTS)))
        
        # 替换各 Bot 的 Deliverables 数量
        html = html.replace('{{CHARLES_DELIVERABLES}}', str(get_output_files_count('sunny')))
        html = html.replace('{{ASIN_DELIVERABLES}}', str(get_output_files_count('rainbow')))
        html = html.replace('{{SEAN_DELIVERABLES}}', str(get_output_files_count('sean')))
        html = html.replace('{{MUMU_DELIVERABLES}}', str(get_output_files_count('mumu')))
        html = html.replace('{{MELODY_DELIVERABLES}}', str(get_output_files_count('melody')))
        html = html.replace('{{CHENLU_DELIVERABLES}}', str(get_output_files_count('main')))
        
        # 替换各 Bot 背面的文件列表
        for bot_id, placeholder in [
            ('sunny', 'CHARLES'),
            ('rainbow', 'ASIN'),
            ('sean', 'SEAN'),
            ('mumu', 'MUMU'),
            ('melody', 'MELODY'),
            ('main', 'CHENLU'),
        ]:
            files = get_output_files(bot_id)
            files_html = ''
            for f in files[:3]:  # 最多显示3个最新产出物
                files_html += f'''<a class="file-item" href="#">
              <span class="file-icon">{self.get_file_icon(f['name'])}</span>
              <div class="file-info">
                <div class="file-name">{beautify_filename(f['name'])}</div>
                <div class="file-path">{f['path']}</div>
              </div>
              <span class="file-tag">{get_file_tag(f['name'])}</span>
            </a>'''
            html = html.replace(f'{{{{{placeholder}_FILES}}}}', files_html)
        
        # 替换真实系统资源数据
        sys_stats = self.get_system_stats()
        html = html.replace('{{CPU_PCT}}', str(sys_stats['cpu']))
        html = html.replace('{{MEM_PCT}}', str(sys_stats['mem']))
        html = html.replace('{{DISK_PCT}}', str(sys_stats['disk']))
        html = html.replace('{{NET_PCT}}', str(sys_stats['net']))
        
        return html


class ThreadedHTTPServer(socketserver.ThreadingMixIn, socketserver.TCPServer):
    allow_reuse_address = True
    daemon_threads = True


def main():
    server = ThreadedHTTPServer(('', PORT), DashboardHandler)
    print(f"Dashboard v5 server running on port {PORT}")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        server.shutdown()


if __name__ == '__main__':
    main()
