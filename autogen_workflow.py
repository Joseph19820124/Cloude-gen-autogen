#!/usr/bin/env python3
"""
AutoGen 0.4.x 多Agent代码开发工作流系统
包含三个agent：代码编写者、代码审查者、代码优化者
采用轮询（round-robin）方式运作
"""

import asyncio
import os
from typing import List, Dict, Any
from autogen_agentchat.agents import AssistantAgent
from autogen_agentchat.teams import RoundRobinGroupChat
from autogen_agentchat.messages import TextMessage
from autogen_core.models import ChatCompletionClient
from autogen_ext.models.gemini import GeminiChatCompletionClient


class CodeDevelopmentWorkflow:
    """代码开发工作流类"""
    
    def __init__(self, api_key: str = None):
        """
        初始化工作流
        
        Args:
            api_key: Google Gemini API密钥，如果不提供则从环境变量获取
        """
        self.api_key = api_key or os.getenv("GEMINI_API_KEY")
        if not self.api_key:
            raise ValueError("请提供Gemini API密钥或设置GEMINI_API_KEY环境变量")
        
        # 初始化Gemini模型客户端
        self.model_client = GeminiChatCompletionClient(
            model="gemini-2.0-flash-exp",  # 使用Gemini 2.0 Flash模型
            api_key=self.api_key
        )
        
        # 初始化agents
        self._setup_agents()
        
        # 初始化团队
        self._setup_team()
    
    def _setup_agents(self):
        """设置三个agent"""
        
        # Agent 1: 代码编写者
        self.coder_agent = AssistantAgent(
            name="CodeWriter",
            model_client=self.model_client,
            system_message="""你是一个专业的Python代码编写者。
            
你的职责：
1. 根据用户提供的任务需求编写Python代码
2. 确保代码具有良好的结构和可读性
3. 添加必要的注释和文档字符串
4. 遵循Python编程最佳实践
5. 提供完整可运行的代码解决方案

请始终以清晰、实用的方式编写代码，并解释你的实现思路。
在回复的最后，请明确标识这是"初始代码版本"。"""
        )
        
        # Agent 2: 代码审查者
        self.reviewer_agent = AssistantAgent(
            name="CodeReviewer", 
            model_client=self.model_client,
            system_message="""你是一个经验丰富的代码审查专家。

你的职责：
1. 仔细审查提供的代码
2. 识别潜在的问题、漏洞或改进空间
3. 检查代码的性能、安全性、可读性和可维护性
4. 提供具体的优化建议和最佳实践建议
5. 指出任何潜在的边界情况或错误处理问题

请提供建设性的反馈，包括：
- 代码质量评估
- 具体的改进建议
- 性能优化建议
- 安全性考虑

在回复的最后，请明确标识这是"代码审查反馈"。"""
        )
        
        # Agent 3: 代码优化者
        self.optimizer_agent = AssistantAgent(
            name="CodeOptimizer",
            model_client=self.model_client, 
            system_message="""你是一个代码优化专家。

你的职责：
1. 基于原始代码和审查者的建议进行代码优化
2. 实现审查者提出的改进建议
3. 优化代码性能、可读性和可维护性
4. 确保优化后的代码保持原有功能
5. 添加更好的错误处理和边界情况处理

请提供：
- 优化后的完整代码
- 优化说明和改进点总结
- 与原始代码的主要差异说明

在回复的最后，请明确标识这是"最终优化代码"。"""
        )
    
    def _setup_team(self):
        """设置团队（轮询模式）"""
        self.team = RoundRobinGroupChat(
            participants=[
                self.coder_agent,
                self.reviewer_agent, 
                self.optimizer_agent
            ]
        )
    
    async def execute_workflow(self, task_description: str, max_rounds: int = 3) -> List[Dict[str, Any]]:
        """
        执行代码开发工作流
        
        Args:
            task_description: 任务描述
            max_rounds: 最大轮数
            
        Returns:
            包含所有消息的列表
        """
        print(f"🚀 开始执行代码开发工作流...")
        print(f"📝 任务描述: {task_description}")
        print(f"🔄 最大轮数: {max_rounds}")
        print("-" * 60)
        
        # 创建初始消息
        initial_message = TextMessage(
            content=f"请为以下任务开发Python代码：\n\n{task_description}",
            source="user"
        )
        
        # 执行团队对话
        result = await self.team.run(
            task=initial_message,
            termination_condition=lambda messages: len(messages) >= max_rounds * 3
        )
        
        # 打印结果
        self._print_workflow_results(result.messages)
        
        return result.messages
    
    def _print_workflow_results(self, messages: List[Any]):
        """打印工作流结果"""
        print("\n" + "="*80)
        print("📊 工作流执行结果")
        print("="*80)
        
        for i, message in enumerate(messages):
            if hasattr(message, 'source') and hasattr(message, 'content'):
                print(f"\n🤖 {message.source}:")
                print("-" * 40)
                print(message.content)
                print("-" * 40)
    
    async def run_interactive_session(self):
        """运行交互式会话"""
        print("🎯 AutoGen 代码开发工作流 - 交互式模式")
        print("输入 'quit' 或 'exit' 退出\n")
        
        while True:
            try:
                task = input("请输入代码开发任务描述: ").strip()
                
                if task.lower() in ['quit', 'exit', '退出']:
                    print("👋 感谢使用！")
                    break
                
                if not task:
                    print("⚠️ 请输入有效的任务描述")
                    continue
                
                await self.execute_workflow(task)
                print("\n" + "="*60 + "\n")
                
            except KeyboardInterrupt:
                print("\n👋 用户中断，退出程序")
                break
            except Exception as e:
                print(f"❌ 执行过程中出现错误: {e}")


async def main():
    """主函数"""
    try:
        # 初始化工作流（请确保设置了GEMINI_API_KEY环境变量）
        workflow = CodeDevelopmentWorkflow()
        
        # 示例任务
        sample_task = """
创建一个Python函数，用于计算斐波那契数列的第n项。
要求：
1. 支持大数值计算
2. 包含输入验证
3. 提供递归和迭代两种实现方式
4. 包含性能测试功能
        """
        
        print("🧪 运行示例任务...")
        await workflow.execute_workflow(sample_task)
        
        print("\n" + "="*60)
        print("示例完成！现在可以尝试交互式模式...")
        print("="*60 + "\n")
        
        # 运行交互式会话
        await workflow.run_interactive_session()
        
    except Exception as e:
        print(f"❌ 程序执行错误: {e}")
        print("💡 请检查：")
        print("   1. GEMINI_API_KEY 环境变量是否设置正确")
        print("   2. 网络连接是否正常")
        print("   3. AutoGen库是否正确安装")


if __name__ == "__main__":
    # 运行主程序
    asyncio.run(main())


# 使用示例和说明
"""
使用说明：

1. 安装依赖：
   pip install "autogen-agentchat[gemini]==0.4.0" python-dotenv

2. 设置环境变量：
   export GEMINI_API_KEY="your-gemini-api-key-here"
   
   或创建 .env 文件：
   GEMINI_API_KEY=your-gemini-api-key-here

3. 运行程序：
   python autogen_workflow.py

工作流程：
1. CodeWriter: 根据任务编写初始代码
2. CodeReviewer: 审查代码并提供改进建议  
3. CodeOptimizer: 基于审查意见优化代码

特性：
- 使用AutoGen 0.4.x版本的最新API
- 集成Google Gemini 2.0 Flash模型
- 轮询（Round-robin）模式确保每个agent按顺序参与
- 支持交互式和批处理模式
- 完整的错误处理和用户友好的输出
- 可配置的最大轮数控制
"""