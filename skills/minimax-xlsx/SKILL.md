# minimax-xlsx Skill

## 描述
使用 Python 和 openpyxl 创建和编辑 Excel 表格 (.xlsx)。

## 用法

### 创建 Excel 文件
```bash
python3 /home/cheche/.openclaw/workspace-chenlu/skills/minimax-xlsx/minimax-xlsx.py \
  --create \
  --data '[["标题1", "标题2"], ["数据1", "数据2"]]' \
  --output /tmp/输出.xlsx
```

### 示例
```bash
python3 /home/cheche/.openclaw/workspace-chenlu/skills/minimax-xlsx/minimax-xlsx.py \
  --create \
  --data '[["日期", "标题", "链接"], ["2026-03-27", "AI新闻", "https://example.com"]]' \
  --output /tmp/晨报数据.xlsx
```

## 依赖
- Python 3.8+
- openpyxl: `pip3 install openpyxl`

## 功能
- 创建新 Excel 文件
- 自动调整列宽
- 表头样式（绿色背景 + 白色文字）
