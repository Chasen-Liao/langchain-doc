# 通过LangChain MCP适配器获取fetch工具列表
from langchain_mcp_adapters.client import MultiServerMCPClient
import asyncio


async def main():
    # 定义MCP客户端
    client = MultiServerMCPClient(
        connections={
            "fetch": {
                "transport": "stdio",
                "command": "python",
                "args": ["-m", "mcp_server_fetch"],
            }
        }
    )

    # 获取工具
    tools = await client.get_tools()

    print("MCP服务器已连接!", flush=True)
    print(f"\n可用工具: {[t.name for t in tools]}", flush=True)
    print(f"\n工具描述: {[t.description for t in tools]}", flush=True)


if __name__ == "__main__":
    asyncio.run(main())
