# OpenClaw 6 Bots 配置总览（含模型 Key）

- 生成时间：2026-03-27 10:12 (Asia/Shanghai)
- **更新时间：2026-03-31 20:46 (Asia/Shanghai)** - Baby 配置修复：主模型 codex-newcli-com/gpt-5.3-codex，备用 kimi-coding
- 注意：本文件包含敏感密钥（API Key / Gateway Token / Feishu 配置），请勿外传。

## 1) 总体映射

| Bot | 服务名 | Gateway | Workspace | 运行绑定 | 生效配置文件 |
|---|---|---:|---|---|---|
| CHENLU | `openclaw-gateway-main.service` | `18794` | `/home/cheche/.openclaw/workspace-chenlu` | `OPENCLAW_HOME=/home/cheche/.openclaw-main` | `/home/cheche/.openclaw-main/.openclaw/openclaw.json` |
| SUNNY | `openclaw-gateway-bot2.service` | `18780` | `/home/cheche/.openclaw/workspace-sunny` | `--profile bot2` | `/home/cheche/.openclaw-bot2/openclaw.json` |
| RAINBOW | `openclaw-gateway-rainbow.service` | `18790` | `/home/cheche/.openclaw/workspace-rainbow` | `OPENCLAW_HOME=/home/cheche/.openclaw-rainbow` | `/home/cheche/.openclaw-rainbow/.openclaw/openclaw.json` |
| MUMU | `openclaw-gateway-mumu.service` | `18795` | `/home/cheche/.openclaw/workspace-mumu` | `OPENCLAW_HOME=/home/cheche/.openclaw-mumu` | `/home/cheche/.openclaw-mumu/.openclaw/openclaw.json` |
| MELODY | `openclaw-gateway-melody.service` | `18810` | `/home/cheche/.openclaw/workspace-melody` | `OPENCLAW_HOME=/home/cheche/.openclaw-melody` | `/home/cheche/.openclaw-melody/.openclaw/openclaw.json` |
| BABY | `openclaw-gateway-baby.service` | `18820` | `/home/cheche/.openclaw/workspace-baby` | `OPENCLAW_HOME=/home/cheche/.openclaw-baby` | `/home/cheche/.openclaw-baby/.openclaw/openclaw.json` |

---

## 2) CHENLU（Main）

### 服务与路径
- 服务文件：`/home/cheche/.config/systemd/user/openclaw-gateway-main.service`
- `ExecStart`：`/home/cheche/.npm-global/bin/openclaw gateway run --port 18794`
- `WorkingDirectory`：`/home/cheche/.openclaw-main`
- 运行配置：`/home/cheche/.openclaw-main/.openclaw/openclaw.json`

### Gateway
- 端口：`18794`
- 模式：`local`
- Token：`chenlu_token_2026`

### Agent
- `id`: `main`
- `name`: `Chenlu`
- `workspace`: `/home/cheche/.openclaw/workspace-chenlu`
- 显式模型：`kimi-coding/kimi-for-coding`
- 默认模型策略：
  - `primary`: `kimi-coding/kimi-for-coding`
  - `fallbacks`: `fox-gemini/gemini-3.1-pro`

### 模型提供方与 Key
- `kimi-coding`
  - `baseUrl`: `https://api.kimi.com/coding/v1`
  - `api`: `anthropic-messages`
  - `models`: `kimi-for-coding`
  - `apiKey`: `sk-kimi-ezBq4P6GDUOi4cNkCIpNLhfhwdld9844idEPYPDLlv7cpiLve1opHfPUGFjyS7sM`
- `fox-gemini`
  - `baseUrl`: `https://code.newcli.com/gemini/v1beta`
  - `api`: `google-generative-ai`
  - `models`: `gemini-3.1-pro`
  - `apiKey`: `sk-ant-oat01-HETLc_eek8lSB4dcqlEyK9PRQcUifVxlpl-t2X5KiVOYRPjaQXmE7tkAmPCvJRS5kw3YAXEYgoTVYUGiekJshYHZVAQ13AA`

### Feishu
- `appId`: `cli_a9285620cd785cb3`
- `connectionMode`: `websocket`
- `dmPolicy`: `null`
- `allowFrom`: `null`

### 凭据文件
- `/home/cheche/.openclaw-main/.openclaw/credentials/feishu-default-allowFrom.json`
- `/home/cheche/.openclaw-main/.openclaw/credentials/feishu-pairing.json`

### 最新运行模型日志
- `2026-03-25T18:00:03.526+08:00 [gateway] agent model: kimi-coding/kimi-for-coding`

---

## 3) SUNNY（bot2）

### 服务与路径
- 服务文件：`/home/cheche/.config/systemd/user/openclaw-gateway-bot2.service`
- `ExecStart`：`/home/cheche/.npm-global/bin/openclaw --profile bot2 gateway run --port 18780`
- 生效配置：`/home/cheche/.openclaw-bot2/openclaw.json`

### Gateway
- 端口：`18780`
- 模式：`local`
- Token：`cbe6d99f499e17b531304d4a93cd0a94b8274258060a9f26`

### Agent
- `id`: `bot2`
- `name`: `Sunny`
- `workspace`: `/home/cheche/.openclaw/workspace-sunny`
- 显式模型：`fox-gemini/gemini-3.1-pro`
- 默认模型策略：
  - `primary`: `fox-gemini/gemini-3.1-pro`
  - `fallbacks`: `kimi-coding/kimi-for-coding`

### 模型提供方与 Key
- `fox-gemini`
  - `baseUrl`: `https://code.newcli.com/gemini/v1beta`
  - `api`: `google-generative-ai`
  - `models`: `gemini-3.1-pro`
  - `apiKey`: `sk-ant-oat01-HETLc_eek8lSB4dcqlEyK9PRQcUifVxlpl-t2X5KiVOYRPjaQXmE7tkAmPCvJRS5kw3YAXEYgoTVYUGiekJshYHZVAQ13AA`
- `kimi-coding`
  - `baseUrl`: `https://api.kimi.com/coding/v1`
  - `api`: `anthropic-messages`
  - `models`: `kimi-for-coding`
  - `apiKey`: `sk-kimi-qI9SNbM6FWYoZTvku4lq8SjM6wmeqkGI0Mk2RRABxziZqPtbm8ZEDXcGUrojdukp`

### Feishu
- `appId`: `cli_a92b91fa7578dbcb`
- `connectionMode`: `websocket`
- `dmPolicy`: `pairing`
- `allowFrom`: `ou_e40c5df02fc12d4786a84a078a9b180d`

### 凭据文件
- `/home/cheche/.openclaw-bot2/credentials/feishu-pairing.json`

### 最新运行模型日志
- `2026-03-25T17:35:20.615+08:00 [gateway] agent model: fox-gemini/gemini-3.1-pro`

---

## 4) RAINBOW

### 服务与路径
- 服务文件：`/home/cheche/.config/systemd/user/openclaw-gateway-rainbow.service`
- `ExecStart`：`/home/cheche/.npm-global/bin/openclaw gateway run --port 18790`
- `WorkingDirectory`：`/home/cheche/.openclaw-rainbow`
- 生效配置：`/home/cheche/.openclaw-rainbow/.openclaw/openclaw.json`

### Gateway
- 端口：`18790`
- 模式：`local`
- Token：`rainbow_token_2026`

### Agent
- `id`: `bot2`（注意：当前配置里 Rainbow 的 id 仍是 `bot2`）
- `name`: `Rainbow`
- `workspace`: `/home/cheche/.openclaw/workspace-rainbow`
- 显式模型：`fox-gemini/gemini-3.1-pro`
- 默认模型策略：
  - `primary`: `fox-gemini/gemini-3.1-pro`
  - `fallbacks`: `kimi-coding/kimi-for-coding`

### 模型提供方与 Key
- `fox-gemini`
  - `baseUrl`: `https://code.newcli.com/gemini/v1beta`
  - `api`: `google-generative-ai`
  - `models`: `gemini-3.1-pro`
  - `apiKey`: `sk-ant-oat01-HETLc_eek8lSB4dcqlEyK9PRQcUifVxlpl-t2X5KiVOYRPjaQXmE7tkAmPCvJRS5kw3YAXEYgoTVYUGiekJshYHZVAQ13AA`
- `kimi-coding`
  - `baseUrl`: `https://api.kimi.com/coding/v1`
  - `api`: `anthropic-messages`
  - `models`: `kimi-for-coding`
  - `apiKey`: `sk-kimi-JqzEUH7jkjyECGcnRkcuOkMXOjBwcN02dK2oycXV99aEVSDKUjVmVgElBxytYkwY`

### Feishu
- `appId`: `cli_a93d539aeef81cce`
- `connectionMode`: `websocket`
- `dmPolicy`: `null`
- `allowFrom`: `null`

### 凭据文件
- `/home/cheche/.openclaw-rainbow/.openclaw/credentials/feishu-default-allowFrom.json`
- `/home/cheche/.openclaw-rainbow/.openclaw/credentials/feishu-pairing.json`

### 最新运行模型日志
- `2026-03-24T23:57:54.623+08:00 [gateway] agent model: fox-gemini/gemini-3.1-pro`

---

## 5) MUMU

### 服务与路径
- 服务文件：`/home/cheche/.config/systemd/user/openclaw-gateway-mumu.service`
- `ExecStart`：`/home/cheche/.npm-global/bin/openclaw gateway run --port 18795`
- `WorkingDirectory`：`/home/cheche/.openclaw-mumu`
- 生效配置：`/home/cheche/.openclaw-mumu/.openclaw/openclaw.json`

### Gateway
- 端口：`18795`
- 模式：`local`
- Token：`mumu_token_2026`

### Agent
- `id`: `mumu`
- `name`: `Mumu`
- `workspace`: `/home/cheche/.openclaw/workspace-mumu`
- 显式模型：`kimi-coding/kimi-for-coding`
- 默认模型策略：
  - `primary`: `kimi-coding/kimi-for-coding`
  - `fallbacks`: `moonshot/kimi-k2.5`

### 模型提供方与 Key
- `kimi-coding`
  - `baseUrl`: `https://api.kimi.com/coding/v1`
  - `api`: `anthropic-messages`
  - `models`: `kimi-for-coding`
  - `apiKey`: `sk-kimi-ibhDAQi2o57Qh0YPIOB30Trtdmd0Aclh0FdOi6b76uLqsDAdSJVTMFONtzo0n5mk`
- `moonshot` (备用)
  - `baseUrl`: `https://api.moonshot.cn/v1`
  - `api`: `openai-completions`
  - `models`: `kimi-k2.5`
  - `apiKey`: `sk-vArOg0KjhxvLNnhZYN14ibd0i8WdhT2u3zM95tqH6EI69BzR`

### Feishu
- `appId`: `cli_a94a090316f85cba`
- `connectionMode`: `websocket`
- `dmPolicy`: `null`
- `allowFrom`: `null`

### 凭据文件
- `/home/cheche/.openclaw-mumu/.openclaw/credentials/feishu-default-allowFrom.json`
- `/home/cheche/.openclaw-mumu/.openclaw/credentials/feishu-pairing.json`

### 最新运行模型日志
- `2026-03-29T20:19:17.569+08:00 [gateway] agent model: kimi-coding/kimi-for-coding`

---

## 6) MELODY

### 服务与路径
- 服务文件：`/home/cheche/.config/systemd/user/openclaw-gateway-melody.service`
- `ExecStart`：`/home/cheche/.npm-global/bin/openclaw gateway run --port 18810`
- `WorkingDirectory`：`/home/cheche/.openclaw-melody`
- 生效配置：`/home/cheche/.openclaw-melody/.openclaw/openclaw.json`

### Gateway
- 端口：`18810`
- 模式：`local`
- Token：`melody_b09ef3c4_b56c_44c6_9ac8_2b1ce823ef56`

### Agent
- `id`: `melody`
- `name`: `Melody`
- `workspace`: `/home/cheche/.openclaw/workspace-melody`
- 显式模型：`kimi-coding/kimi-for-coding`
- 默认模型策略：
  - `primary`: `kimi-coding/kimi-for-coding`
  - `fallbacks`: `moonshot/kimi-k2.5`

### 模型提供方与 Key
- `kimi-coding`
  - `baseUrl`: `https://api.kimi.com/coding/v1`
  - `api`: `anthropic-messages`
  - `models`: `kimi-for-coding`
  - `apiKey`: `sk-kimi-jPo6t8EgeSTYPmZJLJgoMv57IVJ4FhGUJTtdYSFqIougt5rGGBUlkcEVaNZQVcF5`
- `moonshot` (备用)
  - `baseUrl`: `https://api.moonshot.cn/v1`
  - `api`: `openai-completions`
  - `models`: `kimi-k2.5`
  - `apiKey`: `sk-vArOg0KjhxvLNnhZYN14ibd0i8WdhT2u3zM95tqH6EI69BzR`

### Feishu
- `appId`: `cli_a94e775fe1b95cce`
- `connectionMode`: `websocket`
- `dmPolicy`: `null`
- `allowFrom`: `null`

### Channels
- `channels status --probe`：`Gateway reachable`
- Feishu 状态：`enabled, configured, running, works`

### 最新运行模型日志
- `2026-03-29T20:19:16.377+08:00 [gateway] agent model: kimi-coding/kimi-for-coding`

---

## 7) BABY

### 服务与路径
- 服务文件：`/home/cheche/.config/systemd/user/openclaw-gateway-baby.service`
- `ExecStart`：`/home/cheche/.npm-global/bin/openclaw gateway run --port 18820`
- `WorkingDirectory`：`/home/cheche/.openclaw-baby`
- 生效配置：`/home/cheche/.openclaw-baby/.openclaw/openclaw.json`

### Gateway
- 端口：`18820`
- 模式：`local`
- Token：`baby_d9e798b6_30fc_46a0_a1c3_c246b09dd395`

### Agent
- `id`: `baby`
- `name`: `Baby`
- `workspace`: `/home/cheche/.openclaw/workspace-baby`
- 显式模型：`codex-newcli-com/gpt-5.3-codex`
- 默认模型策略：
  - `primary`: `codex-newcli-com/gpt-5.3-codex`
  - `fallbacks`: `kimi-coding/kimi-for-coding`

### 模型提供方与 Key
- `codex-newcli-com` (GPT-5.3-codex，主模型)
  - `baseUrl`: `https://code.newcli.com/codex/v1`
  - `api`: `openai-completions`
  - `models`: `gpt-5.3-codex`
  - `apiKey`: `sk-ant-oat01-vM4edLgSnqS2MpNlI-rseo2NyzRELZRsF8FAX3GoXN84BpZK8gQMt2O9uNx85Pv6G5IBypCCEqkUYWVWUB7oL5scadQtDAA`
- `kimi-coding` (备用)
  - `baseUrl`: `https://api.kimi.com/coding/v1`
  - `api`: `anthropic-messages`
  - `models`: `kimi-for-coding`
  - `apiKey`: `sk-kimi-JqzEUH7jkjyECGcnRkcuOkMXOjBwcN02dK2oycXV99aEVSDKUjVmVgElBxytYkwY`

### Feishu
- `appId`: `cli_a94f590dfefa1bb4`
- `connectionMode`: `websocket`
- `dmPolicy`: `null`
- `allowFrom`: `null`

### Channels
- `channels status --probe`：`Gateway reachable`
- Feishu 状态：`enabled, configured, running, works`

### 最新运行模型日志
- `2026-03-29T19:48:26.857+08:00 [gateway] agent model: fox-gemini/gemini-3.1-pro`

---

## 8) 备注

- 模型策略总览：
  - CHENLU：Kimi 主，Gemini 备
  - SUNNY：Gemini 主，Kimi 备
  - RAINBOW：Gemini 主，Kimi 备
  - MUMU：Kimi 主，Moonshot 备
  - MELODY：Kimi 主，Moonshot 备
  - **BABY：codex-newcli-com/gpt-5.3-codex 主，Kimi 备**（2026-03-31 配置确定）
- SUNNY 已做 `allowFrom` 固化，减少反复 `access not configured`。
