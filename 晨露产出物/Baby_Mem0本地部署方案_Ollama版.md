# Baby 的 Mem0 本地部署方案（Ollama 版）

> 不用翻墙，不用付费，完全本地运行！

---

## 📋 前置检查

确认你的机器配置：
- **CPU**: 任意（有 NVIDIA 显卡更好，没有也行）
- **内存**: 建议 8GB+
- **磁盘**: 需要 5GB+ 空间下载模型

---

## 第一步：安装 Ollama

### Linux（你的机器）
```bash
curl -fsSL https://ollama.com/install.sh | sh
```

安装完成后验证：
```bash
ollama --version
# 应该显示版本号，比如 ollama version 0.3.0
```

---

## 第二步：下载模型

Mem0 需要两个模型：
1. **嵌入模型**（nomic-embed-text）- 用来理解语义
2. **LLM 模型**（llama3.2）- 用来处理记忆

```bash
# 下载嵌入模型（约 275MB）
ollama pull nomic-embed-text

# 下载语言模型（约 2GB）
ollama pull llama3.2
```

等待下载完成...（看网络速度，大概几分钟到十几分钟）

验证安装：
```bash
ollama list
# 应该显示 nomic-embed-text 和 llama3.2
```

---

## 第三步：启动 Ollama 服务

```bash
# 前台启动（测试时用）
ollama serve

# 或者后台启动
nohup ollama serve > /tmp/ollama.log 2>&1 &
```

验证服务运行：
```bash
curl http://localhost:11434/api/tags
# 应该返回模型列表
```

---

## 第四步：配置 OpenClaw

编辑 baby 的配置文件：
```bash
nano /home/cheche/.openclaw-baby/.openclaw/openclaw.json
```

找到 `plugins.entries.openclaw-mem0` 部分，改成：

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
      }
    }
  }
}
```

**保存退出**：按 `Ctrl+O`，回车，然后 `Ctrl+X`

---

## 第五步：重启 Baby 的 Gateway

```bash
systemctl --user restart openclaw-gateway-baby.service
```

查看状态：
```bash
systemctl --user status openclaw-gateway-baby.service --no-pager
```

应该显示 `Active: active (running)` ✅

---

## 第六步：测试记忆功能

1. 给 baby 发一条消息，比如："我喜欢吃草莓"
2. 过几分钟再问 baby："我喜欢吃什么水果？"
3. 如果 baby 能回答"草莓"，说明记忆功能正常！🎉

---

## 🔧 常见问题

### Q1: Ollama 启动失败
```bash
# 检查端口是否被占用
lsof -i :11434

# 如果被占用，杀掉进程
kill -9 <PID>
```

### Q2: 模型下载太慢
```bash
# 设置镜像加速（Linux）
export OLLAMA_HOST=0.0.0.0
# 或者使用代理
```

### Q3: 内存不够
可以换用更小的模型：
```bash
# 换成更小的 LLM
ollama pull llama3.2:1b  # 只有 1.3GB
```

然后把配置里的 `"model": "llama3.2"` 改成 `"model": "llama3.2:1b"`

### Q4: Baby 还是起不来
查看日志：
```bash
journalctl --user -u openclaw-gateway-baby.service -n 50
```

如果显示 connection refused，说明 Ollama 没启动或者端口不对。

---

## 📁 完整配置示例（供复制）

```json
{
  "meta": {
    "lastTouchedVersion": "2026.3.13"
  },
  "models": {
    ...（保持原来的模型配置不变）...
  },
  "agents": {
    ...（保持原来的agent配置不变）...
  },
  "gateway": {
    "port": 18820,
    "mode": "local",
    "auth": {
      "mode": "token",
      "token": "baby_d9e798b6_30fc_46a0_a1c3_c246b09dd395"
    }
  },
  "plugins": {
    "allow": [
      "openclaw-lark",
      "feishu",
      "openclaw-mem0"
    ],
    "slots": {
      "memory": "openclaw-mem0"
    },
    "entries": {
      "feishu": {
        "enabled": false
      },
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
            }
          }
        }
      }
    }
  }
}
```

---

## ✅ 检查清单

- [ ] Ollama 安装成功 (`ollama --version`)
- [ ] 模型下载完成 (`ollama list` 能看到两个模型)
- [ ] Ollama 服务运行中 (`curl localhost:11434/api/tags` 有返回)
- [ ] 配置文件修改正确（有 `config` 包裹所有参数）
- [ ] Baby gateway 重启成功 (`systemctl status` 显示 active)
- [ ] 测试记忆功能正常

---

**有问题就问晨露姐姐，她一直在！** 💕

*文档生成时间：2026-04-04*
