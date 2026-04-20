#!/bin/bash
# 语音识别快速脚本 - 临时方案
# 需要提前安装: pip install openai-whisper

AUDIO_FILE="$1"
MODEL="${2:-tiny}"

if [ -z "$AUDIO_FILE" ]; then
    echo "用法: bash speech_quick.sh <音频文件> [模型大小]"
    echo "示例: bash speech_quick.sh voice.mp3 tiny"
    echo ""
    echo "可用模型: tiny(最小最快), base, small, medium, large"
    exit 1
fi

# 使用 whisper 命令行
whisper "$AUDIO_FILE" --model "$MODEL" --language Chinese --fp16 False
