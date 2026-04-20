# OpenClaw Dashboard 项目速查

## 📍 项目信息
- **文件名**: `openclaw-dashboard.py`
- **完整路径**: `/home/cheche/openclaw-dashboard.py`
- **访问地址**: https://dashboard.cheche-dashboard.site
- **域名**: cheche-dashboard.site (Cloudflare 管理)
- **认证**: HTTP Basic Auth (用户名: cheche / 密码: iloveyou)

## 🔧 服务组件

| 服务名 | 作用 | 状态命令 |
|--------|------|----------|
| `openclaw-dashboard.service` | Dashboard 本体 (Python HTTP Server) | `systemctl --user status openclaw-dashboard.service` |
| `cloudflared-dashboard.service` | Cloudflare Tunnel (公网访问) | `systemctl --user status cloudflared-dashboard.service` |

## 🚀 快速重启

```bash
# 一键重启两个服务
systemctl --user start openclaw-dashboard.service
systemctl --user start cloudflared-dashboard.service

# 检查状态
systemctl --user status openclaw-dashboard.service
systemctl --user status cloudflared-dashboard.service
```

## ⚠️ 常见故障

### 502 Bad Gateway
- **原因**: Cloudflare Tunnel 或 Dashboard 本体服务挂了
- **解决**: 执行上面的重启命令
- **历史**: 2026-04-15 晚上两个服务同时停止，导致 502

## 📝 部署记录
- **首次部署**: 2026-04-13
- **配置**: systemd 自启动服务
- **域名**: Cloudflare 固定 tunnel (openclaw-dashboard)
- **端口**: 8080 (本地) → Cloudflare Tunnel → 443 (公网)

## 🔄 版本变更
- **2026-04-15**: Sunny → Charles 🦊, Rainbow → Asin 🥕
- **当前版本**: v2.3 (定稿-20260408)

## 🔗 相关记忆
- 创建记录: `memory/2026-04-13.md`
- Rainbow→Asin 修改: `memory/daily/2026-04-15.md`
