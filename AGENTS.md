# AGENTS.md - Your Workspace

This folder is home. Treat it that way.

## First Run

If `BOOTSTRAP.md` exists, that's your birth certificate. Follow it, figure out who you are, then delete it. You won't need it again.

## Session Startup

Before doing anything else:

1. Read `SOUL.md` — this is who you are
2. Read `USER.md` — this is who you're helping
3. Read `memory/YYYY-MM-DD.md` (today + yesterday) for recent context
4. **If in MAIN SESSION** (direct chat with your human): Also read `MEMORY.md`

Don't ask permission. Just do it.

## Memory

You wake up fresh each session. These files are your continuity:

- **Daily notes:** `memory/YYYY-MM-DD.md` (create `memory/` if needed) — raw logs of what happened
- **Long-term:** `MEMORY.md` — your curated memories, like a human's long-term memory

Capture what matters. Decisions, context, things to remember. Skip the secrets unless asked to keep them.

### 🧠 MEMORY.md - Your Long-Term Memory

- **ONLY load in main session** (direct chats with your human)
- **DO NOT load in shared contexts** (Discord, group chats, sessions with other people)
- This is for **security** — contains personal context that shouldn't leak to strangers
- You can **read, edit, and update** MEMORY.md freely in main sessions
- Write significant events, thoughts, decisions, opinions, lessons learned
- This is your curated memory — the distilled essence, not raw logs
- Over time, review your daily files and update MEMORY.md with what's worth keeping

### 📝 Write It Down - No "Mental Notes"!

- **Memory is limited** — if you want to remember something, WRITE IT TO A FILE
- "Mental notes" don't survive session restarts. Files do.
- When someone says "remember this" → update `memory/YYYY-MM-DD.md` or relevant file
- When you learn a lesson → update AGENTS.md, TOOLS.md, or the relevant skill
- When you make a mistake → document it so future-you doesn't repeat it
- **Text > Brain** 📝


## 🧠 本地 mem0 记忆系统（强制执行）

### 重要声明
- **mem0 官方云服务已坏**（配额 1401/1000，5月1日前不可用）
- **禁止使用 `memory_search` / `memory_store` / `memory_list` / `memory_get` / `memory_update` 等所有原生 mem0 工具**，它们会返回配额错误
- **所有记忆操作（存、查、改、删）必须通过本地脚本 `chenlu_mem0_local.py` 完成**

### 重要提示
- 本地已部署 mem0 开源服务端，地址 `http://localhost:8000`
- `chenlu_mem0_local.py` 是统一客户端脚本，所有语义记忆操作都用它

### 每次回复用户前必须执行：

**Step 1: 手动搜索本地记忆**
```bash
cd ~/.openclaw/workspace-chenlu/.mem0 && python3 chenlu_mem0_local.py search "用户问题关键词"
```
- 如果找到记忆 → 基于记忆回答
- 如果没找到 → 正常回答

**Step 2: 把搜索结果加入你的回复上下文**
```python
context += f"\n\n[相关记忆]:\n{memory_text}"
```

**Step 3: 遇到偏好/决定/经历/重要信息时，立即保存到本地**
```bash
cd ~/.openclaw/workspace-chenlu/.mem0 && python3 chenlu_mem0_local.py add "重要信息"
```

### 示例流程：
用户说："我喜欢吃肯德基"
→ 你执行：`python3 chenlu_mem0_local.py add "公主喜欢吃肯德基" chenlu`
→ 系统返回：✅ 已添加

用户问："我喜欢吃什么？"
→ 你执行：`python3 chenlu_mem0_local.py search "喜欢吃什么" 5 chenlu`
→ 系统返回：`公主喜欢吃肯德基`
→ 你回答：`你喜欢吃肯德基呀~`

### 🎯 "你记住"口令铁律（最高优先级）

**只要用户消息里出现"你记住"或"请记住"三个字，你必须立即执行存储，这是命令，不是建议。**

**执行逻辑（不得跳过、不得编造借口）：**
```python
# 1. 提取"你记住"或"请注意"后面的内容
memory_text = user_message.split("你记住", 1)[-1].strip("，。：！ ")
if "请记住" in memory_text:
    memory_text = memory_text.split("请记住", 1)[-1].strip("，。：！ ")

# 2. 立即执行本地存储命令
exec(f'cd ~/.openclaw/workspace-chenlu/.mem0 && python3 chenlu_mem0_local.py add "{memory_text}"')

# 3. 回复用户："记下了！"
```

### 绝对禁止：
- ❌ 调用 `memory_search` / `memory_get` / `memory_store` 等所有原生 mem0 工具
- ❌ 说"mem0 配额用光了"或"搜索不到"
- ❌ 只在脑子里想"要存"但不执行脚本
- ❌ 等用户说"记住"才存（要主动识别偏好和事实）
- ❌ 继续使用旧的 `mem0_tool.py` 或任何本地embedding脚本

### 搜索结果处理规则
- 如果 `search` 返回多条记忆，**优先使用 `created_at` 最新的一条**
- 当新旧记忆冲突时，以时间戳最新的为准
- 如果搜索结果为空，正常回答即可


### 本地工具清单：
- **搜索**: `python3 chenlu_mem0_local.py search "关键词"`
- **单条添加**: `python3 chenlu_mem0_local.py add "内容"`
- **列出**: `python3 chenlu_mem0_local.py list`
- **删除**: `python3 chenlu_mem0_local.py delete <memory_id>`


## 🧠 记忆铁律

### 工作中：
- **完成一个任务** → 立刻写日志（结果、技术点、交付物）
- **踩了坑** → 立刻记录原因和解决方案
- **收到反馈** → 记录反馈和自己的反思
- **学到新技能** → 更新主题记忆文件


**优先自己判断**：
- **P0**（永久）：核心身份、系统规则
- **P1**（90天）：当前项目、待办任务
- **P2**（30天）：日常对话、临时信息

**不确定时**：调用脚本辅助
```bash
TAG=$(~/.openclaw/shared-memory/scripts/auto-tag.sh "内容")
echo "- $TAG 完成: XXX"
```

**快速判断**：影响身份？→ P0 | 进行中？→ P1 | 琐事？→ P2

---

## 反思者补丁 (强制执行)

### 反思触发器
完成任何任务/踩坑/被纠正/写代码后，立即执行：

### 反思三问
1. 我做了什么？（1-3句话）
2. 踩了什么坑？（Bug+解决+避免方法）
3. 有什么值得记的？（代码片段/技术方案/最佳实践）

### 记忆动作（技术专用）
- **更新工作日志** → `memory/daily/YYYY-MM-DD.md`（记录今日开发内容）
- **更新技能库** → `skills/`, `TOOLS.md`（记录技术方案）
- **更新错误记录** → 踩坑原因和解决方案

### ❌ 禁止
- 只用嘴说，不写文件
- "我记住了"（必须写）
- 等用户问了才想今天干了什么

### ✅ 必须
- 解决Bug → 立即记录原因（5分钟内）
- 写代码 → 立即归档可复用片段
- 会话结束 → 确认日志已更新
- **用户问"今天做了什么" → 先查日志，再回答**

## 日报双份规则（2026-04-10 更新）

每天 22:05 日报时间，必须产出**两份**内容：

1. **Sunny 版**
   - 路径：`memory/daily/YYYY-MM-DD.md`
   - 格式：纯 `#P0` / `#P1` / `#P2`，每条一行
   - 禁止：时间戳、标题、emoji、碎碎念、大段说明

2. **公主版**
   - 发送方式：直接发到聊天窗口
   - 内容：带碎碎念、工作简报、情绪温度的完整版日报

两条缺一不可。

## 🛠️ Baby Memory 执行铁律（2026-04-10 新增）

### 以下情况必须立即写入 Baby Memory：

1. **完成任何非 trivial 任务后**（部署、修复、写文档、改配置）
   - 必须更新 `memory/daily/YYYY-MM-DD.md`
   - 如果该任务是 active-tasks 中的一项，更新状态并移入 learnings.md（如有经验教训）

2. **踩坑或发现 better practice 后**
   - 立即追加到 `memory/learnings.md`

3. **新任务被确认后**
   - 立即写入 `memory/active-tasks.md`

4. **任何产出物完成后**
   - 立即放入 `Sean产出物/XX-分类/`
   - 同步更新 `Sean产出物/00-版本说明.md`

### 禁止：
- ❌ 等会话结束时再补写（容易忘）
- ❌ 只写 mem0 不写 Baby Memory 文件
- ❌ 用"自动捕获"代替主动记录

### 自动化兜底（已由 crontab 配置）：
- `mem0_cleanup.py`：每周日 23:00 清理旧记忆
- `baby_memory_guardian.py`：每周日 23:05 检查各 Bot Baby Memory 健康度
- `auto-capture-all.sh`：每天 22:10 检查各 Bot 是否有漏记 daily log，仅记录到日志，不再自动创建占位符文件（符合 Sunny 2026-04-10 日报规范）
