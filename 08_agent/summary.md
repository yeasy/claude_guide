## 本章小结

本章讨论的焦点从“如何向 Chatbot 提问”转向“如何构建能自主完成工作的数字员工”，即 Agent Engineering（智能体工程）。

### 核心知识点回顾

#### Agent 的组成

*   **Brain (LLM)**: 核心决策中枢。新项目可从 Claude Sonnet 5.5 开始评测；既有 Sonnet 4.6 与 Sonnet 5 工作负载按迁移清单灰度升级。
*   **Planning (ReAct/Plan-Solve)**: 决定是“走一步看一步”还是“谋定而后动”。
*   **Memory (RAG/VectorDB)**: 超越上下文窗口限制，让 Agent 拥有长期记忆。
*   **Action (MCP)**: 连接现实世界的四肢。

#### 双系统思考

*   **System 1 (LLM)**: 快速直觉反应。
*   **System 2 (Running Code/Extended Thinking)**: 慢速逻辑验证。
*   未来的 Agent 一定是混合这两种系统：用 System 1 快速提案，用 System 2 严格审查。

#### 多 Agent 协作

*   **Multi-Agent Systems**: 分工专业化。与其用一个超级 Prompt 做所有事，不如用三个简单的 Prompt 分别充当 Researcher, Coder, Reviewer。
*   **Orchestration**: 无论是层级式（Leader-Follower）还是接力棒式（Handoff），关键在于清晰的 **状态共享** 和 **边界定义**。

### 开发者自检清单

- [ ] **模式选择**：我面对的任务是探索性的（用 ReAct）还是路径清晰的（用 Plan-and-Solve）？
- [ ] **记忆设计**：我的 Agent 真的需要记住三天前的事情吗？如果需要，我是否配置了向量数据库？
- [ ] **防死循环**：我是否设置了最大迭代次数 (e.g. `max_loops=15`)？
- [ ] **成本监控**：在开启 Extended Thinking 或 Multi-Agent 时，我是否计算过单次任务的 Token 成本？

### 下一章

下一章分析几个真实的 **企业级应用案例**，说明这些 Agent 架构概念如何落地为生产力。

➡️ [企业级应用案例](../09_practical/README.md)

---

> 📝 **发现错误或有改进建议？** 欢迎提交 [Issue](https://github.com/yeasy/claude_guide/issues) 或 [PR](https://github.com/yeasy/claude_guide/pulls)。
