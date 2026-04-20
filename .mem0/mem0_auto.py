#!/usr/bin/env python3
"""
晨露的完整版 mem0 配置
自动捕获对话中的记忆
"""

import os
from mem0 import Memory
from mem0.configs.base import MemoryConfig
from mem0.llms.configs import LlmConfig
from mem0.embeddings.configs import EmbedderConfig
from mem0.vector_stores.configs import VectorStoreConfig

# Qdrant 数据路径
chroma_path = os.path.expanduser("~/.openclaw/workspace-chenlu/.mem0/chroma_db")
os.makedirs(chroma_path, exist_ok=True)

# 创建完整配置
config = MemoryConfig(
    llm=LlmConfig(
        provider="ollama",
        config={
            "model": "llama3.2:latest",
            "ollama_base_url": "http://localhost:11434"
        }
    ),
    embedder=EmbedderConfig(
        provider="ollama",
        config={
            "model": "nomic-embed-text:latest",
            "ollama_base_url": "http://localhost:11434",
            "embedding_dims": 768
        }
    ),
    vector_store=VectorStoreConfig(
        provider="chroma",
        config={
            "path": chroma_path,
            "collection_name": "chenlu_memories",
        }
    )
)

# 初始化 Memory
memory = Memory(config=config)

def add_message(content, user_id="princess"):
    """自动添加对话记忆"""
    result = memory.add(content, user_id=user_id)
    return result

def search_memories(query, user_id="princess"):
    """搜索记忆"""
    results = memory.search(query, user_id=user_id)
    return results

def get_all_memories(user_id="princess"):
    """获取所有记忆"""
    return memory.get_all(user_id=user_id)

if __name__ == "__main__":
    print("🚀 晨露的 mem0 初始化成功！")
    all_memories = get_all_memories()
    print(f"当前记忆数: {len(all_memories.get('results', []))}")
