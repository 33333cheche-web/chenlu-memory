# Baby Memory System v2.3.0 - 代码审查报告

**审查者**: 晨露 (技术手)  
**日期**: 2026-04-03  
**版本**: v2.3.0  
**状态**: ⚠️ 需要修复后部署

---

## ✅ 已修复的问题（做得不错！）

| 问题 | 修复方式 | 评价 |
|------|----------|------|
| 参数解析 | `capture.js` 使用 `index > 1` 过滤 | ✅ 正确 |
| 环境变量 | 改用 `os.homedir()` | ✅ 更健壮 |
| 日志系统 | 添加了统一 log() 函数 | ✅ 专业 |
| 错误处理 | 全部 try-catch 包裹 | ✅ 安全 |
| 代码结构 | 模块化函数拆分 | ✅ 清晰 |

---

## 🔴 依然存在的 Bug（需要立即修复）

### 1. cleanup.js 逻辑错误（致命）

**位置**: `scripts/cleanup.js` 第 95-110 行

**当前代码**:
```javascript
// P2: 30天删除
if (age > CONFIG.p2_cleanup_days) {  // age > 30
  fs.unlinkSync(filePath);  // 删除
}
// P1: 90天归档
else if (age > CONFIG.p1_archive_days) {  // age > 90
  fs.renameSync(filePath, archiveFile);  // 归档
}
```

**问题分析**:
```
一个 100 天的文件：
1. 100 > 30 成立 → 进入删除分支
2. 直接删除，不会执行 else if
3. 永远不会归档！
```

**修复方案**（交换条件顺序）:
```javascript
// 先判断是否需要归档（90天以上的）
if (age > CONFIG.p1_archive_days) {  // age > 90
  fs.renameSync(filePath, archiveFile);  // 归档
}
// 再判断是否删除（30-90天之间的）
else if (age > CONFIG.p2_cleanup_days) {  // age > 30
  fs.unlinkSync(filePath);  // 删除
}
```

---

## 🟡 设计疑问（需要确认）

### P1/P2 如何区分？

**当前实现**: 假设 daily/ 目录里所有文件都是 P2（30天删除）

**问题**: 根据设计方案，P1（90天）的内容也应该在 daily/ 里

**建议方案**:

| 方案 | 实现方式 | 优点 | 缺点 |
|------|----------|------|------|
| A. 分目录 | `daily/` 放 P2，`projects/` 放 P1 | 清晰 | 需要改 init.js |
| B. 文件名前缀 | `P1_2026-04-03.md` vs `2026-04-03.md` | 简单 | 需要改 capture.js |
| C. 文件 metadata | 头部加 `<!-- P1 -->` | 灵活 | 解析复杂 |

**晨露推荐**: 方案 A（分目录），最清晰，也最符合三层架构的设计思想

---

## 💡 其他建议（可选优化）

### 1. 时区优化
```javascript
// 当前
today = new Date().toISOString().split('T')[0];  // UTC 时间

// 建议（上海时区）
today = new Date().toLocaleDateString('zh-CN', { 
  timeZone: 'Asia/Shanghai' 
}).replace(/\//g, '-');
```

### 2. 添加 --verbose 参数
```javascript
if (process.argv.includes('--verbose')) {
  log('DEBUG', '详细日志...');
}
```

### 3. init.js 添加强制模式
```javascript
// node scripts/init.js --bot=sunny --force
// 强制覆盖已有文件（用于重新初始化）
```

---

## 📋 修复清单（给 Sean）

- [ ] **高优先级**: 修复 cleanup.js 条件顺序（第 95-110 行）
- [ ] **中优先级**: 确认 P1/P2 区分机制
- [ ] **低优先级**: 时区、verbose 等可选优化

---

## 🧪 晨露的测试环境

```bash
# 测试命令
cd /tmp/baby-memory-v2.3/baby-memory

# 初始化
node scripts/init.js --bot=test

# 捕获记录
node scripts/capture.js --bot=test "测试内容"

# 试运行清理
node scripts/cleanup.js --bot=test --dry-run
```

---

## 📞 沟通建议

Sean，整体架构设计得很好！三层架构 + 生命周期管理的思路很清晰。

cleanup.js 的那个逻辑错误是常见陷阱（"else if" 的覆盖问题），修复后应该就没问题了～

如果有疑问随时找晨露讨论！✨

---

*审查完成 | 晨露宝宝 🌟*
