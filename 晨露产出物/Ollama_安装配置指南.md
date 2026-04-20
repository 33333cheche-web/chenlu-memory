# Ollama 安装指南 - 为 6 Bots 配置本地记忆

## 📦 安装 Ollama

在终端运行以下命令：

```bash
# 安装 Ollama（需要 sudo 密码）
curl -fsSL https://ollama.com/install.sh | sh

# 验证安装
ollama --version
```

## 📥 下载模型

```bash
# 下载嵌入模型（约 275MB）
ollama pull nomic-embed-text

# 下载 LLM 模型（约 2GB）
ollama pull llama3.2

# 验证模型
ollama list
```

## 🚀 启动服务

```bash
# 前台启动（测试用）
ollama serve

# 或者后台启动
nohup ollama serve > /tmp/ollama.log 2>&1 &
```

验证服务运行：
```bash
curl http://localhost:11434/api/tags
```

## ⚙️ 配置 Bots

安装完成后，每个 Bot 的 openclaw.json 改成：

```json
"openclaw-mem0": {
  "enabled": true,
  "config": {
    "mode": "open-source",
    "userId": "princess",
    "autoCapture": true,
    "autoRecall": true,
    "oss": {
      "embedder": {
        "provider": "ollama",
        "config": {
          "model": "nomic-embed-text"
        }
      },
      "llm": {
        "provider": "ollama",
        "config": {
          "model": "llama3.2"
        }
      },
      "vectorStore": {
        "provider": "memory"
      },
      "disableHistory": true
    }
  }
}
```

## 🔄 重启 Bots

```bash
systemctl --user restart openclaw-gateway-baby.service
systemctl --user restart openclaw-gateway-bot2.service
systemctl --user restart openclaw-gateway-rainbow.service
```

## ✅ 测试记忆

1. 告诉 Bot："我喜欢春天"
2. 过一会儿问："我喜欢什么季节？"
3. 如果回答"春天"，就成功了！

---
*有问题找晨露宝宝～* 💕
