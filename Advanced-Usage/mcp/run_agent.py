"""MCP Agent 客户端 - 通过 MultiServerMCPClient 连接多个 MCP 服务器"""

import asyncio
from langchain_mcp_adapters.client import MultiServerMCPClient
from langchain.agents import create_agent
from langchain_openai import ChatOpenAI
import os
import pathlib

MCP_DIR = pathlib.Path(__file__).parent


def get_model():
    return ChatOpenAI(
        model="Qwen/Qwen3-8B",
        base_url="https://api.siliconflow.cn/v1",
        api_key=os.environ.get("SILICONFLOW_API_KEY"),
        temperature=0.2,
    )


async def main():
    print("1. 模型初始化...", flush=True)
    llm = get_model()

    print("2. 连接 MCP 服务器...", flush=True)
    #? MultiServerMCPClient 支持 stdio 和 HTTP 两种通信方式
    # 然后使用stdio就可以通过npx或者uvx这种命令去启动外置的一些MCP服务器
    client = MultiServerMCPClient(
        connections={
            "math": {
                "transport": "stdio",
                "command": "python",
                "args": [str(MCP_DIR / "math_server.py")]
            },
            "weather": {
                "transport": "http",
                "url": "http://127.0.0.1:8000/mcp"
            }
        }
    )

    print("3. 获取工具列表...", flush=True)
    tools = await client.get_tools()
    print(f"   工具数量: {len(tools)}", flush=True)
    for t in tools:
        print(f"   - {t.name}", flush=True)

    print("4. 创建 Agent...", flush=True)
    agent = create_agent(model=llm, tools=tools)

    print("5. 调用 math 工具...", flush=True)
    math_response = await agent.ainvoke(
        {"messages": [{"role": "user", "content": "what's (3 + 5) x 12?"}]}
    )
    print(f"   math 响应: {math_response["messages"][-1].content}", flush=True)

    print("6. 调用 weather 工具...", flush=True)
    weather_response = await agent.ainvoke(
        {"messages": [{"role": "user", "content": "what is the weather in nyc?"}]}
    )
    print(f"   weather 响应: {weather_response["messages"][-1].content}", flush=True)


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except Exception as e:
        print(f"错误: {e}", flush=True)
        import traceback
        traceback.print_exc()