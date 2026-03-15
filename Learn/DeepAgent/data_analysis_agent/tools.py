"""
数据分析Agent的工具模块

此模块包含数据分析Agent所需的核心工具，用于读取、分析和可视化CSV数据，
并生成markdown格式的分析报告。
"""

import os
import json
from typing import Optional, Dict, Any
import pandas as pd
import matplotlib
matplotlib.use('Agg')  # 使用非 GUI 后端
import matplotlib.pyplot as plt
import seaborn as sns
from langchain.tools import tool
from pathlib import Path
import warnings

# 设置matplotlib中文字体和样式
plt.rcParams['font.sans-serif'] = ['SimHei', 'DejaVu Sans']
plt.rcParams['axes.unicode_minus'] = False
sns.set_style("whitegrid")
warnings.filterwarnings('ignore')

# 支持的图表类型
SUPPORTED_PLOT_TYPES = {
    "histogram": "直方图，用于查看数值变量的分布",
    "scatter": "散点图，用于查看两个数值变量之间的关系",
    "bar": "条形图，用于分类变量的计数或汇总统计",
    "box": "箱线图，用于查看数值变量的分布和异常值",
    "heatmap": "热力图，用于查看相关性矩阵",
    "line": "折线图，用于时间序列数据或趋势分析",
}

@tool
def read_csv(file_path: str, preview_rows: int = 5) -> str:
    """
    读取CSV文件并返回数据预览和基本信息

    Args:
        file_path: CSV文件路径
        preview_rows: 预览的行数，默认5行

    Returns:
        str: 包含文件信息和数据预览的格式化字符串

    Raises:
        FileNotFoundError: 如果文件不存在
        ValueError: 如果文件不是CSV格式或无法解析
    """
    # 安全检查：验证文件路径
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"文件不存在: {file_path}")

    if not file_path.lower().endswith('.csv'):
        raise ValueError(f"文件必须是CSV格式: {file_path}")

    try:
        # 读取CSV文件
        df = pd.read_csv(file_path)

        # 获取基本信息
        file_info = {
            "文件路径": file_path,
            "行数": len(df),
            "列数": len(df.columns),
            "列名": list(df.columns),
            "数据类型": {col: str(dtype) for col, dtype in df.dtypes.items()},
            "缺失值统计": df.isnull().sum().to_dict(),
            "文件大小": f"{os.path.getsize(file_path) / 1024:.2f} KB",
        }

        # 数据预览
        preview = df.head(preview_rows)

        # 格式化输出
        output = "# CSV文件分析报告\n\n"
        output += "## 文件基本信息\n"
        for key, value in file_info.items():
            if key == "列名":
                output += f"- **{key}**: {', '.join(value)}\n"
            elif key == "数据类型":
                output += f"- **{key}**:\n"
                for col, dtype in value.items():
                    output += f"  - {col}: {dtype}\n"
            elif key == "缺失值统计":
                output += f"- **{key}**:\n"
                for col, count in value.items():
                    if count > 0:
                        output += f"  - {col}: {count}个缺失值\n"
            else:
                output += f"- **{key}**: {value}\n"

        output += f"\n## 数据预览 (前{preview_rows}行)\n"
        output += preview.to_string()

        return output

    except Exception as e:
        return f"读取CSV文件时出错: {str(e)}"

@tool
def analyze_data(file_path: str, include_correlation: bool = True) -> str:
    """
    对CSV文件进行基本统计分析

    Args:
        file_path: CSV文件路径
        include_correlation: 是否计算数值列的相关性矩阵

    Returns:
        str: 包含统计分析的markdown格式报告
    """
    # 安全检查
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"文件不存在: {file_path}")

    try:
        df = pd.read_csv(file_path)

        output = "# 数据统计分析报告\n\n"

        # 1. 基本描述性统计
        output += "## 1. 描述性统计\n"
        numeric_cols = df.select_dtypes(include=['int64', 'float64']).columns
        if len(numeric_cols) > 0:
            desc_stats = df[numeric_cols].describe()
            output += desc_stats.to_string()
        else:
            output += "没有数值列可用于描述性统计\n"

        # 2. 缺失值分析
        output += "\n## 2. 缺失值分析\n"
        missing_stats = df.isnull().sum()
        missing_percent = (missing_stats / len(df)) * 100

        missing_df = pd.DataFrame({
            '缺失值数量': missing_stats,
            '缺失值百分比': missing_percent
        })
        output += missing_df.to_string()

        # 3. 唯一值分析（针对分类列）
        output += "\n## 3. 唯一值分析\n"
        categorical_cols = df.select_dtypes(include=['object']).columns
        for col in categorical_cols:
            unique_count = df[col].nunique()
            top_values = df[col].value_counts().head(5)
            output += f"\n**{col}**:\n"
            output += f"- 唯一值数量: {unique_count}\n"
            output += f"- 前5个最常见值:\n"
            for value, count in top_values.items():
                output += f"  - {value}: {count}次 ({count/len(df)*100:.1f}%)\n"

        # 4. 相关性分析
        if include_correlation and len(numeric_cols) > 1:
            output += "\n## 4. 相关性分析\n"
            correlation_matrix = df[numeric_cols].corr()
            output += correlation_matrix.to_string()

            # 识别强相关性（绝对值>0.7）
            strong_corr = []
            for i in range(len(numeric_cols)):
                for j in range(i+1, len(numeric_cols)):
                    corr_value = correlation_matrix.iloc[i, j]
                    if abs(corr_value) > 0.7:
                        strong_corr.append({
                            '变量1': numeric_cols[i],
                            '变量2': numeric_cols[j],
                            '相关系数': f"{corr_value:.3f}"
                        })

            if strong_corr:
                output += "\n**强相关性 (>0.7)**:\n"
                for corr in strong_corr:
                    output += f"- {corr['变量1']} 与 {corr['变量2']}: {corr['相关系数']}\n"

        # 5. 数据质量建议
        output += "\n## 5. 数据质量建议\n"
        issues = []

        # 检查缺失值
        high_missing = missing_percent[missing_percent > 20]
        if len(high_missing) > 0:
            issues.append(f"以下列缺失值超过20%: {', '.join(high_missing.index)}")

        # 检查数据分布
        for col in numeric_cols:
            skewness = df[col].skew()
            if abs(skewness) > 1:
                issues.append(f"{col}列偏度较高 ({skewness:.2f})，可能需要进行数据变换")

        if issues:
            for issue in issues:
                output += f"- ⚠️ {issue}\n"
        else:
            output += "- ✅ 数据质量良好\n"

        return output

    except Exception as e:
        return f"数据分析时出错: {str(e)}"

@tool
def generate_plot(
    file_path: str,
    plot_type: str,
    x_column: Optional[str] = None,
    y_column: Optional[str] = None,
    save_path: Optional[str] = None
) -> str:
    """
    生成数据可视化图表

    Args:
        file_path: CSV文件路径
        plot_type: 图表类型，必须是SUPPORTED_PLOT_TYPES中的一种
        x_column: X轴列名（可选）
        y_column: Y轴列名（可选）
        save_path: 图表保存路径（可选）

    Returns:
        str: 包含图表信息的markdown格式报告
    """
    # 验证参数
    if plot_type not in SUPPORTED_PLOT_TYPES:
        return f"不支持的图表类型: {plot_type}。支持的类型: {', '.join(SUPPORTED_PLOT_TYPES.keys())}"

    if not os.path.exists(file_path):
        raise FileNotFoundError(f"文件不存在: {file_path}")

    try:
        df = pd.read_csv(file_path)

        # 设置默认保存路径
        if save_path is None:
            save_dir = os.path.join(os.path.dirname(file_path), "plots")
            os.makedirs(save_dir, exist_ok=True)
            plot_name = f"{plot_type}_{os.path.basename(file_path).replace('.csv', '')}.png"
            save_path = os.path.join(save_dir, plot_name)

        # 根据图表类型生成可视化
        plt.figure(figsize=(10, 6))

        if plot_type == "histogram":
            if x_column is None:
                # 自动选择第一个数值列
                numeric_cols = df.select_dtypes(include=['int64', 'float64']).columns
                if len(numeric_cols) > 0:
                    x_column = numeric_cols[0]
                else:
                    return "没有数值列可用于生成直方图"

            plt.hist(df[x_column].dropna(), bins=30, edgecolor='black', alpha=0.7)
            plt.xlabel(x_column)
            plt.ylabel('频率')
            plt.title(f'{x_column}的分布直方图')
            plt.tight_layout()

        elif plot_type == "scatter":
            if x_column is None or y_column is None:
                numeric_cols = df.select_dtypes(include=['int64', 'float64']).columns
                if len(numeric_cols) >= 2:
                    x_column, y_column = numeric_cols[0], numeric_cols[1]
                else:
                    return "需要至少两个数值列来生成散点图"

            plt.scatter(df[x_column], df[y_column], alpha=0.6)
            plt.xlabel(x_column)
            plt.ylabel(y_column)
            plt.title(f'{x_column} vs {y_column} 散点图')
            plt.tight_layout()

        elif plot_type == "bar":
            if x_column is None:
                # 自动选择第一个分类列
                categorical_cols = df.select_dtypes(include=['object']).columns
                if len(categorical_cols) > 0:
                    x_column = categorical_cols[0]
                else:
                    return "没有分类列可用于生成条形图"

            value_counts = df[x_column].value_counts().head(20)  # 限制前20个
            value_counts.plot(kind='bar')
            plt.xlabel(x_column)
            plt.ylabel('计数')
            plt.title(f'{x_column}的计数条形图')
            plt.xticks(rotation=45, ha='right')
            plt.tight_layout()

        elif plot_type == "box":
            if x_column is None:
                numeric_cols = df.select_dtypes(include=['int64', 'float64']).columns
                if len(numeric_cols) > 0:
                    df[numeric_cols].plot(kind='box')
                    plt.title('数值列的箱线图')
                else:
                    return "没有数值列可用于生成箱线图"
            else:
                plt.boxplot(df[x_column].dropna())
                plt.xlabel(x_column)
                plt.title(f'{x_column}的箱线图')
            plt.tight_layout()

        elif plot_type == "heatmap":
            numeric_cols = df.select_dtypes(include=['int64', 'float64']).columns
            if len(numeric_cols) < 2:
                return "需要至少两个数值列来生成热力图"

            corr_matrix = df[numeric_cols].corr()
            sns.heatmap(corr_matrix, annot=True, fmt='.2f', cmap='coolwarm',
                       center=0, square=True, linewidths=1)
            plt.title('相关性热力图')
            plt.tight_layout()

        elif plot_type == "line":
            if x_column is None:
                return "折线图需要指定X轴列"

            if y_column is None:
                # 绘制所有数值列
                numeric_cols = df.select_dtypes(include=['int64', 'float64']).columns
                for col in numeric_cols:
                    plt.plot(df[x_column], df[col], label=col)
                plt.legend()
                plt.title(f'{x_column}与各数值列的关系')
            else:
                plt.plot(df[x_column], df[y_column])
                plt.title(f'{x_column} vs {y_column} 折线图')

            plt.xlabel(x_column)
            plt.ylabel('数值')
            plt.xticks(rotation=45)
            plt.tight_layout()

        # 保存图表
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
        plt.close()

        # 生成报告
        output = f"# 可视化图表生成报告\n\n"
        output += f"## 图表信息\n"
        output += f"- **图表类型**: {plot_type}\n"
        output += f"- **图表描述**: {SUPPORTED_PLOT_TYPES[plot_type]}\n"
        if x_column:
            output += f"- **X轴**: {x_column}\n"
        if y_column:
            output += f"- **Y轴**: {y_column}\n"
        output += f"- **保存路径**: `{save_path}`\n"

        # 添加markdown图片引用
        output += f"\n## 图表预览\n"
        output += f"![{plot_type}图表]({save_path})\n"

        return output

    except Exception as e:
        return f"生成图表时出错: {str(e)}"

@tool
def save_markdown_report(content: str, output_path: str) -> str:
    """
    将分析结果保存为markdown格式的报告文件

    Args:
        content: markdown格式的内容
        output_path: 输出文件路径

    Returns:
        str: 保存结果的确认信息
    """
    try:
        # 确保输出目录存在
        output_dir = os.path.dirname(output_path)
        if output_dir:
            os.makedirs(output_dir, exist_ok=True)

        # 写入文件
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(content)

        file_size = os.path.getsize(output_path) / 1024

        return f"✅ Markdown报告已成功保存\n\n**文件信息**:\n- 路径: `{output_path}`\n- 大小: {file_size:.2f} KB\n- 编码: UTF-8"

    except Exception as e:
        return f"保存Markdown报告时出错: {str(e)}"

def get_all_tools():
    """获取所有工具函数"""
    return [read_csv, analyze_data, generate_plot, save_markdown_report]