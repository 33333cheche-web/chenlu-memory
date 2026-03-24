# TOOLS.md - Local Notes

Skills define _how_ tools work. This file is for _your_ specifics — the stuff that's unique to your setup.

## What Goes Here

Things like:

- Camera names and locations
- SSH hosts and aliases
- Preferred voices for TTS
- Speaker/room names
- Device nicknames
- Anything environment-specific

## Examples

```markdown
### Cameras

- living-room → Main area, 180° wide angle
- front-door → Entrance, motion-triggered

### SSH

- home-server → 192.168.1.100, user: admin

### TTS

- Preferred voice: "Nova" (warm, slightly British)
- Default speaker: Kitchen HomePod
```

## Why Separate?

Skills are shared. Your setup is yours. Keeping them apart means you can update skills without losing your notes, and share skills without leaking your infrastructure.

---

Add whatever helps you do your job. This is your cheat sheet.

## 回复模式设置

### 当前设置（2026-03-21 更新）
- **默认模式**：💬 文字回复
- **语音模式**：🎤 仅在公主说"用语音回复我"时启用

### 使用方式
- 平时：晨露用文字回复
- 需要语音时：公主说"用语音回复我"
- 切回文字：公主说"用文字回复"或默认即可

---

## 晨露的语音配置 🎤

### 已选声音
- **主声音**: Kokoro zf_xiaoxiao（晓晓）
- **备选**: Noiz Guest b4775100（悦悦）
- **语音合成**: Kokoro（本地，免费）+ Noiz Guest（云端备用）
- **语音识别**: soundfile + SpeechRecognition（Google API）

### 使用方法
```bash
# Kokoro 本地语音
python3 -c "
from kokoro import KPipeline
import soundfile as sf
pipeline = KPipeline(lang_code='z')
generator = pipeline('要说的内容', voice='zf_xiaoxiao', speed=1.1)
for gs, ps, audio in generator:
    sf.write('output.wav', audio, 24000)
    break
"

# 语音识别
python3 skills/scripts/speech_recognition.py <音频文件>
```
