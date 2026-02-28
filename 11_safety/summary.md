## 本章小结：AI 的安全带

第十一章不是关于“如何让 AI 更强”，而是关于“如何让 AI 更可靠”。

### 核心知识点回顾

#### 宪法式 AI

*   **内在约束**: Claude 不仅是基于人类反馈训练的，更是基于一套明确的价值观（宪法）训练的。
*   这使得它在处理敏感话题时更加**有原则**，而不是一味讨好用户。

#### 护栏工程

*   不要裸奔。
*   **Input Guardrails**: 拦截 Prompt Injection 和 PII。
*   **Output Guardrails**: 过滤有害内容及格式错误。
*   **HITL**: 关键操作必须有人类确认。

#### 数据隐私

*   **API != Training**: 商业 API 数据不用于训练。
*   **Zero Retention**: 对于极致安全需求，可以使用零留存模式。
*   **Local Anonymization**: 在数据出门前就把它变成乱码。

#### 负责任的 AI

*   **Augmentation**: AI 是副驾驶，人类是机长。
*   **Bias Check**: 始终警惕模型可能存在的偏见，并用反事实测试去验证它。

### 全书结语

恭喜你！你已经读完了《Claude 指南：从入门到 Agent 工程化》的所有核心章节。
本书从最基础的 Prompt Engineering 开始，一路升级到 Tool Use, MCP, Computer Use, Agentic Coding 乃至复杂的 Agent Architecture。

现在的开发者，已经手握一把锤子（LLM），但这把锤子能变成螺丝刀、电钻甚至 CNC 机床。
未来的软件开发，将不再是“写代码”，而是“**训练和编排 Agent**”。

希望这本书能成为你在这个新时代的航海图。
Go build something amazing!

➡️ [附录：资源与工具清单](../12_appendix/README.md)
