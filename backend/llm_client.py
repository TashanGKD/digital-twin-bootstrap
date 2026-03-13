"""LLM 客户端：统一 OpenAI 兼容接口"""
from openai import OpenAI

from config import LLM_API_KEY, LLM_BASE_URL, LLM_MODEL


def create_client() -> OpenAI | None:
    if not LLM_API_KEY:
        return None
    return OpenAI(api_key=LLM_API_KEY, base_url=LLM_BASE_URL)


def get_model(override: str | None = None) -> str:
    return override or LLM_MODEL
