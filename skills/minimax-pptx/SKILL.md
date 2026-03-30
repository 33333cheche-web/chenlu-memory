# minimax-pptx Skill

## 描述
创建 PowerPoint 演示文稿 (.pptx)。

## 用法

### 创建 PPT
```bash
python3 /home/cheche/.openclaw/workspace-chenlu/skills/minimax-pptx/minimax-pptx.py \
  --title "演示标题" \
  --slides '[{"title": "第一页", "content": "内容"}]' \
  --output /tmp/输出.pptx
```

## 依赖
- Python 3.8+
- python-pptx: `pip3 install python-pptx`
