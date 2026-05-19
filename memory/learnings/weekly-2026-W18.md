# Weekly Learnings - 2026-W19

> 创建于 2026-05-08 | Dashboard v7 最终定稿日

---

## 🔥 核心教训（Dashboard 开发专用）

### 教训1：永远回退到已知良好的快照，不要在当前版本上修补
- **背景**：Baby 卡片结构损坏后，多次尝试修补导致更多问题
- **正确做法**：立即回退到定稿版本，重新修改，而不是在当前损坏的版本上继续打补丁
- **执行**：回退到 `dashboard-v5_最终定稿_大按钮_底边对齐_高度360px_20260508_1355.html`

### 教训2：CSS 修改必须单点、隔离、可回退
- **背景**：修改 .flip-card-back padding 时连带改了 3 个地方，导致其他卡片出问题
- **正确做法**：每次只改一个 CSS 规则，改完验证效果，再改下一个
- **错误做法**：批量替换多个 CSS 块，后果不可预测

### 教训3：margin-top: auto 只在 flex 布局中生效
- **背景**：.flip-card-back 不是 flex 布局时，margin-top: auto 不生效，导致按钮位置不对齐
- **正确做法**：非 flex 容器用固定 margin-top: 16px，flex 容器才用 margin-top: auto
- **最终方案**：flip-card-front 和 flip-card-back 都用 flex + margin-top: auto

### 教训4：验证层级关系 - 后端认证会拦截前端页面
- **背景**：在 Python 后端加了 HTTP 401 认证，导致页面返回 JSON 错误
- **正确做法**：Dashboard 这种单页应用用纯前端验证（localStorage + JS 弹窗）
- **错误做法**：后端 send_response(401) 会拦截 HTML 页面加载

### 教训5：Playwright 截图时密码层会遮挡元素
- **背景**：密码验证层导致 Playwright 无法定位卡片内的按钮
- **解决**：用 page.evaluate() 直接设置 localStorage 跳过密码层

---

## 🛠️ 技术方案记录

### Dashboard 产出物过滤规则（最终版）
```python
# 排除目录
skip_dirs = {'node_modules', '.git', 'build', 'dist', 'out', 'target', '__pycache__', '.next', '.nuxt', 'vendor', 'libs', 'lib', 'src', 'source'}

# 排除扩展名（代码/配置）
skip_exts = {'.js', '.ts', '.jsx', '.tsx', '.css', '.scss', '.sass', '.less', '.json', '.yaml', '.yml', '.xml', '.map', '.npmignore', '.editorconfig', '.gitignore', '.dockerignore', '.eslintrc', '.prettierrc', '.babelrc'}

# 允许扩展名（交付物）
allow_exts = {'.html', '.htm', '.pdf', '.doc', '.docx', '.ppt', '.pptx', '.xls', '.xlsx', '.md', '.txt', '.png', '.jpg', '.jpeg', '.webp', '.gif', '.mp4', '.mp3', '.wav', '.zip', '.tar', '.gz', '.7z'}
```

### Baby 卡片特殊性
- 面积小（160px vs 360px），不能用大按钮
- 用右上角 28×28px 箭头按钮（正面→，反面←）
- 其他 6 个 Bot 卡片用大按钮（View Deliverables → / ← Back）

---

## 📋 产出物命名规范

###  Dashboard 文件命名
```
dashboard-v5_最终定稿_大按钮_底边对齐_高度360px_YYYYMMDD_HHMM.html
```

### 版本标记规则
| 标记 | 含义 | 使用场景 |
|------|------|---------|
| v1初稿 | 第一版初稿 | 刚完成的原始版本 |
| v2修改 | 第二版修改中 | 根据反馈调整中 |
| v1定稿 | 第一版定稿 | 已确认的最终版本 |
| v2定稿 | 第二版定稿 | 迭代后的最终版本 |

---

## 🎯 Baby Memory 铁律（Dashboard 维护）

1. **完成任何修改后** → 立即验证 HTTP 200，然后截图确认效果
2. **结构损坏时** → 立即回退到快照，不要修补
3. **CSS 修改** → 单点修改，逐个验证
4. **新功能（如密码验证）** → 前后端分离验证，避免后端拦截前端
5. **产出物统计** → 保持过滤规则一致（get_output_files_count 和 get_output_files 共享逻辑）

---

## 📝 今日踩坑时间线

| 时间 | 踩的坑 | 解决方案 |
|------|--------|---------|
| 14:00 | Baby 卡片结构损坏（多余 </div>） | 回退到定稿重新修改 |
| 15:00 | 按钮对齐反复失败 | 分析定稿版本 CSS，恢复正确结构 |
| 16:00 | 产出物数量硬编码 | 改为动态占位符替换 |
| 17:00 | Restart 按钮漏改 | 批量替换所有未改的按钮 |
| 18:00 | 后端认证拦截页面 | 改为纯前端验证 |
| 19:00 | 按钮对齐最终修复 | 统一 flex + margin-top: auto |

---

*晨露记录 - 2026-05-08*
## 2026-05-15 Dashboard v17 定稿补充教训

### 教训6：定稿后任何修改必须先建可回退快照
- **背景**：Dashboard 已定稿后继续微调 Stream、头像、按钮位置，多次出现“修一处影响另一处”。
- **正确做法**：先备份 `index.html + api_server.py + assets + images`，确认后再同步到 `FINAL_LOCKED` 快照。
- **最终方案**：`/home/cheche/dashboard-design-v8/backups/FINAL_LOCKED_20260515_1235/` + `restore_locked_final.sh`。

### 教训7：Stream 不能依赖打包静态数据，必须动态读取真实产出物
- **背景**：页面看到的 Stream 停在 5.13，因为主 bundle 内仍有静态列表。
- **正确做法**：运行时调用 `/api/deliverables/all`，并用 MutationObserver 处理 React 重渲染。
- **展示规则**：过滤版本记录/版本说明/index 入口文件；语义同名去重；先每 Bot 1 条，再按时间顺延补齐 10 条。

### 教训8：UI 微调禁止粗暴全局扫射样式
- **背景**：全局放大 `span/div` 字号导致 Stream 字号忽大忽小。
- **正确做法**：只改目标组件，使用稳定 class/keyframes；光标动画独立为 `.dashboard-live-caret`。
