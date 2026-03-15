---
name: data-analysis
description: 数据分析工作流程和最佳实践，包括数据读取、统计分析、可视化和报告生成
---

# 数据分析技能

## 概述

此技能提供数据分析的完整工作流程，从数据读取到报告生成，涵盖探索性数据分析(EDA)的各个方面。

## 何时使用

在以下情况下使用此技能：
- 需要分析CSV格式的数据文件
- 执行探索性数据分析(EDA)
- 生成统计摘要和可视化图表
- 创建markdown格式的分析报告
- 评估数据质量和提供改进建议

## 工作流程

### 1. 数据读取和初步检查
- 使用 `read_csv` 工具读取文件
- 检查基本信息：行数、列数、数据类型、缺失值
- 预览前几行数据了解数据结构

### 2. 统计分析
- 使用 `analyze_data` 工具执行基本分析
- 包括：描述性统计、缺失值分析、唯一值分析、相关性分析
- 识别数据质量问题（高缺失率、异常分布等）

### 3. 数据可视化
- 使用 `generate_plot` 工具创建图表
- 建议的可视化顺序：
  1. **直方图**：查看数值变量的分布
  2. **箱线图**：识别异常值和分布特征
  3. **散点图**：探索变量之间的关系
  4. **条形图**：显示分类变量的分布
  5. **热力图**：展示相关性矩阵
  6. **折线图**：分析时间序列趋势

### 4. 报告生成
- 使用 `save_markdown_report` 工具保存结果
- 报告应包含：
  - 执行摘要
  - 数据概览
  - 统计分析结果
  - 可视化图表（嵌入图片）
  - 数据质量评估
  - 关键洞察和建议

## 最佳实践

### 数据质量检查
1. **缺失值处理**：
   - 缺失率<5%：可以考虑删除或填充
   - 缺失率5-20%：需要分析原因，谨慎处理
   - 缺失率>20%：考虑删除该列或使用高级填充方法

2. **异常值检测**：
   - 使用箱线图识别异常值
   - 分析异常值是否代表真实现象或数据错误
   - 考虑对极偏分布进行对数变换

3. **数据类型验证**：
   - 确保数值列正确识别为数值类型
   - 日期时间列应转换为datetime格式
   - 分类变量应具有合理的唯一值数量

### 可视化指导原则
1. **图表选择**：
   - 分布分析：直方图或密度图
   - 关系分析：散点图或折线图
   - 比较分析：条形图或箱线图
   - 相关性：热力图

2. **图表优化**：
   - 添加清晰的标题和坐标轴标签
   - 使用适当的颜色方案
   - 控制图表尺寸为10x6英寸
   - 保存为300 DPI的PNG格式

3. **中文支持**：
   - 确保图表标题和标签支持中文
   - 使用SimHei或DejaVu Sans字体

### 报告编写建议
1. **结构清晰**：
   - 使用markdown标题组织内容
   - 重要发现使用强调格式
   - 代码和文件路径使用代码块

2. **内容完整**：
   - 包括数据来源和预处理步骤
   - 记录分析方法和假设
   - 提供可重复的分析步骤

3. **实用性**：
   - 提供具体的业务建议
   - 指出数据局限性和改进方向
   - 包含后续分析建议

## 常见分析模式

### 销售数据分析
```python
# 典型分析步骤
1. read_csv("sales_data.csv")
2. analyze_data("sales_data.csv", include_correlation=True)
3. generate_plot("sales_data.csv", "histogram", x_column="销售额")
4. generate_plot("sales_data.csv", "scatter", x_column="日期", y_column="销售额")
5. generate_plot("sales_data.csv", "bar", x_column="产品类别")
6. save_markdown_report(content, "sales_analysis_report.md")
```

### 用户行为分析
```python
# 典型分析步骤
1. read_csv("user_behavior.csv")
2. analyze_data("user_behavior.csv")
3. generate_plot("user_behavior.csv", "box", x_column="使用时长")
4. generate_plot("user_behavior.csv", "heatmap")
5. generate_plot("user_behavior.csv", "line", x_column="日期", y_column="活跃用户数")
```

### 金融数据分析
```python
# 典型分析步骤
1. read_csv("financial_data.csv")
2. analyze_data("financial_data.csv")
3. generate_plot("financial_data.csv", "histogram", x_column="收益率")
4. generate_plot("financial_data.csv", "scatter", x_column="风险等级", y_column="收益率")
5. generate_plot("financial_data.csv", "box", x_column="投资组合")
```

## 工具使用示例

### read_csv 工具
```python
# 基本使用
result = read_csv("data.csv")

# 自定义预览行数
result = read_csv("data.csv", preview_rows=10)
```

### analyze_data 工具
```python
# 基本统计分析
result = analyze_data("data.csv")

# 不包括相关性分析
result = analyze_data("data.csv", include_correlation=False)
```

### generate_plot 工具
```python
# 直方图
result = generate_plot("data.csv", "histogram", x_column="age")

# 散点图
result = generate_plot("data.csv", "scatter", x_column="income", y_column="spending")

# 自动选择列
result = generate_plot("data.csv", "heatmap")

# 指定保存路径
result = generate_plot("data.csv", "line", x_column="date", y_column="value", save_path="custom_plot.png")
```

### save_markdown_report 工具
```python
# 保存报告
report_content = "# 分析报告\n\n内容..."
result = save_markdown_report(report_content, "analysis_report.md")
```

## 故障排除

### 常见问题
1. **文件读取失败**
   - 检查文件路径是否正确
   - 确认文件编码为UTF-8
   - 验证CSV格式是否正确

2. **中文显示问题**
   - 确保系统中安装了中文字体
   - 检查matplotlib配置

3. **内存不足**
   - 对于大型文件，分批处理数据
   - 使用数据采样进行分析

4. **图表保存失败**
   - 检查保存目录的写权限
   - 确认磁盘空间充足

### 性能优化
1. **大型文件处理**：
   - 使用 `chunksize` 参数分批读取
   - 只加载需要的列
   - 采样数据进行分析

2. **内存管理**：
   - 及时关闭图表释放内存
   - 使用适当的数据类型（如float32代替float64）
   - 删除不再需要的中间变量

## 扩展资源

### 进一步学习
- [pandas官方文档](https://pandas.pydata.org/docs/)
- [matplotlib教程](https://matplotlib.org/stable/tutorials/index.html)
- [seaborn示例库](https://seaborn.pydata.org/examples/index.html)
- [探索性数据分析(EDA)指南](https://towardsdatascience.com/exploratory-data-analysis-eda-a-practical-guide-and-template-for-structured-data-abfbf3ee3bd9)

### 相关技能
- 数据清洗技能
- 机器学习建模技能
- 时间序列分析技能
- 商业智能报告技能

---

**版本**: 1.0.0
**最后更新**: 2024-03-14
**维护者**: 数据分析团队
**标签**: data-analysis, visualization, statistics, reporting