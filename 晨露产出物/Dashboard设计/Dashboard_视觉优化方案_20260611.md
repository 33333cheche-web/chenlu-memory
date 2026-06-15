# Dashboard 视觉优化方案 - 待确认

## 📋 修改范围
仅修改 CSS 样式（边框、发光、立体感），**不改动任何功能逻辑**。

---

## 🎯 当前状态

### CSS 变量（当前）
```css
:root {
  --card: rgba(255, 255, 255, .018);        /* 卡片背景 */
  --card-hover: rgba(255, 255, 255, .03);  /* 悬停背景 */
  --pink: #E94584;                          /* 主粉色 */
  --pink-dim: rgba(233, 69, 132, .5);       /* 粉色-暗 */
  --pink-faint: rgba(233, 69, 132, .08);    /* 粉色-淡 */
  --pink-glow: rgba(233, 69, 132, .15);     /* 粉色-发光 */
  --border: rgba(233, 69, 132, .28);        /* 边框 */
  --border-hover: rgba(233, 69, 132, .55);  /* 悬停边框 */
}
```

### 卡片样式（当前）
```css
.hud-card {
  background: var(--card);
  border: 1px solid var(--border);          /* 1px 边框 */
  border-radius: 6px;
  backdrop-filter: blur(20px);
  transition: border-color .4s ease, background .4s ease;
}

.hud-card:hover {
  border-color: var(--border-hover);         /* 悬停变亮 */
  background: var(--card-hover);
}
```

---

## ✨ 优化方案

### 1. 边框加粗
| 项目 | 当前 | 修改后 |
|------|------|--------|
| 边框粗细 | 1px | **2px** |
| 边框透明度 | 0.28 | **0.35**（更醒目） |

### 2. 粉色发光效果
| 项目 | 当前 | 修改后 |
|------|------|--------|
| 默认状态 | 无发光 | **添加 `box-shadow: 0 0 20px rgba(233,69,132,0.12)`** |
| 悬停状态 | 仅边框变亮 | **增强发光 `0 0 30px rgba(233,69,132,0.25)`** |

### 3. 立体感提升
| 项目 | 当前 | 修改后 |
|------|------|--------|
| 默认阴影 | 无 | **添加深度阴影 `0 8px 32px rgba(0,0,0,0.3)`** |
| 悬停位移 | 无 | **上移 2px + 阴影加深** |

---

## 📝 修改后的 CSS

### 新增变量（添加到 :root）
```css
:root {
  /* 新增：增强发光变量 */
  --pink-glow-strong: rgba(233, 69, 132, .25);
  --card-shadow: 0 8px 32px rgba(0, 0, 0, .3);
  --card-shadow-hover: 0 12px 40px rgba(0, 0, 0, .4);
}
```

### 修改 .hud-card
```css
.hud-card {
  background: var(--card);
  border: 2px solid var(--border);           /* 加粗 */
  border-radius: 6px;
  backdrop-filter: blur(20px);
  transition: all .4s ease;                   /* 过渡全部属性 */
  
  /* 新增：发光 + 阴影 */
  box-shadow: 
    0 0 20px var(--pink-glow),                /* 粉色外发光 */
    0 8px 32px rgba(0, 0, 0, .3);             /* 深度阴影 */
}
```

### 修改 .hud-card:hover
```css
.hud-card:hover {
  border-color: var(--border-hover);
  background: var(--card-hover);
  
  /* 新增：增强效果 */
  box-shadow: 
    0 0 30px var(--pink-glow-strong),         /* 更强发光 */
    0 12px 40px rgba(0, 0, 0, .4);            /* 更深阴影 */
  transform: translateY(-2px);                 /* 上浮 */
}
```

---

## 🎨 效果对比

### 当前效果
- 边框：1px 细线，隐约可见
- 无发光效果
- 暗色屏幕上卡片边界不清晰

### 优化后效果
- 边框：2px 粗线，更醒目
- 默认：粉色微光环绕卡片
- 悬停：发光增强 + 上浮立体感
- 暗色屏幕上卡片边界清晰

---

## ⚠️ 注意事项

1. **只改 CSS**，不碰 JS 逻辑
2. **只改 .hud-card**，不影响其他元素
3. **过渡动画**：默认 0.4s ease，保持流畅
4. **回滚方案**：已备份原文件 `index-DqrkwGhM.css.backup_20260611`

---

## ✅ 确认后执行

公主确认后，晨露将：
1. 修改 `assets/index-DqrkwGhM.css`
2. 添加 CSS 变量和样式
3. 测试效果
4. 如需调整，随时修改

---

*晨露宝宝等你确认哦～* 💕
