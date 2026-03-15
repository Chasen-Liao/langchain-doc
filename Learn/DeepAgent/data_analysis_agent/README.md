# 数据分析Agent

基于硅基流动API和Deep Agents框架构建的数据分析Agent，能够读取CSV文件、进行统计分析、生成可视化图表，并输出markdown格式的分析报告。

## 功能特性

- ✅ 支持读取和分析CSV文件
- ✅ 提供基本统计分析和数据质量评估
- ✅ 生成多种可视化图表（直方图、散点图、条形图、箱线图、热力图、折线图）
- ✅ 输出markdown格式的完整分析报告
- ✅ 集成硅基流动API（支持Qwen、GLM、DeepSeek等开源模型）
- ✅ 基于Deep Agents框架，支持任务规划和人机交互
- ✅ 安全检查和错误处理

## 快速开始

### 1. 环境准备

确保已安装Python 3.13+和[uv](https://github.com/astral-sh/uv)包管理器。

```bash
# 安装uv（如果尚未安装）
pip install uv

# 或在Windows上使用pip
python -m pip install uv
```

### 2. 安装依赖

```bash
# 使用uv安装项目依赖
uv sync

# 或使用pip安装
pip install -e .
```

### 3. 配置API密钥

创建 `.env` 文件并添加硅基流动API密钥：

```bash
SILICONFLOW_API_KEY=your_api_key_here
```

您可以在 [硅基流动官网](https://siliconflow.cn/) 获取API密钥。

### 4. 运行示例

```bash
# 运行示例程序
python main.py --mode example

# 或使用交互模式
python main.py --mode interactive

# 指定API密钥
python main.py --mode example --api-key your_api_key
```

## 项目结构

```
data_analysis_agent/
├── main.py              # 主程序入口
├── config.py           # 硅基流动API配置
├── tools.py           # 数据分析工具定义
├── pyproject.toml     # 项目配置和依赖管理（uv兼容）
├── README.md          # 项目说明
├── sample_data/       # 示例数据目录
│   └── sales_data.csv # 示例销售数据
└── skills/            # 技能目录
    └── data_analysis_skill.md  # 数据分析技能文档
```

## 工具说明

Agent提供以下工具：

### 1. `read_csv(file_path: str, preview_rows: int = 5)`
- 读取CSV文件并返回基本信息
- 显示文件大小、行数、列数、数据类型、缺失值统计
- 提供数据预览

### 2. `analyze_data(file_path: str, include_correlation: bool = True)`
- 执行基本统计分析
- 包括描述性统计、缺失值分析、唯一值分析、相关性分析
- 提供数据质量建议

### 3. `generate_plot(file_path: str, plot_type: str, x_column: str = None, y_column: str = None, save_path: str = None)`
- 生成可视化图表
- 支持：直方图、散点图、条形图、箱线图、热力图、折线图
- 自动保存为PNG格式

### 4. `save_markdown_report(content: str, output_path: str)`
- 保存markdown格式的分析报告
- 支持中文字符
- 文件大小统计

## 支持的图表类型

| 类型 | 描述 | 适用场景 |
|------|------|----------|
| `histogram` | 直方图 | 数值变量分布 |
| `scatter` | 散点图 | 两个数值变量关系 |
| `bar` | 条形图 | 分类变量计数 |
| `box` | 箱线图 | 分布和异常值 |
| `heatmap` | 热力图 | 相关性矩阵 |
| `line` | 折线图 | 时间序列趋势 |

## 硅基流动模型支持

通过 `config.py` 配置，支持以下模型：

- `qwen2.5-7b-instruct` (默认)
- `qwen2.5-14b-instruct`
- `glm-4-9b-chat`
- `deepseek-v3`
- `yi-34b-chat`

## 安全注意事项

⚠️ **重要提示**: 本项目使用默认后端（文件系统访问），在生产环境中应考虑：

1. **沙箱环境**: 实际部署时应使用真正的沙箱环境
2. **权限控制**: 限制文件访问权限
3. **输入验证**: 对所有文件路径进行安全检查
4. **资源限制**: 限制内存和CPU使用

## 故障排除

### 常见问题

1. **API密钥错误**
   ```
   ❌ 错误: 未设置硅基流动API密钥
   ```
   解决方案：设置 `SILICONFLOW_API_KEY` 环境变量或使用 `--api-key` 参数

2. **依赖安装失败**
   ```
   ImportError: No module named 'deepagents'
   ```
   解决方案：使用 `uv sync` 或 `pip install -e .` 安装依赖

3. **图表中文显示问题**
   解决方案：确保系统中安装了中文字体，或修改 `tools.py` 中的字体设置

### 调试模式

```bash
# 查看详细错误信息
python main.py --mode example 2>&1 | more
```

## 扩展开发

### 添加新工具

1. 在 `tools.py` 中使用 `@tool` 装饰器定义新函数
2. 在 `get_all_tools()` 函数中添加新工具
3. 在 `main.py` 中更新系统提示，指导Agent何时使用新工具

### 集成新模型

1. 在 `config.py` 的 `SUPPORTED_MODELS` 字典中添加新模型
2. 在 `get_llm()` 函数中支持新模型参数

### 创建自定义技能

1. 在 `skills/` 目录下创建 `SKILL.md` 文件
2. 按照Deep Agents技能格式编写文档
3. 在Agent配置中启用技能加载

## 许可证

MIT License - 详见项目根目录的LICENSE文件

## 贡献指南

1. Fork 项目
2. 创建功能分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 开启 Pull Request

## 联系方式

- 项目维护者: Chasen
- 邮箱: 2558891266@qq.com
- 项目地址: [LangChain学习仓库](https://github.com/yourusername/langchain-learning)

---

**提示**: 此项目主要用于学习和演示目的，生产环境使用前请进行充分测试和安全评估。