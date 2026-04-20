#!/usr/bin/env python3
"""
Sunny 本地 mem0 server 客户端
调用自托管的 mem0 REST API (http://localhost:8000)
"""

import os
import sys
import json
import requests

BASE_URL = os.environ.get("MEM0_BASE_URL", "http://localhost:8000")
API_KEY = os.environ.get("MEM0_API_KEY", "openclaw-shared-local-key-2026")
DEFAULT_USER_ID = "chenlu"

def headers():
    return {"X-API-Key": API_KEY, "Content-Type": "application/json"}

def add(text: str, user_id: str = None, metadata: dict = None):
    uid = user_id or DEFAULT_USER_ID
    meta = dict(metadata) if metadata else {}
    payload = {
        "messages": [{"role": "user", "content": text}],
        "user_id": uid,
        "metadata": meta,
        "infer": False,
    }
    r = requests.post(f"{BASE_URL}/memories", headers=headers(), json=payload, timeout=30)
    r.raise_for_status()
    return r.json()

def search(query: str, n_results: int = 5, user_id: str = None):
    uid = user_id or DEFAULT_USER_ID
    payload = {
        "query": query,
        "user_id": uid,
        "limit": n_results,
    }
    r = requests.post(f"{BASE_URL}/search", headers=headers(), json=payload, timeout=30)
    r.raise_for_status()
    data = r.json()
    return data.get("results", [])

def delete(memory_id: str):
    r = requests.delete(f"{BASE_URL}/memories/{memory_id}", headers=headers(), timeout=30)
    r.raise_for_status()
    return {"id": memory_id, "status": "deleted"}

def list_all(user_id: str = None, limit: int = 100):
    uid = user_id or DEFAULT_USER_ID
    r = requests.get(f"{BASE_URL}/memories", headers=headers(), params={"user_id": uid, "limit": limit}, timeout=30)
    r.raise_for_status()
    data = r.json()
    # mem0 server get_all 返回 dict 含 memories 列表
    if isinstance(data, dict):
        return data.get("memories", [])
    return data

def main():
    if len(sys.argv) < 2:
        print("用法: python sunny_mem0_local.py <add|search|delete|list> [参数...]")
        sys.exit(1)

    cmd = sys.argv[1]

    if cmd == "add":
        text = sys.argv[2] if len(sys.argv) > 2 else ""
        # sys.argv[3] 可能是 metadata JSON 或 user_id
        user_id = DEFAULT_USER_ID
        metadata = {}
        if len(sys.argv) > 3:
            arg3 = sys.argv[3]
            try:
                parsed = json.loads(arg3)
                if isinstance(parsed, dict):
                    metadata = parsed
                    user_id = sys.argv[4] if len(sys.argv) > 4 else DEFAULT_USER_ID
                else:
                    user_id = arg3
            except json.JSONDecodeError:
                user_id = arg3
            if len(sys.argv) > 4 and not metadata:
                try:
                    metadata = json.loads(sys.argv[4])
                except json.JSONDecodeError:
                    pass
        result = add(text, user_id=user_id, metadata=metadata)
        print(json.dumps(result, ensure_ascii=False))

    elif cmd == "search":
        query = sys.argv[2] if len(sys.argv) > 2 else ""
        n = int(sys.argv[3]) if len(sys.argv) > 3 else 5
        user_id = sys.argv[4] if len(sys.argv) > 4 else DEFAULT_USER_ID
        results = search(query, n_results=n, user_id=user_id)
        print(json.dumps(results, ensure_ascii=False))

    elif cmd == "delete":
        memory_id = sys.argv[2] if len(sys.argv) > 2 else ""
        result = delete(memory_id)
        print(json.dumps(result, ensure_ascii=False))

    elif cmd == "list":
        user_id = sys.argv[2] if len(sys.argv) > 2 else DEFAULT_USER_ID
        limit = int(sys.argv[3]) if len(sys.argv) > 3 else 100
        results = list_all(user_id=user_id, limit=limit)
        print(json.dumps(results, ensure_ascii=False))

    else:
        print(f"未知命令: {cmd}")
        sys.exit(1)

if __name__ == "__main__":
    main()
