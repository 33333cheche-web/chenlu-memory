# Skill: newsletter-designer

## 概述
专业 Newsletter 视觉设计工具，提供 700px 固定宽度、杂志风排版、无缝图片等高级邮件设计能力。

## 设计风格

### [EDT] 杂志风 (Editorial)
- 主色：`#1a1a1a`
- 强调色：`#ff6b35`
- 背景：`#faf9f7`
- 字体：Playfair Display / Source Sans 3

### [CYB] 科技风 (Cyber)
- 主色：`#0a0a0f`
- 强调色：`#00ff88`
- 背景：`#050508`
- 字体：Space Grotesk / Inter

### [ORG] 有机风 (Organic)
- 主色：`#2d5a4a`
- 强调色：`#ff9f76`
- 背景：`#fef9f3`
- 字体：Satoshi / Plus Jakarta Sans

### [MIN] 极简风 (Minimal)
- 主色：`#1a1a1a`
- 背景：`#ffffff`
- 辅助：`#f5f5f5`
- 字体：Montserrat / Source Han Sans SC

### [COR] 企业风 (Corporate)
- 主色：`#006633`
- 强调色：`#00d9a3`
- 背景：`#f8fafc`
- 字体：Outfit / Source Sans 3

## 核心 UI 预制件

### 预制件 1：无缝全宽卡片 (Edge-to-Edge Card)
适用于单条重要资讯、文章推荐。图片顶满，下方文字区背景色与卡片一致。

```html
<table width="700" cellpadding="0" cellspacing="0" border="0" align="center" 
       style="background:#ffffff; border-radius:16px; overflow:hidden; box-shadow:0 8px 24px rgba(0,0,0,0.06);">
  <tr>
    <td style="padding:0; font-size:0; line-height:0;">
      <img src="IMAGE_URL" width="700" style="display:block; width:700px; border:0;" alt="Cover">
    </td>
  </tr>
  <tr>
    <td style="padding:40px 50px; background:#ffffff;">
      <span style="color:#ff6b35; font-size:12px; font-weight:bold; letter-spacing:2px;">TAG</span>
      <h2 style="margin:12px 0 8px; font-family:'Playfair Display',serif; font-size:32px; color:#1a1a1a;">标题</h2>
      <p style="margin:0 0 20px; font-size:15px; color:#555555; line-height:1.6;">正文描述</p>
    </td>
  </tr>
</table>
```

### 预制件 2：优雅双栏图文 (Side-by-Side)
适用于产品介绍、人物引言。左图右文，垂直居中对齐。

```html
<table width="700" cellpadding="0" cellspacing="0" border="0" align="center" 
       style="background:#f8f9fa; border-radius:16px; padding:40px;">
  <tr>
    <td width="300" valign="middle" style="padding:0;">
      <img src="IMAGE_URL" width="300" style="display:block; width:300px; border-radius:12px;" alt="Feature">
    </td>
    <td width="40" style="font-size:0; line-height:0;">&nbsp;</td>
    <td width="360" valign="middle" style="padding:0;">
      <span style="color:#ff6b35; font-size:12px; font-weight:bold; letter-spacing:1px;">TAGLINE</span>
      <h3 style="margin:10px 0 12px; font-size:22px; color:#1a1a1a;">标题</h3>
      <p style="margin:0; font-size:14px; color:#666666; line-height:1.7;">内容</p>
    </td>
  </tr>
</table>
```

### 预制件 3：数据展示卡片 (Data Card)
适用于展示关键数据指标。

```html
<table width="700" cellpadding="0" cellspacing="0" border="0" align="center">
  <tr>
    <td width="33%" align="center" style="padding:20px; background:#faf9f7; border-radius:8px;">
      <div style="font-size:28px; font-weight:bold; color:#ff6b35;">数据</div>
      <div style="font-size:12px; color:#555555; margin-top:5px;">标签</div>
    </td>
    <td width="10" style="font-size:0;">&nbsp;</td>
    <td width="33%" align="center" style="padding:20px; background:#faf9f7; border-radius:8px;">
      <div style="font-size:28px; font-weight:bold; color:#ff6b35;">数据</div>
      <div style="font-size:12px; color:#555555; margin-top:5px;">标签</div>
    </td>
    <td width="10" style="font-size:0;">&nbsp;</td>
    <td width="33%" align="center" style="padding:20px; background:#faf9f7; border-radius:8px;">
      <div style="font-size:28px; font-weight:bold; color:#ff6b35;">数据</div>
      <div style="font-size:12px; color:#555555; margin-top:5px;">标签</div>
    </td>
  </tr>
</table>
```

### 预制件 4：特色功能区 (Feature Box)
适用于展示功能列表或要点。

```html
<table width="100%" cellpadding="0" cellspacing="0" border="0" style="margin-bottom:25px;">
  <tr>
    <td style="background:#f8f9fa; border-radius:12px; padding:25px;">
      <h4 style="margin:0 0 15px; font-size:14px; color:#1a1a1a; letter-spacing:1px;">💡 核心功能</h4>
      <ul style="margin:0; padding-left:20px; font-size:14px; color:#555555; line-height:2;">
        <li>功能1</li>
        <li>功能2</li>
      </ul>
    </td>
  </tr>
</table>
```

### 预制件 5：引用块 (Quote Block)
适用于展示用户评价或重要观点。

```html
<p style="margin:0 0 15px; font-size:13px; color:#555555; line-height:1.8; 
          border-left:3px solid #ff6b35; padding-left:15px; font-style:italic;">
  "这里是引用内容"
</p>
```

### 预制件 6：CTA 按钮 (Call-to-Action)
适用于行动号召。

```html
<table cellpadding="0" cellspacing="0" border="0">
  <tr>
    <td style="background:#1a1a1a; border-radius:8px; padding:12px 24px;">
      <a href="LINK" style="color:#ffffff; text-decoration:none; font-size:14px; font-weight:bold;">按钮文字 →</a>
    </td>
  </tr>
</table>
```

### 预制件 7：深色技术块 (Dark Tech Block)
适用于 GitHub Trending 或技术相关内容。

```html
<table width="700" cellpadding="0" cellspacing="0" border="0" align="center" 
       style="background:#1a1a1a; border-radius:16px; padding:35px 50px;">
  <tr>
    <td>
      <span style="color:#888888; font-size:12px; font-weight:bold; letter-spacing:2px;">⭐ GITHUB TRENDING</span>
      <h3 style="margin:12px 0 8px; font-size:22px; color:#ffffff;">项目名称</h3>
      <p style="margin:0; font-size:13px; color:#ffffff; line-height:1.7;">描述内容</p>
    </td>
  </tr>
</table>
```

### 预制件 8：行动建议块 (Action Block)
适用于总结行动建议。

```html
<table width="700" cellpadding="0" cellspacing="0" border="0" align="center" 
       style="background:#ff6b35; border-radius:16px; padding:30px 50px;">
  <tr>
    <td>
      <h4 style="margin:0 0 15px; font-size:16px; color:#ffffff;">💡 行动建议</h4>
      <ul style="margin:0; padding-left:20px; font-size:14px; color:#ffffff; line-height:2; opacity:0.95;">
        <li>建议1</li>
        <li>建议2</li>
      </ul>
    </td>
  </tr>
</table>
```

## 使用示例

### 完整邮件结构

```html
<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Newsletter Title</title>
    <link href="https://fonts.googleapis.com/css2?family=Playfair+Display:wght@400;700&family=Source+Sans+3:wght@400;600&display=swap" rel="stylesheet">
</head>
<body style="margin:0; padding:0; background:#faf9f7; font-family:'Source Sans 3',sans-serif;">
    
    <!-- 外层居中容器 -->
    <table width="100%" cellpadding="0" cellspacing="0" border="0" align="center">
        <tr>
            <td align="center" style="padding:40px 0;">
                
                <!-- 主容器 700px -->
                <table width="700" cellpadding="0" cellspacing="0" border="0" align="center">
                    
                    <!-- Header -->
                    <tr>
                        <td align="center" style="padding-bottom:30px;">
                            <h1 style="margin:0; font-family:'Playfair Display',serif; font-size:42px; color:#1a1a1a;">
                                标题
                            </h1>
                        </td>
                    </tr>
                    
                    <!-- 内容区块（使用预制件） -->
                    <!-- ... -->
                    
                </table>
            </td>
        </tr>
    </table>
</body>
</html>
```

## 注意事项

1. **绝对固定宽度 700px**：必须使用 table 嵌套结构，禁止使用响应式设计
2. **图片无缝处理**：所有 img 标签必须包含 `style="display:block; border:0;"`
3. **背景色一致性**：图片与其下方文字必须包裹在同一背景色的 table 中
4. **字体引入**：通过 Google Fonts CDN 引入字体
5. **兼容性**：使用 table 布局确保在所有邮件客户端正常显示

## 图片资源

推荐使用 Unsplash 图片进行点缀：
- 游戏：`https://images.unsplash.com/photo-1550745165-9bc0b252726f?w=700`
- 科技：`https://images.unsplash.com/photo-1550751827-4bd374c3f58b?w=700`
- 创意：`https://images.unsplash.com/photo-1558655146-9f40138edfeb?w=700`

## 更新日志

- 2026-03-22: 初始版本，包含8个预制件和5种设计风格
