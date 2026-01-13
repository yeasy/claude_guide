## 本章小结：构建智能体系统的艺术

从这章开始，讨论的焦点不再是"如何向 Chatbot 提问"，而是"如何构建一个能自主干活的数字员工"。这就是 Agent Engineering (智能体工程)。

### 核心知识点回顾

#### Agent 的解剖学
*   **Brain (LLM)**: 核心决策中枢。Claude 4.5 Sonnet 是目前的版本答案。
*   **Planning (ReAct/Plan-Solve)**: 决定是“走一步看一步”还是“谋定而后动”。
*   **Memory (RAG/VectorDB)**: 突破 200k Token 限制，让 Agent 拥有长期记忆。
*   **Action (MCP)**: 连接现实世界的四肢。

#### 思考的进化
*   **System 1 (LLM)**: 快速直觉反应。
*   **System 2 (Running Code/Extended Thinking)**: 慢速逻辑验证。
*   未来的 Agent 一定是混合这两种系统：用 System 1 快速提案，用 System 2 严格审查。

#### 集体智慧
*   **Multi-Agent Systems**: 术业有专攻。与其用一个超级 Prompt 做所有事，不如用三个简单的 Prompt 分别做一个 Researcher, Coder, Reviewer。
*   **Orchestration**: 无论是层级式（Leader-Follower）还是接力棒式（Handoff），关键在于清晰的**状态共享**和**边界定义**。

### 开发者自检清单

- [ ] **模式选择**：我面对的任务是探索性的（用 ReAct）还是路径清晰的（用 Plan-and-Solve）？
- [ ] **记忆设计**：我的 Agent 真的需要记住三天前的事情吗？如果需要，我是否配置了向量数据库？
- [ ] **防死循环**：我是否设置了最大迭代次数 (e.g. `max_loops=15`)？
- [ ] **成本监控**：在开启 Extended Thinking 或 Multi-Agent 时，我是否计算过单次任务的 Token 成本？

### 下一站：落地

Agent 架构听起来很酷，但它在真实世界中能用来干什么？是帮我订外卖，还是帮也是写财报？
下一章，我们将剖析几个真实的**企业级应用案例**，看看先驱者们是如何把这些概念变成生产力的。

➡️ [企业级应用案例](../09_practical/README.md)
