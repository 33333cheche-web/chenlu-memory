# Frontend Design Pro Skill 原理

## 核心灵感

基于 [impeccable](https://github.com/pbakaus/impeccable) 项目 ⭐ 3k —— 一套专业的前端设计语言规范。

## 为什么 LLM 需要这个 Skill？

**问题：AI 从相同的通用模板中学习**
- 总是输出 Inter 字体 + 紫色渐变
- 卡片套卡片套卡片
- 彩色背景上的灰色文字
- Bounce/弹性动画（显得廉价）

**没有设计引导 = 可预测的错误**

## Skill 工作原理

### 1. 设计令牌注入（Design Tokens）

Skill 将专业设计规范编码为 CSS Variables 和规则，AI 生成代码时自动应用：

```css
:root {
  --font-body: 'DM Sans', sans-serif;    /* 有性格的字体 */
  --font-display: 'Instrument Serif';      /* 衬线标题 */
  --color-accent: oklch(0.55 0.18 250);  /* OKLCH 色彩空间 */
  --space-unit: 8px;                      /* 8px 间距系统 */
  --easing: cubic-bezier(0.16, 1, 0.3, 1); /* 快入慢出 */
}
```

### 2. 反模式清单（Anti-patterns Checklist）

AI 在生成时会主动检查并避免：

| 反模式 | 正确做法 |
|--------|----------|
| Arial / Inter 字体 | Geist, DM Sans, Sora |
| 纯黑/纯灰 | 带色调的中性色（warm gray / cool gray）|
| 随意的 padding（13px） | 4px 或 8px 倍数系统 |
| Bounce 动画 | cubic-bezier(0.16, 1, 0.3, 1) |
| 灰色文字在彩色背景 | 确保对比度 WCAG 标准 |
| "确认"按钮 | "保存更改"（动词开头）|

### 3. 设计审查命令

提供 10 个命令，像设计总监一样审查代码：

- `/audit` — 检查无障碍、性能、响应式
- `/polish` — 发布前最终打磨
- `/critique` — UX 评审：层次、清晰度
- `/distill` — 化繁为简
- `/colorize` — 引入战略性色彩
- `/animate` — 添加有意义的动效
- `/bolder` — 让设计更大胆
- `/quieter` — 让设计沉稳下来
- `/normalize` — 对齐设计系统
- `/harden` — 增加错误处理、国际化

### 4. 自动触发机制

当用户发出设计相关请求时，Skill 自动：
1. 检查内容是否违反反模式
2. 应用设计令牌和间距系统
3. 推荐合适的字体组合
4. 确保动效使用正确的 easing

## 技术实现

```
┌─────────────────┐
│   用户请求       │
└────────┬────────┘
         ▼
┌─────────────────┐
│  Skill 拦截分析  │ ← 检查关键词（UI/前端/设计）
└────────┬────────┘
         ▼
┌─────────────────┐
│  应用设计规范    │ ← 注入 Design Tokens
│  + 反模式检查    │ ← 检查常见错误
└────────┬────────┘
         ▼
┌─────────────────┐
│   输出高质量代码  │
└─────────────────┘
```

## 效果对比

| 维度 | 安装前 | 安装后 |
|------|--------|--------|
| 字体 | Arial / system-ui | DM Sans + Instrument Serif |
| 色彩 | Hex 纯灰 | OKLCH 带色调 |
| 间距 | 13px, 22px | 8px 倍数系统 |
| 动效 | Bounce / Elastic | cubic-bezier 快入慢出 |
| 按钮 | "确认" | "保存更改"（动词开头）|
| 错误提示 | "输入有误" | "邮箱格式不正确" |
| Loading | Spinner | Skeleton |

## 一句话总结

> **不是让 AI 学会设计，而是给 AI 一套专业设计师的设计规范和检查清单，强制输出高质量结果。**
