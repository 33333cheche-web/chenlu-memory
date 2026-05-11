#!/bin/bash
# 将头像图片转换为 base64 并替换 HTML 中的引用

cd /home/cheche/.openclaw/workspace-chenlu/晨露产出物/Dashboard_运维

# 读取各图片的 base64
CHARLES_B64=$(base64 -w 0 avatar-charles.jpg)
SEAN_B64=$(base64 -w 0 avatar-sean.jpg)
ASIN_B64=$(base64 -w 0 avatar-asin.jpg)

# 创建临时文件
HTML_FILE="openclaw-dashboard-v4.html"

# 替换 Charles 头像
sed -i "s|src=\"avatar-charles.jpg\"|src=\"data:image/jpeg;base64,${CHARLES_B64}\"|" "$HTML_FILE"

# 替换 Sean 头像
sed -i "s|src=\"avatar-sean.jpg\"|src=\"data:image/jpeg;base64,${SEAN_B64}\"|" "$HTML_FILE"

# 替换 Asin 头像
sed -i "s|src=\"avatar-asin.jpg\"|src=\"data:image/jpeg;base64,${ASIN_B64}\"|" "$HTML_FILE"

echo "✅ 头像已嵌入完成"