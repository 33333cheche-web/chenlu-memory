# HEARTBEAT.md - 晨露定时任务

## 每日日报

- 每天 22:05 直接发送日报（不等提醒）
- 日报格式：使用 #P0/#P1/#P2 标签格式

### 日报格式规范

```markdown
#P1 完成的具体任务1
#P1 完成的具体任务2
#P2 日常/临时任务

碎碎念：3-5句话，真实有温度
```

**标签说明**：
- **#P0** - 核心/永久（影响身份、系统规则）
- **#P1** - 工作/项目（当前进行中的任务）
- **#P2** - 日常/临时（琐事、临时信息）

### 日报触发机制

**Cron任务**: `openclaw cron add --name chenlu-daily-report --cron "5 22 * * *" --system-event daily_report`

**当收到 systemEvent=daily_report 时**：
1. 读取 `~/.openclaw/workspace-chenlu/memory/daily/YYYY-MM-DD.md` 文件
2. 提取今日工作内容
3. 按标准格式生成并发送日报

## 记忆铁律检查

每天22:05发送日报前，检查：
- [ ] 今日完成的工作是否已记录
- [ ] 失误/踩坑是否已记录
- [ ] 重要发现是否已更新到 MEMORY.md


---

## Memory Healthcheck（每次 heartbeat 必做）

1. **检查今日 daily log**
   - 确认 `memory/daily/$(date +%Y-%m-%d).md` 存在
   - 不存在 → 立即创建并补充当前状态

2. **检查 active-tasks.md**
   - 如果超过 3 天未更新 → 在 daily log 中记录状态
   - 如果有新任务未记录 → 立即追加

3. **检查 learnings.md**
   - 如果本周无新记录 → 检查最近 daily log 是否有踩坑经验，提取并追加

4. **会话结束 checklist（每次和公主对话后）**
   - [ ] 是否完成了任务？→ 更新 active-tasks 状态
   - [ ] 是否踩坑/被纠正？→ 追加到 learnings
   - [ ] 是否帮了其他 Bot？→ 记录到 cross-agent-log

