# Noiz TTS 修复指引

> 修复时间：2026-03-30
> 问题：Noiz API 404 错误
> 原因：API 端点变更 (/v1/tts → /v1/text-to-speech)

---

## 问题现象

使用 TTS 语音克隆时报错：
```
Error: 404 - Not Found
```

原 API 端点 `https://api.noiz.ai/v1/tts` 已失效。

---

## 修复内容

### 1. API 端点变更

| 旧端点 | 新端点 |
|--------|--------|
| `https://api.noiz.ai/v1/tts` | `https://api.noiz.ai/v1/text-to-speech` |

### 2. 请求格式变更

| 旧格式 | 新格式 |
|--------|--------|
| JSON (`application/json`) | `multipart/form-data` |

### 3. 新增功能

- **创建 Voice**: 上传参考音频创建语音克隆 (`/v1/voices`)
- **列出 Voices**: 查看所有可用的 voices (`/v1/voices`)

---

## 使用方法

### 前提条件

确保 `~/.config/noiz/api_key` 文件存在且包含有效的 API Key：

```bash
# 检查 API Key
cat ~/.config/noiz/api_key
```

### 脚本位置

```
/home/cheche/.openclaw/workspace-baby/.agents/skills/tts/scripts/tts.py
```

### 基本用法

#### 1. 列出所有可用的 voices

```bash
cd /home/cheche/.openclaw/workspace-baby/.agents/skills/tts/scripts
python3 tts.py -t "test" --list-voices
```

#### 2. 使用已有的 voice_id 生成语音

```bash
python3 tts.py -t "你好，我是Baby" --voice-id YOUR_VOICE_ID -o output.wav
```

#### 3. 用参考音频创建新 voice 并生成

```bash
python3 tts.py -t "你好" --ref-audio /path/to/reference.wav -o output.wav
```

---

## API 调用流程

### 流程1：使用已有 voice

```
用户输入 → /v1/text-to-speech → 生成音频 → 下载保存
```

### 流程2：创建新 voice

```
参考音频 → /v1/voices (创建) → 获取 voice_id → /v1/text-to-speech → 生成音频
```

---

## 关键 API 端点

| 功能 | 端点 | 方法 |
|------|------|------|
| 创建 Voice | `/v1/voices` | POST |
| 列出 Voices | `/v1/voices` | GET |
| 文本转语音 | `/v1/text-to-speech` | POST |

---

## 请求参数说明

### /v1/text-to-speech

| 参数 | 类型 | 说明 |
|------|------|------|
| `text` | string | 要转换的文本 |
| `voice_id` | string | Voice ID |
| `output_format` | string | 输出格式：wav/mp3/opus/flac/ogg |
| `speed` | float | 语速，默认 1.0 |
| `similarity_enh` | boolean | 是否保留音色，默认 false |
| `quality_preset` | int | 质量预设，默认 3 |

### /v1/voices (创建)

| 参数 | 类型 | 说明 |
|------|------|------|
| `file` | file | 参考音频文件 |
| `display_name` | string | Voice 显示名称 |
| `language` | string | 语言，如 zh/en |
| `denoise` | boolean | 是否降噪 |

---

## 故障排查

### Q1: API Key 无效
**错误**: `401 Unauthorized`
**解决**: 
```bash
# 检查 API Key 文件
cat ~/.config/noiz/api_key
# 如果失效，需要重新登录 Noiz 网站获取新的 API Key
```

### Q2: Voice 不存在
**错误**: `Voice not found`
**解决**:
```bash
# 先列出所有 voices
python3 tts.py -t "test" --list-voices
# 使用正确的 voice_id
```

### Q3: 参考音频格式不支持
**错误**: `Unsupported audio format`
**解决**:
- 支持的格式：wav, mp3, m4a
- 建议时长：10秒 - 5分钟
- 建议质量：44.1kHz, 16bit, 单声道

---

## 注意事项

1. **API Key 安全**: 不要泄露 API Key，保存在 `~/.config/noiz/api_key`
2. **参考音频质量**: 音质越好，克隆效果越好
3. **网络稳定**: 生成过程需要联网，确保网络稳定
4. **字符限制**: 单次文本长度有限制（通常 5000 字符）

---

## 参考链接

- Noiz OpenAPI 文档: `https://api.noiz.ai/openapi.json`
- 原脚本备份: `tts.py.backup` (如果有)

---

*修复完成时间：2026-03-30*
*修复者：晨露宝宝 🌟*
