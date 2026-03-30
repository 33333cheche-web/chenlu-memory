# OpenClaw 6-Bot Runbook（稳定运维版）

- 更新时间：2026-03-29（Baby/Melody/Mumu 添加 moonshot 备用模型）
- 目标：让后续 AI 在不破坏现有架构的前提下排障和改配置。
- 先读文件：`/home/cheche/openclaw-6bots-inventory.md`
- 安全提示：配置包含 API Key / token，禁止外传、禁止贴公网。

## 1. 固定架构（不要随意改）

### 1.1 实例与服务映射
| 实例名 | systemd 服务 | Gateway 端口 |
|---|---|---:|
| CHENLU | `openclaw-gateway-main.service` | `18794` |
| SUNNY | `openclaw-gateway-bot2.service` | `18780` |
| RAINBOW | `openclaw-gateway-rainbow.service` | `18790` |
| MUMU | `openclaw-gateway-mumu.service` | `18795` |
| MELODY | `openclaw-gateway-melody.service` | `18810` |
| BABY | `openclaw-gateway-baby.service` | `18820` |

### 1.2 生效配置路径（按运行方式）
- CHENLU：`OPENCLAW_HOME=/home/cheche/.openclaw-main`，生效配置是 `/home/cheche/.openclaw-main/.openclaw/openclaw.json`
- SUNNY：`--profile bot2`，生效配置是 `/home/cheche/.openclaw-bot2/openclaw.json`
- RAINBOW：`OPENCLAW_HOME=/home/cheche/.openclaw-rainbow`，生效配置是 `/home/cheche/.openclaw-rainbow/.openclaw/openclaw.json`
- MUMU：`OPENCLAW_HOME=/home/cheche/.openclaw-mumu`，生效配置是 `/home/cheche/.openclaw-mumu/.openclaw/openclaw.json`
- MELODY：`OPENCLAW_HOME=/home/cheche/.openclaw-melody`，生效配置是 `/home/cheche/.openclaw-melody/.openclaw/openclaw.json`
- BABY：`OPENCLAW_HOME=/home/cheche/.openclaw-baby`，生效配置是 `/home/cheche/.openclaw-baby/.openclaw/openclaw.json`

### 1.3 Workspace 固定映射
- CHENLU：`/home/cheche/.openclaw/workspace-chenlu`
- SUNNY：`/home/cheche/.openclaw/workspace-sunny`
- RAINBOW：`/home/cheche/.openclaw/workspace-rainbow`
- MUMU：`/home/cheche/.openclaw/workspace-mumu`
- MELODY：`/home/cheche/.openclaw/workspace-melody`
- BABY：`/home/cheche/.openclaw/workspace-baby`

## 2. 强约束（后续 AI 必须遵守）

- 只改用户指定实例，其他实例完全不动。
- 先备份，再修改；备份文件名必须带时间戳。
- 只改“生效配置路径”，不要改错到其它历史/嵌套路径。
- 每次只重启对应一个 service，不允许四个一起重启。
- 改完必须验证：
  - `systemctl --user status <service>`
  - `openclaw ... channels status --probe`
  - `journalctl` 中确认 `agent model:` 与预期一致
- 未经明确要求，不改 workspace、agent id、gateway 端口、Feishu appId。
- 不执行破坏性命令（`reset --hard`、删库式清理等）。

## 3. 标准变更流程（SOP）

1. 识别目标实例
- 根据用户描述确定是 CHENLU/SUNNY/RAINBOW/MUMU/MELODY/BABY 哪一个。

2. 定位生效配置
- 按 1.2 映射确定唯一配置文件路径。

3. 备份
- 备份命名：`openclaw.json.pre-<change>-YYYYMMDD-HHMMSS.bak`

4. 修改
- 仅修改用户要求字段（例如模型、fallback、某个 key）。

5. 重启单实例
- 只重启目标 service。

6. 验证
- service active
- channel probe works
- 启动日志有 `agent model:` 且与目标一致

7. 回报
- 给出：改了什么、文件路径、备份路径、验证结果、是否仍有风险。

## 4. 快速命令（按实例）

### 4.1 CHENLU
- 配置路径：`/home/cheche/.openclaw-main/.openclaw/openclaw.json`
- 重启：`systemctl --user restart openclaw-gateway-main.service`
- 状态：`systemctl --user status openclaw-gateway-main.service --no-pager -n 60`

### 4.2 SUNNY
- 配置路径：`/home/cheche/.openclaw-bot2/openclaw.json`
- 重启：`systemctl --user restart openclaw-gateway-bot2.service`
- 状态：`systemctl --user status openclaw-gateway-bot2.service --no-pager -n 60`

### 4.3 RAINBOW
- 配置路径：`/home/cheche/.openclaw-rainbow/.openclaw/openclaw.json`
- 重启：`systemctl --user restart openclaw-gateway-rainbow.service`
- 状态：`systemctl --user status openclaw-gateway-rainbow.service --no-pager -n 60`

### 4.4 MUMU
- 配置路径：`/home/cheche/.openclaw-mumu/.openclaw/openclaw.json`
- 重启：`systemctl --user restart openclaw-gateway-mumu.service`
- 状态：`systemctl --user status openclaw-gateway-mumu.service --no-pager -n 60`

### 4.5 MELODY
- 配置路径：`/home/cheche/.openclaw-melody/.openclaw/openclaw.json`
- 重启：`systemctl --user restart openclaw-gateway-melody.service`
- 状态：`systemctl --user status openclaw-gateway-melody.service --no-pager -n 60`

### 4.6 BABY
- 配置路径：`/home/cheche/.openclaw-baby/.openclaw/openclaw.json`
- 重启：`systemctl --user restart openclaw-gateway-baby.service`
- 状态：`systemctl --user status openclaw-gateway-baby.service --no-pager -n 60`

## 5. 给下一个 AI 的交接模板（复制即用）

```text
先读：
1) /home/cheche/openclaw-6bots-inventory.md
2) /home/cheche/openclaw-runbook.md

当前问题：<粘贴完整报错 + 时间 + 实例名>
只允许改：<CHENLU/SUNNY/RAINBOW/MUMU/MELODY/BABY>
目标：<一句话，例如“切到 kimi 主模型，gemini fallback”>
约束：先备份；只改生效配置；只重启对应 service；输出验证日志。
禁止：不要改其它实例，不要改 workspace/端口/appId。
```

## 6. 当前模型策略基线（2026-03-29 更新）

- CHENLU：Kimi 主，Gemini 备
- SUNNY：Gemini 主，Kimi 备
- RAINBOW：Gemini 主，Kimi 备
- **MUMU：Kimi 主，Moonshot 备**（2026-03-29 添加）
- **MELODY：Kimi 主，Moonshot 备**（2026-03-29 添加）
- **BABY：Gemini 主，Kimi 备**（2026-03-29 从 Moonshot 切换）

如需调整基线，必须同步更新：
- `/home/cheche/openclaw-6bots-inventory.md`
- `/home/cheche/openclaw-runbook.md`
