# minimax-docx Skill

## 描述
使用 C# 和 OpenXML SDK 创建 Word 文档 (.docx)。

## 用法

### 创建 Word 文档
```bash
cd /home/cheche/.openclaw/workspace-chenlu/skills/minimax-docx
dotnet run "文档标题" "文档内容" 输出路径.docx
```

### 示例
```bash
dotnet run "晨露早报" "这是晨报内容\n第二行内容" /tmp/晨报.docx
```

## 依赖
- .NET 6.0+
- DocumentFormat.OpenXml 包

## 安装依赖
```bash
cd /home/cheche/.openclaw/workspace-chenlu/skills/minimax-docx
dotnet restore
```
