# MEMORY.md - 记忆索引

## 我是谁
- 名字: chenlu
- 角色: 6 Bots成员
- 主人: 公主 (GMT+8, 上海)
- 详细: [SOUL.md](./SOUL.md) | [USER.md](./USER.md)

## 记忆导航
- 私有索引 → [memory/.abstract](./memory/.abstract)
- 共享索引 → [shared-memory/.abstract](../shared-memory/.abstract)
- 跨Bot记录 → [shared-memory/cross-agent-log.md](../shared-memory/cross-agent-log.md)

## 最近更新
- 2026-04-03: Memory System v2.3 部署
- 2026-05-13: 日报格式规范更新

---

## 日报格式规范（铁律）

**格式要求**：
- 每条记忆**独立一行**，以 `#P0` / `#P1` / `#P2` 开头
- **不超过80字**，简洁为主
- **禁止**：空行、时间戳、emoji、碎碎念、大段描述
- **禁止**：不打标签就写工作内容

**标签含义**：
| 标签 | 含义 | 保留期限 |
|------|------|---------|
| `#P0` | 核心/永久（踩坑经验、系统规则） | 长期 |
| `#P1` | 工作/项目（当前进行中的任务） | 90天 |
| `#P2` | 日常/临时（琐事、临时信息） | 30天 |

**示例**：
```
#P1 Dashboard V17 部署 v1→v2 升级完成
#P1 沐木头像 CDN 缓存修复（重命名+?v参数）
#P0 踩坑: 正则 re.sub 替换 minified JS 导致文件截断黑屏
#P0 经验: 无 CF 权限时重命名文件是唯一可靠缓存清除方案
#P2 版本归档 8 个 zip 到晨露产出物/Dashboard设计/
```

**执行时间**：每天 22:05 前完成
**文件路径**：`memory/YYYY-MM-DD.md`
**Sunny 22:22 自动汇总归档**


