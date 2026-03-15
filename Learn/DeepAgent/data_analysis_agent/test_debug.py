"""
调试脚本 - 测试 create_deep_agent 的基本功能
"""

import os
import sys
from pathlib import Path
from dotenv import load_dotenv

# 加载环境变量
load_dotenv()

# 检查 API 密钥
api_key = os.getenv("SILICONFLOW_API_KEY")
print(f"API Key 存在：{bool(api_key)}")
if api_key:
    print(f"API Key 前缀：{api_key[:10]}...")

# 测试导入
print("\n测试导入模块...")
try:
    from deepagents import create_deep_agent
    print("✅ deepagents 导入成功")
except Exception as e:
    print(f"❌ deepagents 导入失败：{e}")
    sys.exit(1)

try:
    from langgraph.checkpoint.memory import MemorySaver
    print("✅ MemorySaver 导入成功")
except Exception as e:
    print(f"❌ MemorySaver 导入失败：{e}")
    sys.exit(1)

# 测试 LLM
print("\n测试 LLM 创建...")
try:
    from config import get_llm
    llm = get_llm(
        model_name="deepseek-ai/DeepSeek-V3.2",
        temperature=0.1,
        max_tokens=100,  # 减少 token 数以加快测试
        streaming=False,
        timeout=30,
    )
    print(f"✅ LLM 创建成功：{llm}")
except Exception as e:
    print(f"❌ LLM 创建失败：{e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

# 测试工具
print("\n测试工具加载...")
try:
    from tools import get_all_tools
    tools = get_all_tools()
    print(f"✅ 工具加载成功：{len(tools)} 个工具")
    for tool in tools:
        print(f"   - {tool.name}: {tool.description[:50]}...")
except Exception as e:
    print(f"❌ 工具加载失败：{e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

# 测试创建 Agent
print("\n测试创建 Agent...")
try:
    checkpointer = MemorySaver()

    # 简化 interrupt_on 配置
    interrupt_on = {
        "save_markdown_report": True,
    }

    agent = create_deep_agent(
        model=llm,
        tools=tools,
        checkpointer=checkpointer,
        interrupt_on=interrupt_on,
        system_prompt="你是一个数据分析助手。"
    )
    print(f"✅ Agent 创建成功：{agent}")
except Exception as e:
    print(f"❌ Agent 创建失败：{e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

# 测试简单调用
print("\n测试 Agent 调用...")
try:
    config = {"configurable": {"thread_id": "test-1"}}

    result = agent.invoke(
        {"messages": [{"role": "user", "content": "你好，请简单介绍一下你自己"}]},
        config=config
    )
    print(f"✅ Agent 调用成功")
    print(f"结果：{result}")
except Exception as e:
    print(f"❌ Agent 调用失败：{e}")
    import traceback
    traceback.print_exc()

print("\n调试完成!")
