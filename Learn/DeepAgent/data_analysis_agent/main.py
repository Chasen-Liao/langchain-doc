"""
数据分析Agent主程序

基于硅基流动API和Deep Agents框架构建的数据分析Agent。
能够读取CSV文件、进行统计分析、生成可视化图表，并输出markdown格式的分析报告。

注意：此示例使用LocalShellBackend作为沙箱后端，仅用于演示目的。
在生产环境中应使用真正的沙箱环境以确保安全。
"""

import os
import sys
from pathlib import Path
from dotenv import load_dotenv

# 设置 UTF-8 编码支持（Windows 控制台）
if sys.platform == "win32":
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

# 添加项目根目录到Python路径
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

# 加载环境变量
load_dotenv()

# 检查硅基流动API密钥
if not os.getenv("SILICONFLOW_API_KEY"):
    print("⚠️  警告: SILICONFLOW_API_KEY环境变量未设置")
    print("请设置环境变量: export SILICONFLOW_API_KEY=your_api_key")
    print("或在项目根目录创建.env文件并添加: SILICONFLOW_API_KEY=your_api_key")
    print("您可以在 https://siliconflow.cn/ 获取API密钥")

def create_data_analysis_agent():
    """
    创建数据分析Agent

    Returns:
        AgentExecutor: 配置好的数据分析Agent
    """
    try:
        # 导入必要的模块
        from deepagents import create_deep_agent
        from langgraph.checkpoint.memory import MemorySaver

        # 导入自定义配置和工具
        from config import get_llm
        from tools import get_all_tools

        print("🔧 正在创建数据分析Agent...")

        # 1. 获取硅基流动的LLM实例
        print("   ⚙️  配置硅基流动API...")
        llm = get_llm(
            model_name="deepseek-ai/DeepSeek-V3.2",
            temperature=0.1,
            max_tokens=9999,
            streaming=False
        )
        print(f"   ✅ 使用模型: deepseek-ai/DeepSeek-V3.2")

        # 2. 获取所有工具
        print("   ⚙️  加载数据分析工具...")
        tools = get_all_tools()
        print(f"   ✅ 加载工具: {', '.join([tool.name for tool in tools])}")

        # 3. 创建检查点（用于多轮对话和中断恢复）
        print("   ⚙️  配置检查点...")
        checkpointer = MemorySaver()
        print("   ✅ 使用内存检查点")

        # 4. 配置后端（省略将使用默认backend）
        print("   ⚙️  配置后端...")
        print("   ✅ 使用默认后端（文件系统访问）")

        # 5. 配置中断（人机交互）选项
        # 这里配置对敏感操作（如保存文件）需要人工批准
        interrupt_on = {
            "save_markdown_report": True,  # 保存报告需要批准
            "generate_plot": False,        # 生成图表不需要批准
            "read_csv": False,             # 读取文件不需要批准
            "analyze_data": False,         # 分析数据不需要批准
        }

        # 6. 创建数据分析Agent
        print("   ⚙️  创建Deep Agent...")
        agent = create_deep_agent(
            model=llm,
            tools=tools,
            checkpointer=checkpointer,
            interrupt_on=interrupt_on,
            system_prompt="""
            你是一个专业的数据分析专家，擅长使用各种工具分析CSV数据。

            你的工作流程：
            1. 使用read_csv工具读取CSV文件，了解数据结构
            2. 使用analyze_data工具进行统计分析
            3. 使用generate_plot工具生成可视化图表
            4. 使用save_markdown_report工具保存完整的分析报告

            分析报告应包含：
            - 数据概览和基本信息
            - 统计摘要和关键指标
            - 可视化图表（使用generate_plot生成）
            - 数据质量评估和建议
            - 关键洞察和业务建议

            注意事项：
            - 始终使用中文输出分析结果
            - 生成的图表应保存为PNG格式
            - 最终报告应为markdown格式
            - 确保文件路径正确无误
            - 如果用户需要，可以提供多次分析和不同的可视化

            如果用户没有指定具体的分析需求，请执行完整的EDA（探索性数据分析）。
            """
        )

        print("   ✅ Agent创建成功!")
        print(f"   📋 可用工具: {len(tools)}个")
        print(f"   🛡️  需要人工批准的操作: {[k for k, v in interrupt_on.items() if v]}")

        return agent

    except ImportError as e:
        print(f"❌ 导入错误: {e}")
        print("请确保已安装所有依赖: pip install -e . 或 uv install")
        raise
    except Exception as e:
        print(f"❌ 创建Agent时出错: {e}")
        raise

def run_agent_example():
    """
    运行数据分析Agent示例

    此函数演示如何使用数据分析Agent处理示例数据。
    """
    print("=" * 60)
    print("📊 数据分析Agent示例")
    print("=" * 60)

    try:
        # 创建Agent
        agent = create_data_analysis_agent()

        # 创建示例数据文件（如果不存在）
        # 使用绝对路径，因为 deep agents 的文件系统后端需要绝对路径
        sample_data_path = project_root / "sample_data" / "sales_data.csv"
        if not sample_data_path.exists():
            print("\n📁 创建示例数据文件...")
            os.makedirs(sample_data_path.parent, exist_ok=True)

            # 创建示例销售数据
            import pandas as pd
            import numpy as np

            np.random.seed(42)
            dates = pd.date_range('2024-01-01', '2024-12-31', freq='D')
            data = {
                '日期': dates,
                '销售额': np.random.normal(10000, 2000, len(dates)),
                '订单数量': np.random.randint(50, 200, len(dates)),
                '平均订单价值': np.random.normal(150, 30, len(dates)),
                '客户评分': np.random.uniform(3.5, 5.0, len(dates)),
                '产品类别': np.random.choice(['电子产品', '服装', '家居', '食品', '书籍'], len(dates)),
                '地区': np.random.choice(['华北', '华东', '华南', '华中', '西北'], len(dates)),
            }

            df = pd.DataFrame(data)
            df.to_csv(sample_data_path, index=False, encoding='utf-8')
            print(f"✅ 示例数据已创建: {sample_data_path}")

        # 示例1：读取和分析数据
        print("\n" + "=" * 60)
        print("示例1: 读取和分析CSV文件")
        print("=" * 60)

        input_messages = [
            {
                "role": "user",
                "content": f"请分析这个CSV文件: {sample_data_path}\n"
                          "1. 先读取文件查看基本信息\n"
                          "2. 进行统计分析\n"
                          "3. 生成销售额的直方图和销售额与订单数量的散点图\n"
                          "4. 将分析结果保存为markdown报告\n"
            }
        ]

        print("🤖 Agent正在处理...")

        # 配置线程ID用于检查点
        config = {"configurable": {"thread_id": "example-session-1"}}

        # 执行Agent
        result = agent.invoke(
            {"messages": input_messages},
            config=config
        )

        # 输出结果
        print("\n📄 Agent响应:")
        print("-" * 40)

        # 提取最后一条消息
        if result and "messages" in result:
            last_message = result["messages"][-1]
            if "content" in last_message:
                print(last_message["content"])

        print("-" * 40)

        # 检查是否有中断（需要人工批准）
        if result and "__interrupt__" in result:
            print("\n⏸️  Agent执行被中断，等待人工批准...")
            print("使用以下命令继续执行:")
            print("  result = agent.invoke(Command(resume={'decisions': [{'type': 'approve'}]}), config=config)")

        print("\n✅ 示例执行完成!")
        print(f"📁 示例数据: {sample_data_path}")
        print(f"📄 分析报告: sample_data/analysis_report.md")

    except Exception as e:
        print(f"❌ 示例运行出错: {e}")
        import traceback
        traceback.print_exc()

def interactive_mode():
    """
    交互式模式：允许用户与Agent进行对话
    """
    print("=" * 60)
    print("💬 数据分析Agent交互模式")
    print("=" * 60)
    print("输入 'quit' 或 'exit' 退出")
    print("输入 'help' 查看可用命令")
    print("-" * 60)

    # 创建Agent
    try:
        agent = create_data_analysis_agent()
    except Exception as e:
        print(f"❌ 无法创建Agent: {e}")
        return

    # 配置线程ID
    thread_id = input("请输入会话ID (默认: interactive-session): ").strip()
    if not thread_id:
        thread_id = "interactive-session"

    config = {"configurable": {"thread_id": thread_id}}

    print(f"\n✅ 会话已启动: {thread_id}")
    print("现在你可以向Agent发送消息了!\n")

    while True:
        try:
            # 获取用户输入
            user_input = input("👤 你: ").strip()

            if user_input.lower() in ['quit', 'exit', '退出']:
                print("👋 再见!")
                break

            if user_input.lower() in ['help', '帮助']:
                print("\n📋 可用命令:")
                print("  - 分析文件: '分析 data/sales.csv'")
                print("  - 生成图表: '为data/sales.csv生成销售额直方图'")
                print("  - 保存报告: '将分析结果保存为report.md'")
                print("  - 查看帮助: 'help' 或 '帮助'")
                print("  - 退出: 'quit' 或 'exit' 或 '退出'")
                print()
                continue

            if not user_input:
                continue

            # 执行Agent
            result = agent.invoke(
                {"messages": [{"role": "user", "content": user_input}]},
                config=config
            )

            # 显示Agent响应
            if result and "messages" in result:
                last_message = result["messages"][-1]
                if "content" in last_message:
                    print(f"\n🤖 Agent: {last_message['content']}\n")

            # 检查中断
            if result and "__interrupt__" in result:
                print("\n⏸️  Agent需要人工批准才能继续执行。")
                print("请使用以下命令批准:")
                print("  result = agent.invoke(Command(resume={'decisions': [{'type': 'approve'}]}), config=config)")
                print("或拒绝:")
                print("  result = agent.invoke(Command(resume={'decisions': [{'type': 'reject', 'message': '理由'}]}), config=config)")
                print()

        except KeyboardInterrupt:
            print("\n\n👋 用户中断，退出程序")
            break
        except Exception as e:
            print(f"❌ 错误: {e}")
            continue

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="数据分析Agent")
    parser.add_argument(
        "--mode",
        choices=["example", "interactive"],
        default="example",
        help="运行模式: example (示例) 或 interactive (交互式)"
    )
    parser.add_argument(
        "--api-key",
        type=str,
        help="硅基流动API密钥 (可选，优先使用环境变量)"
    )

    args = parser.parse_args()

    # 如果提供了API密钥，设置环境变量
    if args.api_key:
        os.environ["SILICONFLOW_API_KEY"] = args.api_key

    # 检查API密钥
    if not os.getenv("SILICONFLOW_API_KEY"):
        print("❌ 错误: 未设置硅基流动API密钥")
        print("请使用以下方式之一设置:")
        print("  1. 设置环境变量: export SILICONFLOW_API_KEY=your_key")
        print("  2. 使用命令行参数: --api-key your_key")
        print("  3. 在项目根目录创建.env文件")
        sys.exit(1)

    # 根据模式运行
    if args.mode == "example":
        run_agent_example()
    elif args.mode == "interactive":
        interactive_mode()
    else:
        print(f"❌ 未知模式: {args.mode}")
        sys.exit(1)