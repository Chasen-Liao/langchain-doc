"""
硅基流动 (SiliconFlow) API 配置模块

此模块提供与硅基流动 AI 服务集成的配置，硅基流动是兼容 OpenAI API 的国产 AI 服务提供商。
支持多种开源模型，包括 Qwen、GLM、DeepSeek 等。
"""

import os
from typing import Optional
from langchain_openai import ChatOpenAI
from langchain_openai.embeddings import OpenAIEmbeddings
from dotenv import load_dotenv

# 加载环境变量
load_dotenv()

# 硅基流动 API 配置
SILICONFLOW_API_KEY = os.getenv("SILICONFLOW_API_KEY")
SILICONFLOW_BASE_URL = "https://api.siliconflow.cn/v1"

# 支持的模型列表
SUPPORTED_MODELS = {
    "deepseek-ai/DeepSeek-V3.2": "deepseek-ai/DeepSeek-V3.2",
}

def get_llm(
    model_name: str = "deepseek-ai/DeepSeek-V3.2",
    temperature: float = 0.1,
    max_tokens: Optional[int] = None,
    streaming: bool = False,
    timeout: Optional[int] = 60,
) -> ChatOpenAI:
    """
    获取硅基流动的 LLM 实例

    Args:
        model_name: 模型名称，必须是 SUPPORTED_MODELS 中的键
        temperature: 温度参数，控制随机性
        max_tokens: 最大输出 token 数
        streaming: 是否启用流式输出
        timeout: 请求超时时间（秒）

    Returns:
        ChatOpenAI: 配置好的 LLM 实例

    Raises:
        ValueError: 如果 API 密钥未设置或模型不支持
    """
    # 获取完整的模型路径
    model_path = SUPPORTED_MODELS[model_name]

    # 创建 ChatOpenAI 实例，配置硅基流动的 base_url
    llm = ChatOpenAI(
        model=model_path,
        openai_api_key=SILICONFLOW_API_KEY,
        openai_api_base=SILICONFLOW_BASE_URL,
        temperature=temperature,
        max_tokens=max_tokens,
        streaming=streaming,
        timeout=timeout,
    )

    return llm

def get_embeddings(
    model_name: str = "Qwen/Qwen3-Embedding-4B",
) -> OpenAIEmbeddings:
    """
    获取硅基流动的嵌入模型实例

    Args:
        model_name: 嵌入模型名称，硅基流动支持 OpenAI 兼容的嵌入模型
                  注意：硅基流动可能支持其他嵌入模型，请参考官方文档

    Returns:
        OpenAIEmbeddings: 配置好的嵌入模型实例
    """
    if not SILICONFLOW_API_KEY:
        raise ValueError("SILICONFLOW_API_KEY 环境变量未设置，请设置硅基流动 API 密钥")

    embeddings = OpenAIEmbeddings(
        model=model_name,
        openai_api_key=SILICONFLOW_API_KEY,
        openai_api_base=SILICONFLOW_BASE_URL,
    )

    return embeddings

def check_api_key() -> bool:
    """
    检查硅基流动 API 密钥是否已配置

    Returns:
        bool: 如果 API 密钥已配置返回 True，否则返回 False
    """
    return bool(SILICONFLOW_API_KEY)
