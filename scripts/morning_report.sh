#!/bin/bash
# 晨露早报入口脚本 - 调用 Python 主程序

cd "$(dirname "$0")/../"
python3 scripts/morning_report.py
