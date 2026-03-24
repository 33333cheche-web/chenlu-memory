#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
语音识别工具 - 使用 OpenAI Whisper
将音频/语音文件转换为文字
"""

import sys
import os
import subprocess
import tempfile
from pathlib import Path


def check_ffmpeg() -> bool:
    """检查是否安装了 ffmpeg"""
    try:
        subprocess.run(["ffmpeg", "-version"], capture_output=True, check=True)
        return True
    except (subprocess.CalledProcessError, FileNotFoundError):
        return False


def check_whisper() -> bool:
    """检查是否安装了 whisper"""
    try:
        import whisper
        return True
    except ImportError:
        return False


def install_whisper():
    """提示安装 whisper"""
    print("⚠️  Whisper 未安装，正在尝试安装...", file=sys.stderr)
    try:
        subprocess.run(
            [sys.executable, "-m", "pip", "install", "-U", "openai-whisper", "--break-system-packages"],
            check=True,
            capture_output=True
        )
        print("✅ Whisper 安装完成", file=sys.stderr)
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Whisper 安装失败: {e}", file=sys.stderr)
        return False


def convert_to_wav(input_path: str) -> str:
    """将音频文件转换为 WAV 格式（Whisper 需要）"""
    # 创建临时文件
    temp_fd, temp_path = tempfile.mkstemp(suffix=".wav")
    os.close(temp_fd)
    
    try:
        # 使用 ffmpeg 转换
        subprocess.run(
            [
                "ffmpeg",
                "-i", input_path,
                "-ar", "16000",  # 采样率 16kHz
                "-ac", "1",      # 单声道
                "-c:a", "pcm_s16le",  # 16位 PCM
                "-y",            # 覆盖输出
                temp_path
            ],
            check=True,
            capture_output=True
        )
        return temp_path
    except subprocess.CalledProcessError as e:
        os.unlink(temp_path)
        raise RuntimeError(f"音频转换失败: {e}")


def transcribe_audio(audio_path: str, model_size: str = "base") -> str:
    """
    识别音频文件中的语音
    
    Args:
        audio_path: 音频文件路径
        model_size: 模型大小 (tiny, base, small, medium, large, turbo)
    
    Returns:
        识别出的文字
    """
    # 检查依赖
    if not check_ffmpeg():
        return "❌ 错误：需要安装 ffmpeg。请运行: sudo apt install ffmpeg"
    
    if not check_whisper():
        if not install_whisper():
            return "❌ 错误：Whisper 安装失败，请手动运行: pip install -U openai-whisper"
        # 重新导入
        import importlib
        importlib.invalidate_caches()
    
    import whisper
    
    # 检查文件是否存在
    if not os.path.exists(audio_path):
        return f"❌ 错误：文件不存在: {audio_path}"
    
    # 转换为 WAV（如果不是的话）
    file_ext = Path(audio_path).suffix.lower()
    temp_wav = None
    
    try:
        if file_ext != ".wav":
            print(f"🎵 正在转换音频格式...", file=sys.stderr)
            temp_wav = convert_to_wav(audio_path)
            audio_path = temp_wav
        
        # 加载模型
        print(f"🤖 正在加载 Whisper {model_size} 模型...", file=sys.stderr)
        model = whisper.load_model(model_size)
        
        # 识别
        print(f"📝 正在识别语音...", file=sys.stderr)
        result = model.transcribe(audio_path, language="zh")
        
        return result["text"].strip()
        
    finally:
        # 清理临时文件
        if temp_wav and os.path.exists(temp_wav):
            os.unlink(temp_wav)


def main():
    if len(sys.argv) < 2:
        print("用法：python3 speech_recognition.py <音频文件路径>")
        print("示例：python3 speech_recognition.py /tmp/voice.mp3")
        print("")
        print("支持的格式：mp3, wav, m4a, ogg, webm 等")
        print("可选参数 --model：指定模型大小 (tiny/base/small/medium/large/turbo)")
        sys.exit(1)
    
    audio_path = sys.argv[1]
    
    # 解析可选参数
    model_size = "base"
    if "--model" in sys.argv:
        idx = sys.argv.index("--model")
        if idx + 1 < len(sys.argv):
            model_size = sys.argv[idx + 1]
    
    # 执行识别
    text = transcribe_audio(audio_path, model_size)
    
    if text.startswith("❌"):
        print(text, file=sys.stderr)
        sys.exit(1)
    else:
        print(text)


if __name__ == "__main__":
    main()
