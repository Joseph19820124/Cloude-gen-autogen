# AutoGen 多Agent代码开发工作流系统

![Python](https://img.shields.io/badge/Python-3.8%2B-blue)
![AutoGen](https://img.shields.io/badge/AutoGen-0.4.x-green)
![Gemini](https://img.shields.io/badge/Google%20Gemini-2.0%20Flash-orange)
![License](https://img.shields.io/badge/License-MIT-yellow)

基于 AutoGen 0.4.x 和 Google Gemini 2.0 Flash 模型的智能多Agent协作代码开发系统，通过三个专业角色的Agent协作，实现高质量的代码生成、审查和优化流程。

## 🌟 项目特色

- **三Agent协作模式**：代码编写者 → 代码审查者 → 代码优化者
- **轮询工作流**：采用Round-robin模式确保每个Agent按顺序参与
- **智能代码生成**：基于Google Gemini 2.0 Flash模型的强大代码生成能力
- **全面代码审查**：专业的代码质量评估和改进建议
- **自动化优化**：基于审查反馈的智能代码优化
- **交互式界面**：支持交互式和批处理两种运行模式
- **完善错误处理**：友好的用户体验和错误提示

## 🏗️ 系统架构

```
用户输入任务
      ↓
┌─────────────────┐
│   CodeWriter    │ ← 代码编写者：根据需求编写初始代码
│   (Agent 1)     │
└─────────────────┘
      ↓
┌─────────────────┐
│  CodeReviewer   │ ← 代码审查者：审查代码质量并提出改进建议
│   (Agent 2)     │
└─────────────────┘
      ↓
┌─────────────────┐
│ CodeOptimizer   │ ← 代码优化者：基于审查意见优化代码
│   (Agent 3)     │
└─────────────────┘
      ↓
   最终优化代码
```

## 🤖 Agent角色详解

### 1. CodeWriter (代码编写者)
**职责：**
- 根据用户提供的任务需求编写Python代码
- 确保代码具有良好的结构和可读性
- 添加必要的注释和文档字符串
- 遵循Python编程最佳实践
- 提供完整可运行的代码解决方案

### 2. CodeReviewer (代码审查者)
**职责：**
- 仔细审查提供的代码
- 识别潜在的问题、漏洞或改进空间
- 检查代码的性能、安全性、可读性和可维护性
- 提供具体的优化建议和最佳实践建议
- 指出任何潜在的边界情况或错误处理问题

### 3. CodeOptimizer (代码优化者)
**职责：**
- 基于原始代码和审查者的建议进行代码优化
- 实现审查者提出的改进建议
- 优化代码性能、可读性和可维护性
- 确保优化后的代码保持原有功能
- 添加更好的错误处理和边界情况处理

## 🚀 快速开始

### 环境要求

- Python 3.8+
- Google Gemini API密钥

### 安装依赖

```bash
pip install "autogen-agentchat[gemini]==0.4.0" python-dotenv
```

### 配置API密钥

#### 方法1：环境变量
```bash
export GEMINI_API_KEY="your-gemini-api-key-here"
```

#### 方法2：创建.env文件
```bash
echo "GEMINI_API_KEY=your-gemini-api-key-here" > .env
```

### 运行程序

```bash
python autogen_workflow.py
```

## 📖 使用示例

### 示例任务
程序启动后会自动运行一个斐波那契数列的示例任务：

```python
sample_task = """
创建一个Python函数，用于计算斐波那契数列的第n项。
要求：
1. 支持大数值计算
2. 包含输入验证
3. 提供递归和迭代两种实现方式
4. 包含性能测试功能
"""
```

### 交互式模式
示例完成后，程序会进入交互式模式，你可以输入任何代码开发需求：

```
🎯 AutoGen 代码开发工作流 - 交互式模式
输入 'quit' 或 'exit' 退出

请输入代码开发任务描述: 创建一个简单的Web爬虫
```

## 🔧 自定义配置

### 调整最大轮数
```python
# 默认3轮，可以根据需求调整
await workflow.execute_workflow(task_description, max_rounds=5)
```

### 直接传入API密钥
```python
workflow = CodeDevelopmentWorkflow(api_key="your-api-key")
```

## 📊 工作流程输出

系统会清晰显示每个Agent的工作成果：

```
================================================================================
📊 工作流执行结果
================================================================================

🤖 CodeWriter:
----------------------------------------
[初始代码版本]
...
----------------------------------------

🤖 CodeReviewer:
----------------------------------------
[代码审查反馈]
...
----------------------------------------

🤖 CodeOptimizer:
----------------------------------------
[最终优化代码]
...
----------------------------------------
```

## 🛠️ 代码结构

```
autogen_workflow.py
├── CodeDevelopmentWorkflow     # 主工作流类
│   ├── __init__()             # 初始化和配置
│   ├── _setup_agents()        # 设置三个Agent
│   ├── _setup_team()          # 配置轮询团队
│   ├── execute_workflow()     # 执行工作流
│   ├── _print_workflow_results() # 输出结果
│   └── run_interactive_session() # 交互式会话
└── main()                     # 主函数
```

## 🔍 技术特点

### AutoGen 0.4.x 新特性
- 使用最新的 `autogen_agentchat` API
- 支持 `RoundRobinGroupChat` 轮询模式
- 优化的消息传递机制
- 更好的错误处理和稳定性

### Google Gemini 2.0 Flash
- 最新的 Gemini 2.0 Flash 实验版模型
- 优秀的代码理解和生成能力
- 快速响应和高质量输出
- 支持长文本和复杂逻辑

## 🎯 适用场景

- **学习编程**：通过专业Agent的协作学习最佳实践
- **代码重构**：对现有代码进行审查和优化
- **原型开发**：快速生成高质量的代码原型
- **教学演示**：展示专业的代码开发流程
- **团队协作**：模拟真实的代码审查和优化过程

## ⚠️ 注意事项

1. **API密钥安全**：请妥善保管您的Gemini API密钥，不要提交到版本控制系统
2. **网络连接**：需要稳定的网络连接访问Google Gemini API
3. **依赖版本**：确保安装正确版本的AutoGen库 (0.4.0)
4. **使用限制**：注意Google Gemini API的使用限制和费用

## 🐛 故障排除

### 常见问题

1. **API密钥错误**
   ```
   ValueError: 请提供Gemini API密钥或设置GEMINI_API_KEY环境变量
   ```
   解决：检查API密钥是否正确设置

2. **依赖安装问题**
   ```
   ModuleNotFoundError: No module named 'autogen_agentchat'
   ```
   解决：重新安装依赖
   ```bash
   pip install "autogen-agentchat[gemini]==0.4.0"
   ```

3. **网络连接问题**
   ```
   ConnectionError: ...
   ```
   解决：检查网络连接和API服务状态

## 🤝 贡献指南

欢迎提交Issue和Pull Request来改进这个项目！

1. Fork本仓库
2. 创建功能分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 开启Pull Request

## 📄 许可证

本项目采用 MIT 许可证 - 查看 [LICENSE](LICENSE) 文件了解详情

## 🙏 致谢

- [Microsoft AutoGen](https://github.com/microsoft/autogen) - 强大的多Agent框架
- [Google Gemini](https://ai.google.dev/) - 优秀的AI模型服务
- 开源社区的支持和贡献

## 📞 联系方式

如有问题或建议，请通过以下方式联系：

- 创建 [Issue](https://github.com/Joseph19820124/Cloude-gen-autogen/issues)
- 发起 [Discussion](https://github.com/Joseph19820124/Cloude-gen-autogen/discussions)

---

⭐ 如果这个项目对你有帮助，请给它一个星标！