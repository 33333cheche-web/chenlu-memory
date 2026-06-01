# Dashboard 部署指南（适配 Python 后端）

## Kimi 生成后的文件结构
```
dist/
├── index.html          ← 入口文件（需要嵌入 API 调用代码）
├── assets/
│   ├── index-xxx.js    ← JS 代码
│   ├── index-xxx.css   ← CSS 样式
│   └── (字体文件)
└── images/
    ├── avatar-commander.jpg
    ├── avatar-charles.jpg
    ├── avatar-asin.jpg
    ├── avatar-sean.jpg
    ├── avatar-mumu.jpg
    ├── avatar-melody.jpg
    └── avatar-chenlu.jpg
```

## 部署步骤（晨露执行）

### 1. 接收文件
- 公主把 Kimi 生成的 `openclaw-dashboard.zip` 发给我
- 或者直接把 `dist/` 文件夹压缩发给我

### 2. 解压到服务器
```bash
# 备份旧版本
mv /home/cheche/dashboard-design-v8 /home/cheche/dashboard-design-v8.bak.日期

# 解压新版本
unzip openclaw-dashboard.zip -d /home/cheche/dashboard-design-v8/
```

### 3. 修改入口文件（关键！）
在 `index.html` 的 `<head>` 中添加 API 调用代码：
```html
<script>
// 全局 fetch 拦截器：自动带认证 token
const AUTH_TOKEN = localStorage.getItem('dashboard_auth') || '';
const originalFetch = window.fetch;
window.fetch = function(url, options = {}) {
  options.headers = options.headers || {};
  if (AUTH_TOKEN && !options.headers['Authorization']) {
    options.headers['Authorization'] = 'Bearer ' + AUTH_TOKEN;
  }
  return originalFetch(url, options);
};

// API 调用示例
async function fetchBotStatus() {
  const res = await fetch('/api/status');
  const data = await res.json();
  return data.bots;
}

async function restartBot(botId) {
  const res = await fetch('/api/restart/' + botId);
  return res.json();
}
</script>
```

### 4. 修改后端路由
```python
# dashboard.py 中 do_GET 方法
if path == '/' or path.startswith('/assets/') or path.startswith('/images/'):
    relative_path = path[1:] if path != '/' else 'index.html'
    self.serve_static_file('/home/cheche/dashboard-design-v8', relative_path)
    return
```

### 5. 重启服务
```bash
systemctl --user restart openclaw-dashboard.service
```

### 6. 验证
- 访问 dashboard.cheche-dashboard.site
- 确认 Bot 状态正常加载
- 确认产出物列表正常
- 确认重启功能正常

## 注意事项

1. **API 路径**：Kimi 生成的静态文件中，所有 API 调用必须使用相对路径 `/api/xxx`

2. **图片路径**：头像图片路径必须是 `/images/avatar-xxx.jpg`

3. **密码验证**：部署完成后需要加回密码验证（当前临时禁用）

4. **如果 Kimi 生成了单文件 HTML**（所有 CSS/JS 内联）：
   - 直接替换 `/home/cheche/dashboard-v9.html`
   - 在 `<head>` 中添加 API 调用代码
   - 重启服务即可

## 快速部署命令（晨露用）

```bash
# 一键部署脚本
cd /home/cheche

# 备份
mv dashboard-design-v8 dashboard-design-v8.bak.$(date +%Y%m%d-%H%M%S)

# 解压新版本（假设文件已上传）
unzip /tmp/openclaw-dashboard.zip -d dashboard-design-v8/

# 重启服务
systemctl --user restart openclaw-dashboard.service

# 验证
curl -s https://dashboard.cheche-dashboard.site/ | head -5
```
