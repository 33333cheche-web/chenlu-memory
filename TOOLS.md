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
- **主声音（文字）**: Edge TTS zh-CN-XiaoyiNeural（晓伊 - 卡通萝莉音）✅
- **备选**: Kokoro zf_xiaoxiao（晓晓）
- **备选**: Noiz Guest b4775100（悦悦）
- **语音合成**: Edge TTS（在线，中文萝莉音）+ Kokoro（本地备用）
- **语音识别**: soundfile + SpeechRecognition（Google API）

### 触发语音回复
当公主说 **"用语音回复我"** 时，晨露宝宝会用 **晓伊（Xiaoyi）** 的声音发语音消息。

生成命令：
```bash
# 1. 生成 mp3
edge-tts --voice zh-CN-XiaoyiNeural --text "要说的话" --write-media /tmp/openclaw/temp.mp3

# 2. 转成 opus 格式（飞书可直接播放）
ffmpeg -i /tmp/openclaw/temp.mp3 -c:a libopus -b:a 24k /tmp/openclaw/voice.opus -y
```

发送命令：
```python
message(action="send", filePath="/tmp/openclaw/voice.opus", filename="voice.opus", mimeType="audio/ogg")
```

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

---

## 🔍 搜索工具状态总览（2026-04-15 更新）

| 搜索工具 | 状态 | 适用场景 | 调用方式 |
|---------|------|---------|---------|
| **Brave** | ❌ 未配置 | OpenClaw原生`web_search` | 需要申请API Key |
| **Tavily** | ✅ 可用 | 英文内容、学术研究 | `node skills/tavily-search/scripts/search.mjs "关键词"` |
| **秘塔搜索** | ✅ 可用 | 中文内容、国内资讯 | `~/.openclaw/shared-memory/scripts/metaso-search.sh "关键词"` |
| **百度搜索** | ✅ 已配置（Baby部署） | 中文内容、百度生态 | `python3 ~/.npm-global/lib/node_modules/openclaw/skills/baidu-search/scripts/search.py "关键词"` |

### 使用建议
- **中文搜索** → 优先用秘塔或百度
- **英文/学术搜索** → 用Tavily
- **OpenClaw原生web_search** → 暂不可用（需Brave Key）

### API Keys位置
- Tavily: `~/.openclaw/shared-memory/entities/apis.md`
- 秘塔: `~/.openclaw/shared-memory/entities/apis.md`
- 百度: Baby负责管理

---

## 📦 轻笔记项目 - 精准调取索引

### V1 定稿版本（最新）
**关键词：** "轻笔记最后一个版本"、"轻笔记定稿"、"轻笔记v1"、"Melody优化版"

**调取命令：**
```bash
# 完整路径
/home/cheche/.openclaw/workspace-chenlu/晨露产出物/轻笔记项目/轻笔记_小程序_v1定稿_Melody优化版_20260328.zip

# 文件夹路径
/home/cheche/.openclaw/workspace-chenlu/晨露产出物/轻笔记项目/轻笔记_小程序_Melody优化版/

# 版本记录
/home/cheche/.openclaw/workspace-chenlu/晨露产出物/轻笔记项目/版本记录.md
```

**快速调取脚本：**
```bash
cd "/home/cheche/.openclaw/workspace-chenlu/晨露产出物/轻笔记项目" && ls -lh 轻笔记_小程序_v1定稿_Melody优化版_20260328.zip
```

### 其他版本索引
| 版本名称 | 文件路径 |
|---------|---------|
| Stitch部署包 | `轻笔记_Stitch部署包.zip` |
| H5网页版 | `轻笔记_部署包.zip` |
| 早期小程序 | `轻笔记_小程序代码.zip` |
| 版本记录 | `版本记录.md` |

**注意：** 公主问"最后一个版本"或"定稿版本"时，默认提供 **Melody优化版_v1定稿**

---

## 📁 文件管理规范（通用）

### 产出物命名规则
```
项目名_类型_版本状态_优化者_日期.扩展名

示例：
轻笔记_小程序_v1定稿_Melody优化版_20260328.zip
睡眠谷_方案_v2初稿_20260325.pptx
早报_模板_v1定稿_20260320.html
```

### 版本状态标记
| 标记 | 含义 | 使用场景 |
|------|------|---------|
| v1初稿 | 第一版初稿 | 刚完成的原始版本 |
| v2修改 | 第二版修改中 | 根据反馈调整中 |
| v1定稿 | 第一版定稿 | 已确认的最终版本 |
| v2定稿 | 第二版定稿 | 迭代后的最终版本 |

### 产出物目录结构
```
晨露产出物/
├── 项目A/
│   ├── 项目A_文档_v1定稿_20260328.docx
│   ├── 项目A_代码_v1定稿_20260328.zip
│   └── 版本记录.md
├── 项目B/
│   └── ...
└── 参考资料/
    └── ...
```

### 精准调取方法
**1. 按项目名调取**
```bash
ls "/home/cheche/.openclaw/workspace-chenlu/晨露产出物/项目名/"
```

**2. 按版本调取**
```bash
find "/home/cheche/.openclaw/workspace-chenlu/晨露产出物" -name "*v1定稿*" -type f
```

**3. 按日期调取**
```bash
find "/home/cheche/.openclaw/workspace-chenlu/晨露产出物" -name "*20260328*" -type f
```

### 版本记录模板
每个项目文件夹必须包含 `版本记录.md`：
```markdown
# 项目名 - 版本记录

## 最新定稿版本
- 文件名：xxx_v1定稿_xxx.zip
- 日期：2026-03-28
- 说明：xxx

## 历史版本
| 文件名 | 日期 | 状态 |
|--------|------|------|
| xxx_v1初稿 | 2026-03-26 | 已废弃 |
| xxx_v2修改 | 2026-03-27 | 已废弃 |
| xxx_v1定稿 | 2026-03-28 | ✅ 当前使用 |
```

### 铁律
1. **所有产出物必须放入** `晨露产出物/项目名/` 文件夹
2. **必须包含日期** 格式：YYYYMMDD
3. **定稿版本必须标记** `vX定稿`
4. **必须创建版本记录.md**
5. **公主问"最后一个版本"时**，自动提供最新的 `vX定稿` 版本

---

## 🔐 GitHub 备份配置

### 核心记忆自动备份
- **备份时间**: 每周一 23:10
- **备份脚本**: `/home/cheche/.openclaw/workspace-chenlu/scripts/memory-backup.sh`
- **仓库地址**: `https://github.com/33333cheche-web/chenlu-memory.git`
- **GitHub Token**: 已从文件中移除（请从环境变量 `GITHUB_TOKEN` 读取）
- **配置方式**: Token 已嵌入 git remote URL（通过环境变量配置）

### 手动推送命令
```bash
cd /home/cheche/.openclaw/workspace-chenlu
git add SOUL.md MEMORY.md USER.md IDENTITY.md AGENTS.md HEARTBEAT.md TOOLS.md memory/
git commit -m "备份说明"
git push origin master
```

### 检查远程仓库
```bash
git remote -v
```

---

## 🎨 DESIGN.md 设计系统库

知名网站的设计系统文档，用于快速构建一致风格的 UI。

### 存放位置
```
~/晨露产出物/DESIGN_Markdown_设计系统/
```

### 已下载的设计系统

| 文件 | 风格 | 适用场景 |
|------|------|----------|
| `Linear_DESIGN.md` | 暗黑科技感、紫罗兰强调色 | 开发者工具、SaaS、仪表盘 |
| `Figma_DESIGN.md` | 现代简洁、黑白为主 | 设计工具、创意产品 |
| `Notion_DESIGN.md` | 温和友好、米白背景 | 笔记应用、知识管理 |
| `Vercel_DESIGN.md` | 极简黑白、科技感 | 开发者平台、落地页 |
| `Apple_DESIGN.md` | 高端质感、圆角卡片 | 产品展示、品牌官网 |
| `Spotify_DESIGN.md` | 渐变色彩、音乐氛围 | 娱乐应用、社交平台 |

### 使用方法
```bash
# 1. 复制到项目
cp ~/晨露产出物/DESIGN_Markdown_设计系统/Linear_DESIGN.md ~/你的项目/DESIGN.md

# 2. 告诉 AI 使用
# "参考 DESIGN.md 的设计风格，帮我做一个登录页面"
```

### 来源
- **GitHub**: [VoltAgent/awesome-design-md](https://github.com/VoltAgent/awesome-design-md)
- **说明**: Google Stitch 推出的设计系统格式，AI 可直接读取并生成一致 UI