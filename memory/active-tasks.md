# Active Tasks - 进行中任务

> 当前活跃的项目和任务，P1 级别（保留90天）
> 完成或取消的任务及时归档到 learnings.md 或删除

## 进行中

- [P0] **Dashboard 和 Heartflow 服务维护**
  - 描述：确保 dashboard 和 heartflow 公网访问稳定
  - 子任务：
    - [ ] 监控 `cloudflared-dashboard.service` 运行状态
    - [ ] 监控 `openclaw-dashboard.service` 运行状态
    - [ ] 监控 `heartflow-server.service` 运行状态
    - [ ] 处理 Clash TUN 模式导致的 Tunnel 连接问题
  - 状态：🔄 进行中
  - 说明：dashboard.cheche-dashboard.site 和 heartflow.cheche-dashboard.site

- [P1] **6 Bots 技术排障支持**
  - 描述：配合 Baby 进行系统维护和修复
  - 子任务：
    - [ ] 各 Bot 服务状态检查
    - [ ] 飞书插件问题排查
    - [ ] 权限和授权问题处理
  - 状态：🔄 持续
  - 说明：作为技术手，配合其他 Bots 解决技术问题

- [P1] **记忆系统 v3.0 日常运维**（升级完成，进入习惯养成阶段）
  - 描述：Baby 已完成记忆系统升级，晨露负责日常使用与维护
  - 子任务：
    - [ ] 每次会话优先调用 `chenlu_mem0_local.py search` 查询记忆
    - [ ] 遇到偏好/决定/踩坑，立即 `chenlu_mem0_local.py add` 存储
    - [ ] 每天 22:05 前检查 `memory/daily/YYYY-MM-DD.md` 是否已更新
    - [ ] 每周日配合 `baby_memory_guardian.py` 检查记忆健康度
  - 状态：🔄 进行中
  - 下一步：养成条件反射式记录习惯

## 待开始

*暂无*

## 已完成（本周归档）

- [P1] **记忆系统整改跟进**（2026-04-13 完成升级配合）
  - 结果：Baby 完成记忆系统 v3.0 升级，本地 mem0 Server 和 Baby Memory 已就绪
  - 归档到：learnings.md

- [P1] **Dashboard v2.3 定稿部署**（2026-04-16 完成）
  - 结果：完成 Dashboard 版本更新，Bot 名称更新（Sunny→Charles🦊, Rainbow→Asin🥕）
  - 归档到：运维手册/openclaw-dashboard速查.md

## 已暂停

*暂无*

---

**更新规则**：
- 新任务 → 添加到"进行中"
- 完成任务 → 记录到 learnings.md（踩坑/经验），然后移到"已完成"
- 取消任务 → 直接删除

**最后更新**: 2026-04-16