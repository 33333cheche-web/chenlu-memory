#!/usr/bin/env python3
"""
mem0 wrapper for Sunny - 轻量版（无 LLM 提取，纯规则）
使用本地 embedding + Chroma
"""

import sys
import os

# 激活虚拟环境
venv_path = os.path.expanduser("~/.openclaw/.venvs/mem0-env")
activate_script = os.path.join(venv_path, "bin", "activate_this.py")

if os.path.exists(activate_script):
    exec(open(activate_script).read(), {'__file__': activate_script})

from sentence_transformers import SentenceTransformer
import chromadb
from chromadb.config import Settings
from datetime import datetime
import re

# 设置缓存
os.environ['TRANSFORMERS_CACHE'] = os.path.expanduser('~/.cache/huggingface')
os.environ['HF_HOME'] = os.path.expanduser('~/.cache/huggingface')

# 初始化 embedding 模型
print("🔄 加载模型...")
embedder = SentenceTransformer('all-MiniLM-L6-v2', cache_folder=os.path.expanduser('~/.cache/huggingface'))

# 初始化 Chroma（新格式）
chroma_client = chromadb.PersistentClient(
    path="/home/cheche/.openclaw/workspace-chenlu/.mem0/chroma_db"
)
collection = chroma_client.get_or_create_collection(name="sunny_memories")

def simple_extract(text):
    """简单规则提取记忆"""
    # 提取"喜欢/偏好"
    if "喜欢" in text or "偏好" in text:
        match = re.search(r'(.{0,20}喜欢.{0,30})', text)
        if match:
            return match.group(1)
    
    # 提取"每天/定时"
    if "每天" in text or "定时" in text or "点" in text:
        match = re.search(r'(.{0,10}每天.{0,30})', text)
        if match:
            return match.group(1)
    
    # 提取"完成/做了"
    if "完成" in text or "做了" in text or "发送" in text:
        return text[:50] + "..." if len(text) > 50 else text
    
    return text[:50] + "..." if len(text) > 50 else text

def add_memory(text):
    """添加记忆"""
    memory = simple_extract(text)
    if not memory:
        print("ℹ️ 无重要记忆")
        return
    
    # 生成 embedding
    embedding = embedder.encode(memory).tolist()
    
    # 生成 ID
    memory_id = f"mem_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
    
    # 存入 Chroma
    collection.add(
        embeddings=[embedding],
        documents=[memory],
        ids=[memory_id],
        metadatas=[{"timestamp": datetime.now().isoformat(), "source": text[:100]}]
    )
    
    print(f"✅ 已添加 [{memory_id}]: {memory}")
    return memory_id

def search_memories(query, n_results=3):
    """搜索记忆"""
    query_embedding = embedder.encode(query).tolist()
    
    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=n_results
    )
    
    memories = []
    if results['documents'] and results['documents'][0]:
        for i, doc in enumerate(results['documents'][0]):
            memories.append({
                'memory': doc,
                'id': results['ids'][0][i],
                'distance': results['distances'][0][i] if 'distances' in results else None
            })
    
    return memories

def list_all_memories():
    """列出所有记忆"""
    results = collection.get()
    
    memories = []
    if results['documents']:
        for i, doc in enumerate(results['documents']):
            memories.append({
                'memory': doc,
                'id': results['ids'][i],
                'metadata': results['metadatas'][i] if 'metadatas' in results else {}
            })
    
    return memories

def main():
    if len(sys.argv) < 2:
        print("用法: python mem0_sunny.py <命令> [参数]")
        print("命令: add, search, list")
        return
    
    cmd = sys.argv[1]
    
    if cmd == "add":
        if len(sys.argv) < 3:
            print("用法: add <内容>")
            return
        content = sys.argv[2]
        add_memory(content)
    
    elif cmd == "search":
        if len(sys.argv) < 3:
            print("用法: search <查询>")
            return
        query = sys.argv[2]
        results = search_memories(query)
        print(f"🔍 找到 {len(results)} 条:")
        for r in results:
            print(f"  - [{r['id']}] {r['memory']}")
    
    elif cmd == "list":
        results = list_all_memories()
        print(f"📚 共 {len(results)} 条:")
        for r in results:
            print(f"  - [{r['id']}] {r['memory']}")
    
    else:
        print(f"未知命令: {cmd}")

if __name__ == "__main__":
    main()
