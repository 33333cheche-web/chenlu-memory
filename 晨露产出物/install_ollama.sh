#!/bin/bash
# Ollama 安装脚本 for 6 Bots mem0 记忆系统

echo "🦙 正在安装 Ollama..."

# 安装 Ollama
curl -fsSL https://ollama.com/install.sh | sh

# 检查安装
if ! command -v ollama &> /dev/null; then
    echo "❌ Ollama 安装失败"
    exit 1
fi

echo "✅ Ollama 安装成功"
echo ""
echo "📥 正在下载模型（约 2.5GB，请耐心等待）..."

# 下载嵌入模型（约 275MB）
echo "⏳ 下载 nomic-embed-text..."
ollama pull nomic-embed-text

# 下载 LLM 模型（约 2GB）
echo "⏳ 下载 llama3.2..."
ollama pull llama3.2

echo ""
echo "✅ 模型下载完成！"
echo ""
echo "🚀 启动 Ollama 服务..."
ollama serve &

echo ""
echo "📋 安装完成！"
echo ""
echo "验证安装："
echo "  ollama list          # 查看已下载的模型"
echo "  curl http://localhost:11434/api/tags  # 检查服务状态"
