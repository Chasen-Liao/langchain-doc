# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## 项目概述

这是一个 LangChain v1.2 官方文档学习仓库，完全按照 LangChain 官方文档顺序组织学习内容。项目使用 Python 3.13+，主要通过 Jupyter notebook 实践 LangChain 的核心概念和 API 使用。多使用mcp获取doc来获取最新文档

## 开发环境设置

### 包管理
项目使用 [uv](https://github.com/astral-sh/uv) 作为 Python 包管理器：

```bash
# 安装依赖（使用 uv）
uv pip install -e .

# 安装开发依赖
uv pip install -e ".[dev]"

# 安装测试依赖
uv pip install -e ".[test]"
```

### 虚拟环境
项目已配置 `.venv` 目录作为虚拟环境。确保在激活虚拟环境后运行命令：

```bash
# Windows
.venv\Scripts\activate

# Unix/macOS
source .venv/bin/activate
```

## 项目架构

### 目录结构
```
├── Core-components/           # LangChain 核心组件学习
│   ├── Agents/               # 智能代理
│   ├── Messages/             # 消息系统
│   ├── Models/               # 模型集成
│   ├── Tools/                # 工具调用
│   ├── Structure-Output/     # 结构化输出
│   ├── Streaming/            # 流式处理
│   └── Short-term-Memory/    # 短期记忆管理
├── Middleware/               # 中间件机制
├── Advanced-Usage/           # 高级用法
├── pyproject.toml           # 项目配置和依赖
└── requirements.txt         # 传统依赖文件（兼容性）
```

### 学习路径
项目按照 LangChain 官方文档顺序组织：
1. **基础组件**（Core-components/）：先学习核心接口
2. **中间件**（Middleware/）：理解扩展机制
3. **高级用法**（Advanced-Usage/）：掌握复杂场景

### 技术栈
- **核心框架**：LangChain v1.2（LTS 版本）
- **运行时**：LangGraph v0.2+（代理编排）
- **模型集成**：langchain-openai、langchain-community
- **向量存储**：ChromaDB
- **开发工具**：black、ruff、mypy、pytest

## 代码规范

### Python 版本
- 目标版本：Python 3.13
- 使用类型提示（Type hints）
- 遵循 PEP 8 标准

### 配置参考
项目已配置以下工具的配置文件：
- `pyproject.toml`：包含 black、ruff、mypy、pytest 配置
- 行长度：88 字符（black 标准）
- 类型检查：严格模式（mypy）

## LangChain 特定指南

### 依赖版本管理
- LangChain v1.x 是长期支持版本
- langchain-core 提供基础接口
- 社区集成在 langchain-community 中
- 避免直接依赖 @langchain/classic（已弃用）

### 代理开发模式
```python
# 推荐使用 create_agent API（LangChain v1.x 标准）
from langchain.agents import create_agent

# 避免使用 create_react_agent（已弃用）
# 避免使用 legacy 模块
```

### 环境变量
使用 `.env` 文件管理 API 密钥：
```bash
# .env 文件示例
OPENAI_API_KEY=your_key_here
ANTHROPIC_API_KEY=your_key_here
GOOGLE_API_KEY=your_key_here
SILICONFLOW_API_KEY=your_key_here
```

在代码中使用：
```python
from dotenv import load_dotenv
load_dotenv()
```

## 工作流程建议

### 1. 学习新概念
- 在对应的目录下创建 Jupyter notebook
- 按照官方文档顺序实践
- 添加中文注释解释核心概念

### 2. 代码实践
- 先在 notebook 中实验
- 提取可重用代码到 Python 模块
- 编写测试验证理解

### 3. 质量控制
- 提交前运行代码检查
- 确保类型提示完整
- 验证示例代码可运行

## 故障排除

### 常见问题
1. **导入错误**：检查 uv 是否已安装所有依赖
2. **版本冲突**：使用 uv 的锁文件机制
3. **API 密钥**：确保 `.env` 文件已配置

### 调试建议
- 使用 `import langchain; print(langchain.__version__)` 检查版本
- 查看 LangChain 官方文档获取最新 API
- 使用 MCP 工具查询文档（docs-langchain）

## 扩展项目

### 添加新学习模块
1. 在 `Core-components/` 下创建对应目录
2. 添加 Jupyter notebook 文件
3. 更新 README.md 中的导航
4. 确保代码示例可运行

### 添加测试
1. 在项目根目录创建 `tests/` 目录
2. 使用 pytest 测试框架
3. 遵循现有配置（见 pyproject.toml）

## 参考资源

- [LangChain 官方文档](https://docs.langchain.com/oss/python/langchain/overview)
- [LangGraph 文档](https://docs.langchain.com/oss/python/langgraph/overview)
- [组件架构指南](https://docs.langchain.com/oss/python/langchain/component-architecture)
- [迁移指南 v1.x](https://docs.langchain.com/oss/python/releases/langchain-v1)