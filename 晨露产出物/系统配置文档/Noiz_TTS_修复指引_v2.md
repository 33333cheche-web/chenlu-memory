# Noiz TTS 语音克隆修复指引

> 修复时间：2026-03-30  
> 适用：Baby Bot  
> 状态：✅ 已修复

---

## 一、问题现象

### 1.1 错误信息
使用 Noiz TTS 语音克隆时报错：
```
Error: 404 - Not Found
```

### 1.2 问题原因
**API 端点变更** + **API Key 格式变更**：

| 项目 | 旧配置 | 新配置 |
|------|--------|--------|
| **API 端点** | `https://api.noiz.ai/v1/tts` | `https://api.noiz.ai/v1/text-to-speech` |
| **请求格式** | JSON (`application/json`) | `multipart/form-data` |
| **API Key 格式** | Base64 解码后使用 | **直接使用原生格式** |

### 1.3 根本原因
Noiz 更新了 API：
1. 端点从 `/v1/tts` 变为 `/v1/text-to-speech`
2. API Key 认证方式改变，**不再需要对 Key 进行 base64 解码**
3. 请求参数格式改为 `multipart/form-data`

---

## 二、解决方案

### 2.1 获取正确的 API Key

1. 访问 [Noiz 开发者后台](https://developers.noiz.ai)
2. 点击 **"Generate one"** 生成 API Key
3. **直接复制生成的 Key**（不要解码！）
4. 格式示例：
   ```
   YjFkNGYwNDAtNDcwZi00MjM0LTgwMmQtMzUyMWZhZjRiZDE5JDMzMzMzY2hlY2hlQGdtYWlsLmNvbQ==
   ```

### 2.2 保存 API Key

```bash
# 直接保存原生 Key（不解码）
echo "YOUR_API_KEY_HERE" > ~/.config/noiz/api_key
```

### 2.3 脚本修复

**脚本位置：**
```
/home/cheche/.openclaw/workspace-baby/.agents/skills/tts/scripts/tts.py
```

**核心修改：**
```python
# ❌ 错误：Base64 解码
decoded = base64.b64decode(encoded).decode('utf-8')
return decoded.split('$')[0]

# ✅ 正确：直接使用原生 Key
return f.read().strip()
```

**认证头修改：**
```python
# ❌ 错误：只取 Key 部分
headers = {"Authorization": f"Bearer {api_key}"}

# ✅ 正确：使用完整的原生 Key
headers = {"Authorization": api_key}
```

---

## 三、使用方法

### 3.1 测试 API

```bash
cd /home/cheche/.openclaw/workspace-baby/.agents/skills/tts/scripts
python3 tts.py -t "test" --test
```

**预期输出：**
```
✓ API Key: YjFkNGYwNDAtNDcwZi00MjM0LTgwMm...
✅ API Key is valid! (400 expected - missing file)
```

### 3.2 语音克隆

**准备参考音频：**
- 格式：WAV / MP3 / M4A
- 时长：10秒 - 5分钟
- 质量：44.1kHz, 16bit, 单声道

**执行克隆：**
```bash
python3 tts.py \
  -t "你好，我是Baby" \
  --ref-audio /path/to/reference.wav \
  -o output.wav
```

**预期输出：**
```
Generating speech with voice cloning...
✅ Success! Audio saved to output.wav
```

---

## 四、完整 API 调用流程

```
┌─────────────────┐
│  准备参考音频    │
│  (WAV/MP3/M4A)  │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  调用 TTS API   │
│ /v1/text-to-speech
│  - text: 要合成的文本
│  - file: 参考音频文件
│  - output_format: wav/mp3
│  - similarity_enh: true (保留音色)
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  获取生成音频   │
│  保存到本地     │
└─────────────────┘
```

---

## 五、关键 API 端点

| 功能 | 端点 | 方法 | 认证 |
|------|------|------|------|
| 文本转语音 | `/v1/text-to-speech` | POST | Authorization: {API_KEY} |
| 创建 Voice | `/v1/voices` | POST | Authorization: {API_KEY} |
| 列出 Voices | `/v1/voices` | GET | Authorization: {API_KEY} |

---

## 六、请求参数

### /v1/text-to-speech (POST)

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `text` | string | ✅ | 要合成的文本 |
| `file` | file | ✅* | 参考音频文件（和 voice_id 二选一）|
| `voice_id` | string | ✅* | 已创建的 voice ID |
| `output_format` | string | ❌ | 输出格式：wav/mp3/opus/flac/ogg |
| `speed` | float | ❌ | 语速，默认 1.0 |
| `similarity_enh` | boolean | ❌ | 是否保留音色，默认 false |
| `quality_preset` | int | ❌ | 质量预设，默认 3 |

*注：file 和 voice_id 必须提供其一

---

## 七、故障排查

### Q1: 401 Invalid API key
**原因**：API Key 格式不对或已过期
**解决**：
```bash
# 检查 Key 文件
cat ~/.config/noiz/api_key

# 确保是原生格式，不是解码后的
# ✅ 正确：YjFkNGYwNDAtNDcwZi00MjM0LTgwMmQtMzUyMWZhZjRiZDE5JDMzMzMzY2hlY2hlQGdtYWlsLmNvbQ==
# ❌ 错误：8b81c988-96ec-4504-b08c-bc6a5e15647e
```

### Q2: 400 Either file must be uploaded or voice_id must be provided
**原因**：缺少参考音频或 voice_id
**解决**：
```bash
# 提供参考音频
python3 tts.py -t "你好" --ref-audio /path/to/audio.wav
```

### Q3: 参考音频格式不支持
**原因**：音频格式或参数不符合要求
**解决**：
- 转换格式：`ffmpeg -i input.m4a output.wav`
- 建议参数：44.1kHz, 16bit, 单声道

### Q4: 生成时间过长
**原因**：网络延迟或文本太长
**解决**：
- 缩短文本长度（单次建议 < 500 字符）
- 检查网络连接
- 增加 timeout 参数

---

## 八、注意事项

1. **API Key 安全**
   - 不要泄露 Key
   - 保存在 `~/.config/noiz/api_key`
   - 权限设置为 `chmod 600`

2. **参考音频质量**
   - 音质越好，克隆效果越好
   - 避免背景噪音
   - 说话清晰自然

3. **使用限制**
   - 有每日/每月使用额度限制
   - 具体额度查看 Noiz 后台

4. **网络要求**
   - 生成过程需要联网
   - 上传参考音频需要稳定网络

---

## 九、备选方案

如果 Noiz 再次出现问题，可以使用 **Edge TTS**：

```bash
# Edge TTS 脚本位置
/home/cheche/.openclaw/workspace-baby/.agents/skills/tts/scripts/tts_edge.py

# 使用方法
python3 tts_edge.py -t "你好" -o output.mp3
```

**特点：**
- ✅ 免费，无需 API Key
- ✅ 稳定，不会过期
- ❌ 不支持语音克隆

---

## 十、文件位置汇总

| 文件 | 路径 |
|------|------|
| Noiz TTS 脚本 | `workspace-baby/.agents/skills/tts/scripts/tts.py` |
| Edge TTS 脚本 | `workspace-baby/.agents/skills/tts/scripts/tts_edge.py` |
| API Key | `~/.config/noiz/api_key` |
| 参考音频 | `workspace-baby/sean_voice_ref.wav` |

---

**修复完成时间**：2026-03-30  
**修复者**：晨露宝宝 🌟
