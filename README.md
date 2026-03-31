# LangChain 学习指南

[![Python Version](https://img.shields.io/badge/python-3.10%2B-blue)](https://www.python.org/)
[![LangChain Version](https://img.shields.io/badge/langchain-1.2%2B-green)](https://www.langchain.com/)
[![License](https://img.shields.io/badge/license-MIT-lightgrey)](LICENSE)

这是我学习 LangChain V1.x 框架的开源仓库，按照 LangChain 官方文档顺序编排，涵盖核心组件和高级用法。

## 📚 快速导航

### 核心组件

- [🤖 Agents（智能代理）](Core-components/Agents/) - 创建和配置 LangChain Agents
- [💬 Messages（消息系统）](Core-components/Messages/) - 消息传递和处理机制
- [🧠 Models（模型集成）](Core-components/Models/) - 集成各种 LLM 模型提供商
- [🔧 Tools（工具调用）](Core-components/Tools/) - 创建和使用自定义工具
- [📊 Structure Output（结构化输出）](Core-components/Structure-Output/) - 控制模型输出格式
- [⚡ Streaming（流式处理）](Core-components/Streaming/) - 实现实时流式响应
- [🧠 Short-term Memory（短期记忆）](Core-components/Short-term-Memory/) - 管理对话状态和上下文

### 高级用法

- [🔗 Context Engineering（上下文工程）](Advanced-Usage/) - 探索上下文工程的核心概念

### 中间件

- [🔄 Middleware（中间件）](Middleware/) - 中间件机制和自定义扩展

## 🚀 开始学习

### 环境设置

```bash
# 克隆仓库
git clone https://github.com/your-username/langchain-doc.git
cd langchain-doc

# 安装依赖
pip install -r requirements.txt

# 启动 Jupyter Lab
jupyter lab
```

## 📖 当前内容

### 核心组件

- [Agents 基础](Core-components/Agents/agents.ipynb) - 智能代理的基本概念和创建方法
- [Messages 系统](Core-components/Messages/messages.ipynb) - 消息传递和处理机制
- [Models 集成](Core-components/Models/model.ipynb) - LLM 模型集成实践
- [Tools 开发](Core-components/Tools/tools.ipynb) - 自定义工具的创建和使用
- [结构化输出](Core-components/Structure-Output/structure_output.ipynb) - 控制模型输出格式
- [流式处理](Core-components/Streaming/streaming.ipynb) - 实时流式响应实现
- [短期记忆管理](Core-components/Short-term-Memory/short_term_Memory.ipynb) - 对话状态和上下文管理

### 高级用法

- [上下文工程](Advanced-Usage/Context_engineering.ipynb) - 上下文工程核心概念

### 中间件

- [中间件概览](Middleware/overview.ipynb) - 中间件机制介绍
- [自定义中间件](Middleware/custom_middleware.ipynb) - 自定义中间件开发

## 🛠️ 技术栈

- **LangChain**: v1.2+
- **LangGraph**: 状态管理和编排
- **Jupyter**: 交互式学习环境
- **Python**: 3.10+

## 🤝 参与贡献

欢迎提交 Pull Request 来完善本学习指南！

## 📄 许可证

MIT 许可证 - 查看 [LICENSE](LICENSE) 文件了解详情。

---

<div align="center">
<sub>构建更好的 LLM 应用，从学习 LangChain 开始！</sub>
</div>
