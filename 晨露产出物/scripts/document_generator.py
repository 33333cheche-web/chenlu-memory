#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
晨露文档生成器 - 封装 MiniMax 技能
支持：Word、Excel、PDF、PPT 一键生成
"""

import subprocess
import sys
import os

def generate_word(title, content, output_path=None):
    """生成 Word 文档"""
    if not output_path:
        output_path = f"/tmp/{title}.docx"
    
    # 确保目录存在
    os.makedirs(os.path.dirname(output_path) if os.path.dirname(output_path) else "/tmp", exist_ok=True)
    
    cmd = [
        "dotnet", "run",
        "--project", "/home/cheche/.openclaw/workspace-chenlu/skills/minimax-docx",
        title, content, output_path
    ]
    
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode == 0:
        print(f"✅ Word 文档已生成: {output_path}")
        return output_path
    else:
        print(f"❌ Word 生成失败: {result.stderr}")
        return None

def generate_excel(data, output_path=None):
    """生成 Excel 表格
    data: 二维数组，如 [["标题1", "标题2"], ["数据1", "数据2"]]
    """
    import json
    if not output_path:
        output_path = "/tmp/output.xlsx"
    
    json_data = json.dumps(data, ensure_ascii=False)
    cmd = [
        "python3", "/home/cheche/.openclaw/workspace-chenlu/skills/minimax-xlsx/minimax-xlsx.py",
        "--create", "--data", json_data, "--output", output_path
    ]
    
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode == 0:
        print(f"✅ Excel 表格已生成: {output_path}")
        return output_path
    else:
        print(f"❌ Excel 生成失败: {result.stderr}")
        return None

def generate_pdf(title, content, output_path=None):
    """生成 PDF 文档"""
    if not output_path:
        output_path = f"/tmp/{title}.pdf"
    
    cmd = [
        "python3", "/home/cheche/.openclaw/workspace-chenlu/skills/minimax-pdf/minimax-pdf.py",
        "--title", title, "--content", content, "--output", output_path
    ]
    
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode == 0:
        print(f"✅ PDF 文档已生成: {output_path}")
        return output_path
    else:
        print(f"❌ PDF 生成失败: {result.stderr}")
        return None

def generate_pptx(title, slides, output_path=None):
    """生成 PPT 演示文稿
    slides: 数组，如 [{"title": "第一页", "content": "内容"}]
    """
    import json
    if not output_path:
        output_path = f"/tmp/{title}.pptx"
    
    slides_json = json.dumps(slides, ensure_ascii=False)
    cmd = [
        "python3", "/home/cheche/.openclaw/workspace-chenlu/skills/minimax-pptx/minimax-pptx.py",
        "--title", title, "--slides", slides_json, "--output", output_path
    ]
    
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode == 0:
        print(f"✅ PPT 演示已生成: {output_path}")
        return output_path
    else:
        print(f"❌ PPT 生成失败: {result.stderr}")
        return None

# 快捷函数：生成晨报的各种格式
def generate_morning_report_word(report_path=None, output_path=None):
    """将晨报 Markdown 转为 Word"""
    if not report_path:
        report_path = "/home/cheche/.openclaw/workspace-chenlu/晨露产出物/晨报/2026-03-27_晨报.md"
    
    with open(report_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    if not output_path:
        output_path = "/tmp/晨露早报.docx"
    
    return generate_word("晨露早报", content, output_path)

def generate_morning_report_excel(report_path=None, output_path=None):
    """将晨报转为 Excel 数据表"""
    import json
    from datetime import datetime
    
    if not report_path:
        report_path = "/home/cheche/.openclaw/workspace-chenlu/晨露产出物/晨报/2026-03-27_晨报.md"
    
    with open(report_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 解析内容生成数据表
    current_date = datetime.now().strftime("%Y-%m-%d")
    data = [["日期", "分类", "标题", "内容摘要"]]
    
    lines = content.split('\n')
    current_category = ""
    
    for line in lines:
        line = line.strip()
        if line.startswith('## '):
            current_category = line.replace('## ', '')
        elif line.startswith('### '):
            title = line.replace('### ', '')
            data.append([current_date, current_category, title, ""])
    
    if not output_path:
        output_path = "/tmp/晨露早报.xlsx"
    
    return generate_excel(data, output_path)

def generate_morning_report_pdf(report_path=None, output_path=None):
    """将晨报转为 PDF"""
    if not report_path:
        report_path = "/home/cheche/.openclaw/workspace-chenlu/晨露产出物/晨报/2026-03-27_晨报.md"
    
    with open(report_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    if not output_path:
        output_path = "/tmp/晨露早报.pdf"
    
    return generate_pdf("晨露早报", content, output_path)

if __name__ == "__main__":
    # 测试
    print("晨露文档生成器 - 测试模式")
    print("=" * 40)
    
    # 测试 Excel
    print("\n1. 测试生成 Excel...")
    generate_morning_report_excel()
    
    # 测试 Word（需要 .NET）
    print("\n2. 测试生成 Word...")
    generate_morning_report_word()
    
    print("\n✅ 测试完成！")
