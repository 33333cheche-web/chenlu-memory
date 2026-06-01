#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
将 /home/cheche/dashboard-v5.html 中的 Baby metric-card 改为标准 flip-card 结构。

功能：
1) 自动定位 id="baby-metric" 的旧卡片（metric-card）
2) 保留旧卡片正面内容（Special Assistant/头像/名字/状态等）
3) 生成背面 file-list，文件来源：/home/cheche/.openclaw/workspace-baby/Baby产出物/
4) 添加 View Deliverables 与 Back 翻转按钮
5) 替换后保持在 metrics grid 中，不破坏整体布局
"""

from __future__ import annotations

import html
import os
import re
from pathlib import Path

DASHBOARD = Path('/home/cheche/dashboard-v5.html')
BABY_DIR = Path('/home/cheche/.openclaw/workspace-baby/Baby产出物/')
MAX_FILES = 30


def find_div_block(src: str, marker: str) -> tuple[int, int, str]:
    """找到包含 marker 的 <div ...>...</div> 完整块，返回(start, end, inner_html)。"""
    pos = src.find(marker)
    if pos == -1:
        raise ValueError(f'未找到标记: {marker}')

    start = src.rfind('<div', 0, pos)
    if start == -1:
        raise ValueError('未找到目标 div 起始标签')

    open_end = src.find('>', start)
    if open_end == -1:
        raise ValueError('目标 div 起始标签不完整')

    i = open_end + 1
    depth = 1
    div_open = re.compile(r'<div\b[^>]*>', re.IGNORECASE)
    div_close = re.compile(r'</div\s*>', re.IGNORECASE)

    while i < len(src):
        m_open = div_open.search(src, i)
        m_close = div_close.search(src, i)

        if not m_close:
            raise ValueError('未找到匹配的 </div>，HTML 结构可能损坏')

        if m_open and m_open.start() < m_close.start():
            depth += 1
            i = m_open.end()
        else:
            depth -= 1
            i = m_close.end()
            if depth == 0:
                end = i
                inner = src[open_end + 1:end - len(m_close.group(0))]
                return start, end, inner

    raise ValueError('未能闭合目标 div')


def build_file_items(files: list[Path]) -> str:
    if not files:
        return (
            '            <a class="file-item" href="#">\n'
            '              <span class="file-icon">📄</span>\n'
            '              <div class="file-info">\n'
            '                <div class="file-name">暂无产出物（目录不存在或为空）</div>\n'
            '                <div class="file-path">/home/cheche/.openclaw/workspace-baby/Baby产出物/</div>\n'
            '              </div>\n'
            '              <span class="file-tag">N/A</span>\n'
            '            </a>'
        )

    items = []
    for p in files:
        ext = p.suffix[1:].upper() if p.suffix else 'FILE'
        rel = str(p)
        name = html.escape(p.name)
        path_txt = html.escape(rel)
        tag = html.escape(ext[:8])
        item = (
            '            <a class="file-item" href="#">\n'
            '              <span class="file-icon">📝</span>\n'
            '              <div class="file-info">\n'
            f'                <div class="file-name">{name}</div>\n'
            f'                <div class="file-path">{path_txt}</div>\n'
            '              </div>\n'
            f'              <span class="file-tag">{tag}</span>\n'
            '            </a>'
        )
        items.append(item)

    return '\n'.join(items)


def get_baby_files() -> list[Path]:
    if not BABY_DIR.exists() or not BABY_DIR.is_dir():
        return []

    all_files = [p for p in BABY_DIR.rglob('*') if p.is_file()]
    all_files.sort(key=lambda x: str(x).lower())
    return all_files[:MAX_FILES]


def main() -> None:
    if not DASHBOARD.exists():
        raise FileNotFoundError(f'文件不存在: {DASHBOARD}')

    src = DASHBOARD.read_text(encoding='utf-8')

    start, end, front_inner = find_div_block(src, 'id="baby-metric"')

    # 去掉旧容器的 onclick（避免整卡点击与按钮触发冲突）
    front_inner_clean = re.sub(
        r'\s+onclick\s*=\s*"[^"]*"', '', front_inner, flags=re.IGNORECASE
    )

    files = get_baby_files()
    file_items = build_file_items(files)

    deliverables_count = len(files)
    deliverables_label = f'{deliverables_count} files' if deliverables_count else '0 files'

    new_block = f'''    <!-- Baby Card (Flip) -->
    <div class="flip-card" id="card-baby" style="height: 360px;">
      <div class="flip-card-inner">
        <!-- Front -->
        <div class="flip-card-front">
{front_inner_clean.rstrip()}
          <div class="bot-actions" style="margin-top: auto;">
            <button class="btn" onclick="flipCard('card-baby')">View Deliverables →</button>
          </div>
        </div>
        <!-- Back -->
        <div class="flip-card-back">
          <div class="back-header">
            <h3>Baby — Deliverables</h3>
          </div>
          <div class="bot-meta" style="margin-bottom: 12px;">
            <div class="bot-meta-row">
              <span class="bot-meta-label">Deliverables</span>
              <span class="bot-meta-value">{deliverables_label}</span>
            </div>
            <div class="bot-meta-row">
              <span class="bot-meta-label">Source</span>
              <span class="bot-meta-value" style="max-width: 240px; overflow: hidden; text-overflow: ellipsis; white-space: nowrap;">Baby产出物</span>
            </div>
          </div>
          <div class="file-list">
{file_items}
          </div>
          <div class="bot-actions" style="margin-top: auto;">
            <button class="btn" onclick="flipCard('card-baby')">← Back</button>
          </div>
        </div>
      </div>
    </div>'''

    out = src[:start] + new_block + src[end:]

    DASHBOARD.write_text(out, encoding='utf-8')
    print('✅ 已完成替换: Baby metric-card -> flip-card')
    print(f'📄 文件: {DASHBOARD}')
    print(f'📦 Baby 产出物文件数: {deliverables_count}')
    if not files:
        print('⚠️ 注意: /home/cheche/.openclaw/workspace-baby/Baby产出物/ 不存在或为空，已写入占位项。')


if __name__ == '__main__':
    main()
