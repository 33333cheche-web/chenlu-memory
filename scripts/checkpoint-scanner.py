#!/usr/bin/env python3
"""
断点续传扫描器 - 自动提取对话中的进行中任务
运行时间：每天 01:00（扫描最近 24 小时）
输出：memory/active-task-state.md
"""

import json
import os
import re
import glob
from datetime import datetime, timedelta
from pathlib import Path

# 配置
WORKSPACE = "/home/cheche/.openclaw/workspace-chenlu"
MEMORY_DIR = f"{WORKSPACE}/memory"
SESSIONS_DIR = os.path.expanduser("~/.openclaw-main/.openclaw/agents/main/sessions")
OUTPUT_FILE = f"{MEMORY_DIR}/active-task-state.md"

os.makedirs(MEMORY_DIR, exist_ok=True)

QUESTION_PAT = re.compile(r"(\?|？|请确认|请回复|你觉得|你认为|你怎么看|你选|你决定|是否|要不要)")
TASK_HINT_PAT = re.compile(r"(任务|工作|项目|方案|修改|推进|确认|回复|选择|安排|执行)")


def get_recent_sessions(hours=24):
    cutoff = datetime.now() - timedelta(hours=hours)
    sessions = []
    if not os.path.exists(SESSIONS_DIR):
        return sessions
    for jsonl_file in glob.glob(f"{SESSIONS_DIR}/*.jsonl"):
        mtime = datetime.fromtimestamp(os.path.getmtime(jsonl_file))
        if mtime > cutoff:
            sessions.append((jsonl_file, mtime))
    sessions.sort(key=lambda x: x[1], reverse=True)
    return sessions


def extract_task_signals(content):
    signals = {
        'in_progress': [],
        'pending_reply': [],
        'pending_action': [],
        'decisions': [],
        'blockers': []
    }

    patterns = {
        'in_progress': [
            r'(?:正在|进行中|还没完|做到一半|待完成|未完成).*?(?:任务|工作|项目|部署|配置|修改)',
            r'(?:下一步|接下来|然后|之后).*?(?:需要|要做|执行|推进)',
            r'(?:等|等待|pending|待).*?(?:确认|回复|批准|决定)',
        ],
        'pending_reply': [
            r'(?:你觉得|你认为|你怎么看|你的意见|你选哪个|你决定)',
            r'(?:请回复|请确认|请告知|请决定|请拍板)',
            r'(?:公主|宝|你).*?(?:觉得|认为|想|选|决定|确认)',
        ],
        'pending_action': [
            r'(?:我来|我去|我帮你|我处理|我安排|我准备)',
            r'(?:我去做|我去改|我去配|我去查|我去写)',
            r'(?:稍后|等下|马上|这就|立刻).*?(?:处理|执行|完成|搞定)',
        ],
        'blockers': [
            r'(?:卡住|阻塞|失败|报错|错误|异常|timeout|超时)',
            r'(?:不行|不对|有误|出问题|搞不定|失败)',
            r'(?:需要|等).*?(?:修复|解决|排查|调试)',
        ]
    }

    for category, pattern_list in patterns.items():
        for pattern in pattern_list:
            for match in re.finditer(pattern, content, re.IGNORECASE):
                start = max(0, match.start() - 50)
                end = min(len(content), match.end() + 50)
                context = content[start:end].strip()
                if len(context) > 10:
                    signals[category].append(context)

    for category in signals:
        signals[category] = list(dict.fromkeys(signals[category]))[:6]
    return signals


def parse_messages(session_file):
    msgs = []
    try:
        with open(session_file, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                try:
                    m = json.loads(line)
                except Exception:
                    continue
                role = m.get('role', '')
                if role not in ('user', 'assistant'):
                    continue
                content = m.get('content', '')
                if not isinstance(content, str):
                    continue
                ts = m.get('ts') or m.get('timestamp') or m.get('time')
                msgs.append({'role': role, 'content': content.strip(), 'ts': ts})
    except Exception:
        return []
    return msgs


def detect_unreplied_last_task_question(messages):
    """高优先级规则：最后一条 assistant 任务/确认型问句，且后续无 user 回复。"""
    if not messages:
        return None
    # 找最后一条 assistant
    idx = None
    for i in range(len(messages)-1, -1, -1):
        if messages[i]['role'] == 'assistant' and messages[i]['content']:
            idx = i
            break
    if idx is None:
        return None
    msg = messages[idx]['content']
    if len(msg) < 8:
        return None
    if not QUESTION_PAT.search(msg):
        return None
    if not TASK_HINT_PAT.search(msg):
        return None

    # 后续有没有 user 回复
    for j in range(idx+1, len(messages)):
        if messages[j]['role'] == 'user' and len(messages[j]['content']) > 0:
            return None

    short = msg.replace('\n', ' ')
    if len(short) > 120:
        short = short[:120] + '...'
    return f"[高优先级未回复] {short}"


def scan_sessions():
    sessions = get_recent_sessions(24)
    if not sessions:
        return None

    all_signals = {
        'in_progress': [],
        'pending_reply': [],
        'pending_action': [],
        'decisions': [],
        'blockers': []
    }

    for session_file, _ in sessions[:3]:
        messages = parse_messages(session_file)
        # 规则增强：最后问句未回复
        unreplied = detect_unreplied_last_task_question(messages)
        if unreplied:
            all_signals['pending_reply'].append(unreplied)

        for m in messages:
            content = m['content']
            if len(content) <= 20:
                continue
            sig = extract_task_signals(content)
            for k, items in sig.items():
                all_signals[k].extend(items)

    for category in all_signals:
        all_signals[category] = list(dict.fromkeys(all_signals[category]))[:10]
    return all_signals


def dedupe_pending_reply(items):
    """去重待回复：同一内容保留一条，优先保留[高优先级未回复]。"""
    chosen = {}
    for it in items:
        base = it.replace('[高优先级未回复] ', '').strip()
        prev = chosen.get(base)
        if prev is None:
            chosen[base] = it
        else:
            if it.startswith('[高优先级未回复]') and not prev.startswith('[高优先级未回复]'):
                chosen[base] = it
    return list(chosen.values())


def generate_task_state(signals):
    now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    d = datetime.now().strftime('%Y-%m-%d')

    # 输出前再做一次去重清洗
    signals['pending_reply'] = dedupe_pending_reply(signals.get('pending_reply', []))

    out = [
        f"# 断点状态 - {d}",
        "",
        f"> 自动生成于 {now} | 扫描最近 24 小时对话",
        "> 此文件由断点续传扫描器维护，请勿手动修改",
        "",
        "## 进行中任务",
    ]

    out += [f"{i}. {x}" for i, x in enumerate(signals['in_progress'], 1)] or ["_无明确进行中任务_"]

    out += ["", "## 待公主回复/确认"]
    out += [f"{i}. {x}" for i, x in enumerate(signals['pending_reply'], 1)] or ["_无待回复事项_"]

    out += ["", "## 待 Bot 执行"]
    out += [f"{i}. {x}" for i, x in enumerate(signals['pending_action'], 1)] or ["_无待执行事项_"]

    out += ["", "## 阻塞/问题"]
    out += [f"{i}. ⚠️ {x}" for i, x in enumerate(signals['blockers'], 1)] or ["_无阻塞事项_"]

    out += [
        "",
        "## 下一步建议",
        "- 优先处理：高优先级未回复 > 阻塞事项 > 待回复 > 待执行 > 进行中",
        "- 完成后更新此文件状态",
        "",
        "## 时间戳",
        f"- 保存时间：{now}",
        "- 扫描范围：最近 24 小时",
    ]
    return "\n".join(out) + "\n"


def main():
    print(f"[{datetime.now()}] 开始扫描断点任务...")
    signals = scan_sessions()
    if signals is None:
        print("未找到最近 24 小时的 session，写入空状态")
        signals = {'in_progress': [], 'pending_reply': [], 'pending_action': [], 'decisions': [], 'blockers': []}

    content = generate_task_state(signals)
    with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
        f.write(content)

    print(f"[{datetime.now()}] 已保存到 {OUTPUT_FILE}")
    print(f"  - 进行中: {len(signals['in_progress'])}")
    print(f"  - 待回复: {len(signals['pending_reply'])}")
    print(f"  - 待执行: {len(signals['pending_action'])}")
    print(f"  - 阻塞: {len(signals['blockers'])}")


if __name__ == '__main__':
    main()
