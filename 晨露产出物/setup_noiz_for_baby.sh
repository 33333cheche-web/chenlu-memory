#!/bin/bash
# Noiz TTS 一键配置脚本 for baby
# 用法: bash setup_noiz_for_baby.sh

echo "🎙️ 开始配置 Noiz TTS..."

# 颜色输出
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# 1. 检查 Python
if ! command -v python3 &> /dev/null; then
    echo -e "${RED}❌ 错误: 没有找到 python3${NC}"
    exit 1
fi
echo -e "${GREEN}✅ Python3 已安装${NC}"

# 2. 安装依赖
echo "📦 安装依赖..."
pip install requests soundfile pydub --quiet 2>/dev/null || uv pip install requests soundfile pydub --quiet 2>/dev/null
echo -e "${GREEN}✅ 依赖安装完成${NC}"

# 3. 创建配置目录
mkdir -p ~/.config/noiz

# 4. 写入 API Key（base64 编码）
echo "ZmFkZWNkNjAtMjY3Yi00YTA4LWE3MDAtNDA4YWNhNjA2M2ZiJDMzMzMzY2hlY2hlQGdtYWlsLmNvbQ==" > ~/.config/noiz/api_key
chmod 600 ~/.config/noiz/api_key

echo -e "${GREEN}✅ API Key 已配置${NC}"

# 5. 查找 tts skill 路径
SKILL_PATH=$(find ~/.openclaw -name "tts.py" -type f 2>/dev/null | head -1)

if [ -z "$SKILL_PATH" ]; then
    echo -e "${YELLOW}⚠️ 警告: 没有找到 tts skill，请先安装 skill${NC}"
    echo "   安装命令: clawhub install tts"
else
    echo -e "${GREEN}✅ 找到 tts skill: $SKILL_PATH${NC}"
    
    # 6. 测试运行
    echo "🧪 测试生成语音..."
    cd "$(dirname "$SKILL_PATH")"
    python3 tts.py -t "配置成功！我是 baby，很高兴认识你～" --voice-id b4775100 --format opus -o /tmp/openclaw/test_baby.opus 2>/dev/null
    
    if [ -f "/tmp/openclaw/test_baby.opus" ]; then
        echo -e "${GREEN}🎉 配置成功！测试音频已生成: /tmp/openclaw/test_baby.opus${NC}"
        echo ""
        echo "📝 使用示例:"
        echo "   python3 scripts/tts.py -t '你好' --voice-id b4775100 -o hello.wav"
        echo ""
        echo "🎵 推荐声音:"
        echo "   - 悦悦(中文): b4775100"
        echo "   - 婉青(中文): 77e15f2c"
    else
        echo -e "${YELLOW}⚠️ 测试生成失败，但 key 已配置${NC}"
    fi
fi

echo ""
echo "✨ 配置完成！有问题找晨露宝宝～"
