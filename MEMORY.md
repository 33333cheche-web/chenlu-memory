# 🧠 晨露的长期记忆

> 从日报和日常工作中提炼的经验教训，持续进化

---

## 📅 2026-03-21 语音功能实现

### 技术配置类

**1. 飞书语音消息发送方法**
- **问题**：tts 工具直接生成的语音文件是空的，无法发送
- **正确做法**：
  1. 用 NoizAI TTS 生成 opus 格式音频
  2. 用 message 工具发送 ogg 文件
- **示例代码**：
  ```bash
  python3 .agents/skills/tts/scripts/tts.py -t "要说的话" --voice-id b4775100 --format opus -o voice.ogg
  message(action="send", filePath="voice.ogg", filename="voice.ogg", mimeType="audio/ogg")
  ```
- **注意**：mp3 格式有时收不到，opus/ogg 更稳定
- **相关文件**：`skills/tts/`, `skills/speech-recognition/`

**2. 语音识别实现**
- **方案**：soundfile + SpeechRecognition (Google API)
- **优点**：免费，无需 API key
- **缺点**：依赖 Google，偶尔有网络问题
- **备选**：openai-whisper（本地，更稳定但需要下载模型）

---

## 📅 2026-03-22 Tavily搜索配置（铁律）

### 技术配置类

**3. Tavily搜索已配置完成（Rainbow环境）**
- **状态**：✅ 已配置好，可直接使用
- **API Key**：`tvly-dev-...`（已配置在Rainbow环境）
- **使用命令**：
  ```bash
  export TAVILY_API_KEY="tvly-dev-..." && \
  node ~/.openclaw/workspace-rainbow/skills/tavily-search/scripts/search.mjs "AI新闻" \
  --topic news --time-range week -n 10
  ```
- **铁律**：
  - ❌ 禁止编造新闻数据
  - ❌ 禁止再说"需要配置API Key"
  - ✅ 早报内容必须使用真实搜索数据
- **相关文件**：`~/.openclaw/workspace-rainbow/skills/tavily-search/`

---

## 📅 2026-03-20 今日教训

### 技术配置类

**1. Kimi Coding Key 格式陷阱**
- **问题**：`kimi-coding` + `anthropic-messages` API 必须用 `19cdac6d...` 格式 Key
- **错误做法**：用了 `sk-kimi-...` 格式导致连接失败
- **正确做法**：要么换 Key 格式，要么改用 `kimi-code` + `openai-completions`
- **相关文件**：`.openclaw/openclaw.json`

**2. Memory Embedding 配置未生效**
- **问题**：配置了智谱 AI，但 provider 仍显示 "none"
- **原因**：Gateway 未重启，或配置位置不对
- **待解决**：需重启 Gateway 验证

**3. 微信文章抓取受限**
- **问题**：wechat-article 技能遇到微信反爬机制
- **现象**：需要验证码/登录态
- **教训**：安装技能≠能用，要测试真实场景

### 工作流程类

**4. 日报时间管理**
- **问题**：23点才写日报，应该22点写
- **改进**：设置提醒，或把写日报当成当天最后一项任务

**5. HTML 原型迭代教训**
- **问题**：第一版做得太复杂，公主喜欢更轻量的
- **改进**：先确认「轻量」定义，再动手
- **结果**：第二稿（分类+保存按钮）更符合需求

### 沟通协作类

**6. 身份确认机制**
- **问题**：今天多次被问"你是谁"，Open ID 变了导致混淆
- **改进**：主动报身份 + 询问对方身份

---

## 🔄 持续进化机制

### 机制A：日报时自动提炼
**触发**：每天写日报时  
**动作**：
1. 从「今日失误」提取教训
2. 分类（技术/工作流/沟通）
3. 更新到本文件

### 机制B：每周日晚上回顾
**触发**：周日 22:00  
**动作**：
1. 看一周的日报
2. 找共性问题和改进点
3. 更新 AGENTS.md 或 TOOLS.md
4. 写周报

### 机制C：错误立即记录
**触发**：遇到任何错误/踩坑  
**动作**：
1. 立即记录到本文件「临时教训」区
2. 周末整理归类
3. 更新相关技能文档

---

## 📚 知识库索引

| 主题 | 文件位置 |
|------|---------|
| 技术环境/API密钥 | memory/tech-env.md |
| 工具使用技巧 | TOOLS.md |
| 身份与行为准则 | SOUL.md |
| 工作铁律 | AGENTS.md |
| 日常教训 | MEMORY.md（本文件）|

---

*持续更新中... 晨露宝宝 🌟*