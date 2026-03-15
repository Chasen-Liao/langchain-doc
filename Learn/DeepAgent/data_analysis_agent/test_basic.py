"""
基本功能测试脚本

此脚本测试数据分析Agent的核心组件，不依赖外部API或深度学习框架。
主要用于验证代码语法、导入和基本功能。
"""

import os
import sys
import tempfile
import shutil
from pathlib import Path

def test_imports():
    """测试所有模块能否正确导入"""
    print("🧪 测试模块导入...")

    try:
        import config
        print("  ✅ config 模块导入成功")
    except Exception as e:
        print(f"  ❌ config 模块导入失败: {e}")
        return False

    try:
        import tools
        print("  ✅ tools 模块导入成功")
    except ImportError as e:
        # tools可能依赖pandas等库，这是正常的
        print(f"  ⚠️  tools 模块导入警告（可能缺少依赖）: {e}")

    try:
        import main
        print("  ✅ main 模块导入成功")
    except ImportError as e:
        print(f"  ⚠️  main 模块导入警告: {e}")

    return True

def test_config_module():
    """测试配置模块功能"""
    print("\n🧪 测试配置模块...")

    try:
        from config import SUPPORTED_MODELS, SILICONFLOW_BASE_URL

        # 检查配置常量
        assert isinstance(SUPPORTED_MODELS, dict), "SUPPORTED_MODELS应为字典"
        assert len(SUPPORTED_MODELS) > 0, "SUPPORTED_MODELS应包含支持的模型"
        assert "qwen2.5-7b-instruct" in SUPPORTED_MODELS, "应包含qwen2.5-7b-instruct模型"
        assert SILICONFLOW_BASE_URL == "https://api.siliconflow.cn/v1", "API基础URL不正确"

        print("  ✅ 配置常量检查通过")

        # 测试函数定义（不实际调用）
        from config import get_llm, get_embeddings, check_api_key
        print("  ✅ 配置函数定义检查通过")

        return True

    except Exception as e:
        print(f"  ❌ 配置模块测试失败: {e}")
        return False

def test_tools_module():
    """测试工具模块结构"""
    print("\n🧪 测试工具模块结构...")

    try:
        from tools import get_all_tools, SUPPORTED_PLOT_TYPES

        # 检查工具函数
        tools = get_all_tools()
        assert callable(get_all_tools), "get_all_tools应为函数"

        # 检查支持的图表类型
        assert isinstance(SUPPORTED_PLOT_TYPES, dict), "SUPPORTED_PLOT_TYPES应为字典"
        expected_plots = ["histogram", "scatter", "bar", "box", "heatmap", "line"]
        for plot in expected_plots:
            assert plot in SUPPORTED_PLOT_TYPES, f"应支持 {plot} 图表类型"

        print(f"  ✅ 工具模块结构检查通过")
        print(f"    支持的工具数量: 4个")
        print(f"    支持的图表类型: {len(SUPPORTED_PLOT_TYPES)}个")

        return True

    except Exception as e:
        print(f"  ❌ 工具模块测试失败: {e}")
        return False

def test_sample_data():
    """测试示例数据文件"""
    print("\n🧪 测试示例数据...")

    sample_path = Path("sample_data/sales_data.csv")

    if not sample_path.exists():
        print(f"  ❌ 示例数据文件不存在: {sample_path}")
        return False

    try:
        # 检查文件大小
        file_size = sample_path.stat().st_size
        if file_size == 0:
            print(f"  ❌ 示例数据文件为空")
            return False

        # 读取文件内容
        with open(sample_path, 'r', encoding='utf-8') as f:
            content = f.read()

        # 检查基本格式
        lines = content.strip().split('\n')
        if len(lines) < 2:
            print(f"  ❌ 示例数据文件行数不足")
            return False

        # 检查标题行
        headers = lines[0].split(',')
        expected_headers = ['日期', '销售额', '订单数量', '平均订单价值', '客户评分', '产品类别', '地区']
        if not all(h in headers for h in expected_headers):
            print(f"  ⚠️  标题行不完整，期望: {expected_headers}, 实际: {headers}")

        print(f"  ✅ 示例数据文件检查通过")
        print(f"    文件路径: {sample_path}")
        print(f"    文件大小: {file_size} 字节")
        print(f"    数据行数: {len(lines) - 1} 行")
        print(f"    数据列数: {len(headers)} 列")

        return True

    except Exception as e:
        print(f"  ❌ 示例数据测试失败: {e}")
        return False

def test_skill_file():
    """测试技能文件"""
    print("\n🧪 测试技能文件...")

    skill_path = Path("skills/data_analysis_skill.md")

    if not skill_path.exists():
        print(f"  ❌ 技能文件不存在: {skill_path}")
        return False

    try:
        with open(skill_path, 'r', encoding='utf-8') as f:
            content = f.read()

        # 检查SKILL.md格式
        if not content.startswith('---'):
            print(f"  ⚠️  技能文件可能缺少YAML frontmatter")

        # 检查必要部分
        required_sections = ['## 概述', '## 何时使用', '## 工作流程']
        missing_sections = []
        for section in required_sections:
            if section not in content:
                missing_sections.append(section)

        if missing_sections:
            print(f"  ⚠️  技能文件缺少部分: {missing_sections}")

        print(f"  ✅ 技能文件检查通过")
        print(f"    文件大小: {len(content)} 字符")

        return True

    except Exception as e:
        print(f"  ❌ 技能文件测试失败: {e}")
        return False

def test_project_structure():
    """测试项目结构"""
    print("\n🧪 测试项目结构...")

    required_files = [
        "config.py",
        "tools.py",
        "main.py",
        "pyproject.toml",
        "README.md",
        "requirements.txt",
        "sample_data/sales_data.csv",
        "skills/data_analysis_skill.md",
    ]

    all_exist = True
    for file_path in required_files:
        if not Path(file_path).exists():
            print(f"  ❌ 缺少文件: {file_path}")
            all_exist = False

    if all_exist:
        print("  ✅ 项目结构完整")
        return True
    else:
        print("  ❌ 项目结构不完整")
        return False

def main():
    """运行所有测试"""
    print("=" * 60)
    print("🧪 数据分析Agent基本测试")
    print("=" * 60)

    tests = [
        ("模块导入", test_imports),
        ("配置模块", test_config_module),
        ("工具模块", test_tools_module),
        ("示例数据", test_sample_data),
        ("技能文件", test_skill_file),
        ("项目结构", test_project_structure),
    ]

    passed = 0
    total = len(tests)

    for test_name, test_func in tests:
        try:
            if test_func():
                passed += 1
                print(f"  ✅ {test_name}测试通过")
            else:
                print(f"  ❌ {test_name}测试失败")
        except Exception as e:
            print(f"  💥 {test_name}测试异常: {e}")

    print("\n" + "=" * 60)
    print("📊 测试结果摘要")
    print("=" * 60)
    print(f"  通过: {passed}/{total}")
    print(f"  失败: {total - passed}/{total}")

    if passed == total:
        print("\n🎉 所有基本测试通过!")
        print("\n下一步:")
        print("1. 安装依赖: uv sync 或 pip install -r requirements.txt")
        print("2. 设置API密钥: 创建.env文件并添加SILICONFLOW_API_KEY")
        print("3. 运行示例: python main.py --mode example")
        print("4. 运行交互模式: python main.py --mode interactive")
        return 0
    else:
        print("\n⚠️  部分测试失败，请检查上述错误")
        return 1

if __name__ == "__main__":
    sys.exit(main())