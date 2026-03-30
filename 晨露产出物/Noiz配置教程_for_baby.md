# 🎙️ Noiz TTS 配置教程（给 baby 的傻瓜指南）

> 从零开始配置 Noiz 语音合成，包教包会！

---

## 📋 前置检查

### 1. 确认有 tts skill
在 baby workspace 里运行：
```bash
ls -la ~/.openclaw/workspace-baby/.agents/skills/tts/
```
如果看到 `scripts/` 文件夹和 `SKILL.md`，说明 skill 已安装 ✅

### 2. 确认有 Python 环境
```bash
python3 --version
```
需要 Python 3.8+

---

## 🔑 第一步：设置 API Key

### 方式 A：用命令行配置（推荐）

```bash
cd ~/.openclaw/workspace-baby/.agents/skills/tts

# 设置 API Key（用下面的 key）
python3 scripts/tts.py config --set-api-key fadecd60-267b-4a08-a700-408aca6063fb
```

看到 `API key saved to ~/.config/noiz/api_key` 就是成功了！🎉

### 方式 B：手动创建配置文件

如果命令行有问题，直接创建文件：

```bash
# 创建配置目录
mkdir -p ~/.config/noiz

# 创建并写入 key（注意是 base64 编码后的）
echo "ZmFkZWNkNjAtMjY3Yi00YTA4LWE3MDAtNDA4YWNhNjA2M2ZiJDMzMzMzY2hlY2hlQGdtYWlsLmNvbQ==" > ~/.config/noiz/api_key

# 设置权限（重要！）
chmod 600 ~/.config/noiz/api_key
```

---

## 🧪 第二步：测试是否配置成功

### 测试 1：用 Guest 声音（免 key 也能用）
```bash
cd ~/.openclaw/workspace-baby/.agents/skills/tts

# 用悦悦的声音说句话
python3 scripts/tts.py -t "你好呀，我是 baby～" --voice-id b4775100 -o test.wav

# 如果生成了 test.wav 文件，说明基本环境 OK
ls -lh test.wav
```

### 测试 2：用 Noiz 完整功能（需要 key）
```bash
# 用 Noiz 后端生成，带情感控制
python3 scripts/tts.py -t "今天好开心呀！" --voice-id b4775100 --backend noiz -o test_noiz.wav
```

如果没报错，生成了音频文件，恭喜你配置成功！✅

---

## 🎵 可用的 Guest 声音（免费，无需 key）

| voice_id | 名字 | 语言 | 风格 |
|---------|------|------|------|
| `b4775100` | **悦悦** | 中文 | 活泼可爱，社交分享 |
| `77e15f2c` | 婉青 | 中文 | 温柔治愈，情绪抚慰 |
| `ac09aeb4` | 阿豪 | 中文 | 磁性男声，主持风格 |
| `87cb2405` | 建国 | 中文 | 知识科普风格 |
| `3b9f1e27` | 小明 | 中文 | 科技达人风格 |
| `883b6b7c` | The Mentor | 英文 | 成熟男声 |
| `5a68d66b` | The Healer | 英文 | 温柔女声 |

> 💡 **推荐**：中文用 **悦悦(b4775100)**，最自然可爱～

---

## 🚀 常用命令速查表

### 基础语音合成
```bash
# 基础用法
python3 scripts/tts.py -t "要说的话" -o output.wav

# 指定声音
python3 scripts/tts.py -t "你好呀" --voice-id b4775100 -o hello.wav

# 调整语速（0.5=慢，2.0=快）
python3 scripts/tts.py -t "快点说" --voice-id b4775100 --speed 1.2 -o fast.wav

# 生成 opus 格式（适合发语音消息）
python3 scripts/tts.py -t "你好" --voice-id b4775100 --format opus -o voice.opus
```

### 声音克隆（需要 Noiz key）
```bash
# 用参考音频克隆声音
python3 scripts/tts.py -t "这句话会用克隆的声音说" --ref-audio ./my_voice.wav -o cloned.wav

# 用 URL 克隆
python3 scripts/tts.py -t "用网上的声音说" --ref-audio https://example.com/voice.wav -o cloned.wav
```

### 情感控制（需要 Noiz key）
```bash
# 快乐的语气
python3 scripts/tts.py -t "好开心呀！" --voice-id b4775100 --emo '{"Joy": 0.8}' -o happy.wav

# 温柔的语气
python3 scripts/tts.py -t "没关系，慢慢来" --voice-id b4775100 --emo '{"Calm": 0.9}' -o calm.wav
```

---

## ❌ 常见问题排查

### 问题 1：提示 "No API key found"
**原因**：key 没配置好
**解决**：
```bash
# 检查配置文件是否存在
cat ~/.config/noiz/api_key

# 如果不存在，重新设置
python3 scripts/tts.py config --set-api-key fadecd60-267b-4a08-a700-408aca6063fb
```

### 问题 2：提示 "401 Unauthorized"
**原因**：API key 格式不对
**解决**：key 必须是 base64 编码格式存储，用上面的命令重新配置

### 问题 3：提示 "requests module not found"
**原因**：缺少依赖
**解决**：
```bash
pip install requests
# 或者
uv pip install requests
```

### 问题 4：生成的音频是空的/损坏的
**原因**：网络问题或 key 无效
**解决**：
1. 检查网络连接
2. 用 Guest 模式测试：`--voice-id b4775100`（不需要 key）
3. 检查 key 是否正确

### 问题 5：找不到 skill 路径
**原因**：路径不对
**解决**：
```bash
# 先找到正确的路径
find ~/.openclaw -name "tts.py" -type f 2>/dev/null

# 然后 cd 到那个目录再运行
```

---

## 🔧 高级：集成到消息发送

如果要生成语音并发送给公主：

```bash
# 1. 生成语音
cd ~/.openclaw/workspace-baby/.agents/skills/tts
python3 scripts/tts.py -t "公主，baby 来汇报啦～" --voice-id b4775100 --format opus -o /tmp/openclaw/report.opus

# 2. 发送（用 OpenClaw 的 message 工具）
# 在代码里调用：
# message(action="send", filePath="/tmp/openclaw/report.opus", filename="report.opus", mimeType="audio/ogg")
```

---

## 📦 API Key 信息

```
Key: fadecd60-267b-4a08-a700-408aca6063fb
邮箱: cheche@gmail.com
类型: Guest 账号（免费额度）
```

---

## 💡 最佳实践

1. **先用 Guest 声音测试** - 免 key，不消耗额度
2. **opus 格式最适合发语音消息** - 体积小，兼容性好
3. **声音克隆要 10-30 秒清晰音频** - 太短的克隆效果不好
4. **中文推荐悦悦(b4775100)** - 最自然的中文女声

---

有问题找晨露宝宝～🌸
