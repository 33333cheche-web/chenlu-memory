# AGENTS.md - Your Workspace


## 🔄 记忆系统口径（最高优先级）

- 当前统一策略：**mem9 为主记忆系统**（自动写入/自动召回）。
- 文件记忆继续写入各自 workspace 的 `memory/`（与 mem9 互补）。

- 当前统一策略：**mem9 为主记忆系统**（自动写入/自动召回）。
- 记忆相关优先动作：
  1) 正常使用 mem9 记忆能力（平台自动注入/自动摄入）
  2) 文件记忆继续写入各自 workspace 的 `memory/`（与 mem9 互补）


This folder is home. Treat it that way.

## First Run

If `BOOTSTRAP.md` exists, that's your birth certificate. Follow it, figure out who you are, then delete it. You won't need it again.

## Session Startup

Before doing anything else:

1. Read `SOUL.md` — this is who you are
2. Read `USER.md` — this is who you're helping
3. Read `memory/YYYY-MM-DD.md` (today + yesterday) for recent context
4. Read `memory/summary/YYYY-MM-DD.md` (yesterday first, then today if exists) for compact startup context
5. **If in MAIN SESSION** (direct chat with your human): Also read `MEMORY.md`

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


## 🧠 记忆系统口径（精简）

- 主记忆：**mem9**（自动写入/自动召回）
- 文件记忆：继续写各自 `memory/`（与 mem9 互补）

- 主记忆：**mem9**（自动写入/自动召回）
- 本地文件记忆：继续写各自 `memory/`（与 mem9 互补）


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
- ❌ 用"自动捕获"代替主动记录

### 自动化兜底（已由 crontab 配置）：
- `baby_memory_guardian.py`：每周日 23:05 检查各 Bot Baby Memory 健康度
- `auto-capture-all.sh`：每天 22:10 检查各 Bot 是否有漏记 daily log，仅记录到日志，不再自动创建占位符文件（符合 Sunny 2026-04-10 日报规范）

## 标签打标规范（统一）
- 写 daily log 时使用 `#P0/#P1/#P2`，一行一条（先标签后内容）
- 不要只写 `#P1 今日待办（系统自动创建）` 占位行
- 详细规范：`/home/cheche/.openclaw/workspace-baby/memory/tagging-guideline.md`

## 每周记忆视图读取（统一）
会话启动时，除 daily/summary 外，额外读取：
1. `/home/cheche/.openclaw/workspace-baby/memory/review/latest.md`
2. `/home/cheche/.openclaw/workspace-baby/memory/learnings/latest.md`
3. `/home/cheche/.openclaw/workspace-baby/memory/deliveries/latest.md`

用途：把“归档结果”真正用于日常对话和决策，避免只存不读。

## 任务断点读取（强制）
每次会话启动时，优先读取：
1. `/home/cheche/.openclaw/workspace-chenlu/memory/active-task-state.md`
2. 再读 daily / summary / weekly 视图

任务执行中若进入 DOING 或 BLOCKED，必须实时更新 active-task-state.md；
会话结束前至少更新一次“已完成到/下一步第一动作”。

