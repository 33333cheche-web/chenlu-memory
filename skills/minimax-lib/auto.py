#!/usr/bin/env python3
"""
MiniMax Skills 智能调用器
根据用户需求自动选择合适的 Skill
"""

import subprocess
import json
import os
import sys

SKILLS_DIR = os.path.expanduser("~/.openclaw/workspace-mumu/skills")

def generate_excel(data, output_path, title=""):
    """生成Excel报价表/数据表"""
    script = f"{SKILLS_DIR}/minimax-xlsx/minimax-xlsx.py"
    data_json = json.dumps(data)
    
    result = subprocess.run(
        ["python3", script, "--create", "--data", data_json, "--output", output_path],
        capture_output=True,
        text=True
    )
    
    if result.returncode == 0:
        return output_path
    else:
        raise Exception(f"Excel生成失败: {result.stderr}")

def generate_pdf(title, content, output_path):
    """生成PDF方案书"""
    script = f"{SKILLS_DIR}/minimax-pdf/minimax-pdf.py"
    
    result = subprocess.run(
        ["python3", script, "--title", title, "--content", content, "--output", output_path],
        capture_output=True,
        text=True
    )
    
    if result.returncode == 0:
        return output_path
    else:
        raise Exception(f"PDF生成失败: {result.stderr}")

def generate_ppt(title, slides, output_path):
    """生成PPT演示文稿"""
    script = f"{SKILLS_DIR}/minimax-pptx/minimax-pptx.py"
    slides_json = json.dumps(slides)
    
    result = subprocess.run(
        ["python3", script, "--title", title, "--slides", slides_json, "--output", output_path],
        capture_output=True,
        text=True
    )
    
    if result.returncode == 0:
        return output_path
    else:
        raise Exception(f"PPT生成失败: {result.stderr}")

def auto_generate(task_type, data, output_name):
    """
    根据任务类型自动生成文档
    
    task_type: 'quote' | 'proposal' | 'presentation' | 'data'
    """
    output_dir = os.path.expanduser("~/.openclaw/workspace-mumu/沐木产出物")
    os.makedirs(output_dir, exist_ok=True)
    
    if task_type == 'quote':
        # 报价表 → Excel
        output_path = f"{output_dir}/{output_name}.xlsx"
        return generate_excel(data, output_path, "报价表")
    
    elif task_type == 'proposal':
        # 方案书 → PDF
        output_path = f"{output_dir}/{output_name}.pdf"
        title = data.get('title', '方案书')
        content = data.get('content', '')
        return generate_pdf(title, content, output_path)
    
    elif task_type == 'presentation':
        # PPT演示 → PPTX
        output_path = f"{output_dir}/{output_name}.pptx"
        title = data.get('title', '演示文稿')
        slides = data.get('slides', [])
        return generate_ppt(title, slides, output_path)
    
    elif task_type == 'data':
        # 数据表 → Excel
        output_path = f"{output_dir}/{output_name}.xlsx"
        return generate_excel(data, output_path, "数据表")
    
    else:
        raise ValueError(f"未知的任务类型: {task_type}")

# 便捷函数
def create_quote(data, name="报价表"):
    """创建报价表"""
    return auto_generate('quote', data, name)

def create_proposal(title, content, name="方案书"):
    """创建方案书PDF"""
    return auto_generate('proposal', {'title': title, 'content': content}, name)

def create_ppt(title, slides, name="演示文稿"):
    """创建PPT"""
    return auto_generate('presentation', {'title': title, 'slides': slides}, name)

if __name__ == "__main__":
    # 测试
    print("MiniMax Skills 智能调用器已加载")
    print("可用函数: create_quote(), create_proposal(), create_ppt()")
