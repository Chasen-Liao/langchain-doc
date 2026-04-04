# Model Context Protocol (MCP)

## 什么是 MCP？

**MCP（Model Context Protocol）** 是一个开放协议，标准化了应用程序向 LLM 提供**工具（Tools）**和**上下文（Context）**的方式。

MCP 的核心思想：**把工具定义在"服务器"上，客户端连接服务器获取工具来调用。** 这样工具的宿主（用什么语言、跑在哪里）和 LLM Agent 的宿主是分离的。

```
┌─────────────────┐         ┌─────────────────┐
│   MCP Client    │         │   MCP Client    │
│  (LangChain)    │         │  (LangChain)    │
└────────┬────────┘         └────────┬────────┘
         │                           │
         │  stdio / HTTP             │  stdio / HTTP
         │                           │
┌────────▼────────┐         ┌────────▼────────┐
│   Math MCP      │         │  Weather MCP    │
│   Server        │         │  Server         │
│  (FastMCP)      │         │  (FastMCP)      │
└─────────────────┘         └─────────────────┘
```

## 核心组件

### 1. MCP Server（服务器端）

使用 `fastmcp` 库定义工具并运行服务器。

**math_server.py** - 数学服务（通过 stdio 调用）

```python
from fastmcp import FastMCP

mcp = FastMCP("Math")

@mcp.tool()
def add(a: int, b: int) -> int:
    """Add two numbers"""
    return a + b

@mcp.tool()
def multiply(a: int, b: int) -> int:
    """Multiply two numbers"""
    return a * b

if __name__ == "__main__":
    mcp.run(transport="stdio")
```

**weather_server.py** - 天气服务（通过 HTTP 调用）

```python
from fastmcp import FastMCP

mcp = FastMCP("Weather")

@mcp.tool()
async def get_weather(location: str) -> str:
    """Get weather for location."""
    return f"It's always sunny in {location}"

if __name__ == "__main__":
    mcp.run(transport="streamable-http", host="127.0.0.1", port=8002)
```

> [!TIP]
> `@mcp.tool()` 装饰器将函数注册为 LLM 可调用的工具。函数名和 docstring 会作为工具描述供模型理解用途。

### 2. MCP Client（客户端）

使用 `langchain-mcp-adapters` 的 `MultiServerMCPClient` 连接多个 MCP 服务器。

**支持的 Transport 类型：**

| Transport | 适用场景 | 调用方式 |
|-----------|---------|---------|
| `stdio` | 同一台机器、子进程调用 | 通过 stdin/stdout 通信 |
| `streamable-http` | 远程服务、独立进程 | HTTP 请求 |

### 3. LangChain Agent

`create_agent` 将 LLM 和工具绑定为 Agent，通过 `ainvoke` 调用。

## 完整示例：多 MCP 服务器 Agent

```python
import asyncio
from langchain_mcp_adapters.client import MultiServerMCPClient
from langchain.agents import create_agent
from langchain_openai import ChatOpenAI
import os

def get_model():
    return ChatOpenAI(
        model="Qwen/Qwen2.5-7B-Instruct",
        base_url="https://api.siliconflow.cn/v1",
        api_key=os.environ.get("SILICONFLOW_API_KEY"),
        temperature=0.2,
    )

async def main():
    llm = get_model()

    client = MultiServerMCPClient(
        connections={
            # stdio: 每次调用拉起子进程通信
            "math": {
                "transport": "stdio",
                "command": "python",
                "args": ["math_server.py"]
            },
            # HTTP: 连接已启动的 HTTP 服务
            "weather": {
                "transport": "http",
                "url": "http://127.0.0.1:8002/mcp"
            }
        }
    )

    tools = await client.get_tools()
    agent = create_agent(model=llm, tools=tools)

    math_response = await agent.ainvoke(
        {"messages": [{"role": "user", "content": "what's (3 + 5) x 12?"}]}
    )
    weather_response = await agent.ainvoke(
        {"messages": [{"role": "user", "content": "what is the weather in nyc?"}]}
    )
    print(math_response)
    print(weather_response)

asyncio.run(main())
```

## 运行步骤

```bash
# 1. 启动 weather 服务（终端1）
python weather_server.py

# 2. 运行 agent（终端2）
python run_agent.py
```

`MultiServerMCPClient` 会自动管理连接生命周期，无状态设计意味着每次工具调用都是独立的session。

## 文件结构

```
Advanced-Usage/mcp/
├── math_server.py    # 数学 MCP 服务器（stdio transport）
├── weather_server.py # 天气 MCP 服务器（http transport, port 8002）
└── run_agent.py      # Agent 客户端，连接两个服务器
```