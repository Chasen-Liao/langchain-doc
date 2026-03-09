# LangChain 学习指南

[![Python Version](https://img.shields.io/badge/python-3.8%2B-blue)](https://www.python.org/)
[![LangChain Version](https://img.shields.io/badge/langchain-1.0%2B-green)](https://www.langchain.com/)
[![License](https://img.shields.io/badge/license-MIT-lightgrey)](LICENSE)

这是我学习 LangChainV1.x 框架的开源仓库，是按照Langchain官网的doc顺序来编排的，并且补充了很多 Langchain中的核心概念

## 📚 快速导航

### 核心组件
- [🤖 Agents（智能代理）](Core-components/Agents/) - 学习如何创建和配置 LangChain Agents
- [💬 Messages（消息系统）](Core-components/Messages/) - 理解消息传递和处理机制
- [🧠 Models（模型集成）](Core-components/Models/) - 集成各种 LLM 模型提供商
- [🔧 Tools（工具调用）](Core-components/Tools/) - 创建和使用自定义工具
- [📊 Structure Output（结构化输出）](Core-components/Structure-Output/) - 控制模型输出格式
- [⚡ Streaming（流式处理）](Core-components/Streaming/) - 实现实时流式响应
- [🧠 Short-term Memory（短期记忆）](Core-components/Short-term-Memory/) - 管理对话状态和上下文

### 高级用法
- [🔗 Advanced Usage（高级用法）](Advanced-Usage/) - 探索高级功能和最佳实践

### 中间件
- [🔄 Middleware（中间件）](Middleware/) - 了解中间件机制和自定义扩展

## 🚀 开始学习

### 环境设置
```bash
# 克隆仓库
git clone https://github.com/your-username/langchain-doc.git
cd langchain-doc

# 安装依赖
uv pip install -r requirements.txt
```


## 📖 当前内容

### 已完成章节
- [Agents 基础](Core-components/Agents/agents.ipynb) - 智能代理的基本概念和创建方法

### 待完善章节
- Messages 系统
- Models 集成
- Tools 开发
- 结构化输出
- 流式处理
- 短期记忆管理
- 中间件机制
- 高级用法



## 🤝 参与贡献
欢迎提交 Pull Request 来完善本学习指南！您可以：
- 添加新的学习章节
- 改进现有内容
- 修复错误或更新信息
- 提供更好的示例代码

## 📄 许可证
本项目采用 MIT 许可证 - 查看 [LICENSE](LICENSE) 文件了解详情。

## 🙏 致谢
感谢所有为 LangChain 生态系统做出贡献的开发者们！

---

<div align="center">
<sub>构建更好的 LLM 应用，从学习 LangChain 开始！</sub>
</div>