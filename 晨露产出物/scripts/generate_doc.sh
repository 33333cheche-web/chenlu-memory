#!/bin/bash
# 晨露文档生成快捷命令
# 用法: ./generate_doc.sh [word|excel|pdf|pptx] [参数...]

SCRIPT_DIR="/home/cheche/.openclaw/workspace-chenlu/晨露产出物/scripts"

case "$1" in
    word|docx)
        echo "📝 生成 Word 文档..."
        python3 "$SCRIPT_DIR/document_generator.py"
        ;;
    excel|xlsx)
        echo "📊 生成 Excel 表格..."
        python3 -c "
import sys
sys.path.insert(0, '$SCRIPT_DIR')
from document_generator import generate_morning_report_excel
generate_morning_report_excel()
"
        ;;
    pdf)
        echo "📄 生成 PDF 文档..."
        python3 -c "
import sys
sys.path.insert(0, '$SCRIPT_DIR')
from document_generator import generate_morning_report_pdf
generate_morning_report_pdf()
"
        ;;
    pptx|ppt)
        echo "🎯 生成 PPT 演示..."
        echo "（需要手动调用 document_generator.py 的 generate_pptx 函数）"
        ;;
    *)
        echo "晨露文档生成器"
        echo "用法:"
        echo "  ./generate_doc.sh word    - 生成 Word 版晨报"
        echo "  ./generate_doc.sh excel   - 生成 Excel 版晨报"
        echo "  ./generate_doc.sh pdf     - 生成 PDF 版晨报"
        ;;
esac
