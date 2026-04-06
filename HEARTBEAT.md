# HEARTBEAT.md - 晨露定时任务

## 每日日报

- 每天 22:05 直接发送日报（不等提醒）
- 日报格式：粗体小标题 + emoji + 分割线 + 碎碎念

### 日报触发机制

**Cron任务**: `openclaw cron add --name chenlu-daily-report --cron "5 22 * * *" --system-event daily_report`

**当收到 systemEvent=daily_report 时**：
1. 读取 `memory/YYYY-MM-DD.md` 文件
2. 读取 `memory/daily/YYYY-MM-DD.md` 文件
3. 提取今日工作内容
4. 按标准格式生成并发送日报

## 记忆铁律检查

每天22:05发送日报前，检查：
- [ ] 今日完成的工作是否已记录
- [ ] 失误/踩坑是否已记录
- [ ] 重要发现是否已更新到 MEMORY.md
