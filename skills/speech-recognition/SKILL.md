---
name: speech-recognition
description: 语音识别工具，使用 OpenAI Whisper 将音频/语音转换为文字。支持 mp3, wav, m4a, ogg, webm 等格式。
metadata: { "openclaw": { "emoji": "🎤", "requires": { "bins": ["python3", "ffmpeg"], "env": [] } } }
---

# 语音识别 (Speech Recognition)

使用 OpenAI Whisper 将音频文件中的语音转换为文字。

## 安装依赖

```bash
# 安装 ffmpeg
sudo apt install ffmpeg

# 安装 Whisper
pip install -U openai-whisper --break-system-packages
```

## Usage

```bash
python3 skills/scripts/speech_recognition.py <音频文件路径>

# 指定模型（默认 base）
python3 skills/scripts/speech_recognition.py voice.mp3 --model small
```

## 可用模型

| 模型 | 速度 | 准确率 | 适用场景 |
|------|------|--------|----------|
| tiny | 最快 | 一般 | 快速测试 |
| base | 快 | 较好 | 日常使用 |
| small | 中等 | 好 | 推荐 |
| medium | 较慢 | 很好 | 高质量 |
| large | 慢 | 最好 | 专业用途 |
| turbo | 很快 | 接近 large | 推荐 |

## 支持的格式

- MP3
- WAV
- M4A
- OGG
- WEBM
- MP4（会提取音频）
- 其他 ffmpeg 支持的格式

## 示例

```bash
# 识别语音消息
python3 skills/scripts/speech_recognition.py /tmp/voice.mp3

# 识别视频中的音频
python3 skills/scripts/speech_recognition.py video.mp4

# 使用高质量模型
python3 skills/scripts/speech_recognition.py recording.wav --model small
```
