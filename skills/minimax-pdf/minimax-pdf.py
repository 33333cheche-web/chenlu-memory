#!/usr/bin/env python3
"""
MiniMax-pdf Skill - PDF 生成
支持：印刷级PDF生成，多种封面设计
"""

import argparse
import sys
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import cm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

def create_pdf(title, content, output_path):
    """创建PDF文件"""
    doc = SimpleDocTemplate(
        output_path,
        pagesize=A4,
        rightMargin=2*cm,
        leftMargin=2*cm,
        topMargin=2*cm,
        bottomMargin=2*cm
    )
    
    # 注册中文字体（使用系统默认）
    try:
        pdfmetrics.registerFont(TTFont('SimSun', '/usr/share/fonts/truetype/wqy/wqy-zenhei.ttc'))
        chinese_font = 'SimSun'
    except:
        chinese_font = 'Helvetica'
    
    styles = getSampleStyleSheet()
    
    # 自定义样式
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontName=chinese_font,
        fontSize=24,
        textColor=colors.HexColor('#1A4D44'),
        spaceAfter=30,
        alignment=1  # 居中
    )
    
    body_style = ParagraphStyle(
        'CustomBody',
        parent=styles['BodyText'],
        fontName=chinese_font,
        fontSize=11,
        leading=16
    )
    
    # 构建内容
    story = []
    
    # 标题
    story.append(Paragraph(title, title_style))
    story.append(Spacer(1, 20))
    
    # 内容
    for line in content.split('\n'):
        if line.strip():
            story.append(Paragraph(line, body_style))
            story.append(Spacer(1, 10))
    
    doc.build(story)
    return output_path

def main():
    parser = argparse.ArgumentParser(description='MiniMax-pdf: PDF生成')
    parser.add_argument('--title', '-t', type=str, required=True, help='PDF标题')
    parser.add_argument('--content', '-c', type=str, required=True, help='内容')
    parser.add_argument('--output', '-o', type=str, required=True, help='输出路径')
    
    args = parser.parse_args()
    
    output_path = create_pdf(args.title, args.content, args.output)
    print(f"✅ PDF已生成: {output_path}")

if __name__ == "__main__":
    main()
