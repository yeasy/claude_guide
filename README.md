# Claude 技术指南

> 从零开始，系统掌握 Anthropic Claude 的核心能力与最佳实践

---

## 这本书是关于什么的？

本书是一本面向初学者和进阶用户的 Claude 完整学习指南。我们将系统性地介绍 Claude 的核心能力体系，包括：

- **[提示工程（Prompt Engineering）](02_prompt/README.md)**：与 Claude 高效沟通的艺术
- **[工具使用（Tool Use）](03_tools/README.md)**：让 Claude 调用外部 API 和服务
- **[模型上下文协议（MCP）](04_mcp/README.md)**：连接 Claude 与外部世界的标准接口
- **[计算机操控（Computer Use）](05_computer_use/README.md)**：Claude 自主操作桌面环境
- **[Skills 系统](06_skills/README.md)**：可复用的定制化工作流
- **[代码执行与 Agentic Coding](07_coding/README.md)**：Claude 作为自主编程助手

本书基于最新的Claude 模型（包括 Claude 3.5 Sonnet、Claude 4 Opus、Claude 4.5 Sonnet 等），提供经过验证的最佳实践。

---

## 目标读者

本书适合以下人群：

| 读者类型 | 你将获得什么 |
|---------|-------------|
| **AI 应用开发者** | 掌握 Claude API 的高级用法，构建生产级 AI 应用 |
| **产品经理 / 业务人员** | 理解 Claude 能力边界，规划 AI 产品路线图 |
| **自动化工程师** | 利用 Claude 构建端到端工作流自动化 |
| **AI 研究爱好者** | 深入理解大语言模型的能力演进与设计原理 |
| **Claude 用户** | 提升日常使用效率，解锁高级功能 |

**前置知识要求**：
- 基础编程经验（Python/JavaScript 优先，但非必需）
- 对大语言模型有初步了解
- 能够访问 Claude（[claude.ai](https://claude.ai) 或 [API](https://claude.com/platform/api)）

---

## 你将学到什么

完成本书学习后，你将能够：

### 🎯 基础能力
- [ ] 理解 Claude 的能力矩阵与模型选择策略
- [ ] 编写高质量的系统提示词（System Prompt）
- [ ] 使用 XML 标签结构化复杂指令
- [ ] 应用少样本学习（Few-shot Learning）和思维链（Chain of Thought）

### 🔧 中级技能
- [ ] 定义并调用自定义工具（Tool Use）
- [ ] 实现多轮对话与上下文管理
- [ ] 使用 Files API 处理文档
- [ ] 配置 MCP 服务器连接外部数据源

### 🚀 高级应用
- [ ] 构建具备 Computer Use 能力的 AI Agent
- [ ] 设计可复用的 Skills 工作流
- [ ] 使用 Claude Code SDK 实现 Agentic Coding
- [ ] 优化 Token 使用与成本控制
- [ ] 部署生产级 Claude 应用架构

---

## 本书结构

本书采用渐进式学习路径：

```
第一部分：基础篇
├── Claude 概览与模型选择
└── 提示工程核心技术

第二部分：工具篇
├── Tool Use 工具调用
├── MCP 模型上下文协议
└── Computer Use 计算机操控

第三部分：进阶篇
├── Skills 技能系统
├── Agentic Coding 与 Claude Code
└── Agent 架构设计

第四部分：实战篇
├── 企业级应用案例
├── 成本优化与性能调优
└── 安全与伦理考量
```

---

## 关于本书

本书基于 Anthropic 官方文档、开发者社区最佳实践及行业案例整理编撰，力求内容准确、实用、包括最新的特性。主要面向 Claude 3.5 Sonnet / Claude 4 系列 / Claude 4.5 系列模型。

---

## 开始阅读

点击 [目录](SUMMARY.md)，或从 [第一章：认识 Claude](01_intro/README.md) 开始你的学习之旅。

> 💡 **提示**：建议边阅读边实践。每章都提供可运行的代码示例，确保你拥有 [Claude](https://claude.ai) 访问权限以获得最佳学习体验。
