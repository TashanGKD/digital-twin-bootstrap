"""配置：内置 API Key 和模型列表，支持 .env 覆盖"""
import os
from pathlib import Path

from dotenv import load_dotenv

_env_paths = [
    Path(__file__).resolve().parent / ".env",
    Path(__file__).resolve().parent.parent.parent / ".env",
]
for p in _env_paths:
    if p.exists():
        load_dotenv(p)
        break
else:
    load_dotenv()

LLM_API_KEY = os.environ.get("LLM_API_KEY", "")
LLM_BASE_URL = os.environ.get(
    "LLM_BASE_URL", "https://dashscope.aliyuncs.com/compatible-mode/v1"
)
LLM_MODEL = os.environ.get("LLM_MODEL", "qwen-plus")

AVAILABLE_MODELS = [
    {"value": "qwen3.5-plus", "label": "Qwen3.5 Plus（推荐）"},
    {"value": "kimi-k2.5", "label": "Kimi K2.5"},
    {"value": "glm-5", "label": "GLM-5"},
    {"value": "MiniMax-M2.5", "label": "MiniMax M2.5"},
    {"value": "qwen3-max-2026-01-23", "label": "Qwen3 Max"},
    {"value": "qwen3-coder-next", "label": "Qwen3 Coder Next"},
    {"value": "qwen3-coder-plus", "label": "Qwen3 Coder Plus"},
    {"value": "glm-4.7", "label": "GLM-4.7"},
]
