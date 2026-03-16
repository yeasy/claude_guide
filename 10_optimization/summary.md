## 本章小结：AI 时代的精益工程

在 AI 浪潮的早期（2023年），大家都在关注“它能做什么”。
到了现在（2026年），关注点已经转移到了“多少钱能做这件事”。
本章就是关于 **如何省钱** 和 **如何提速** 的工程指南。

### 核心知识点回顾

#### Token 经济学

*   Token 是计费单位，也是算力单位。
*   Haiku, Sonnet, Opus 构成了明确的价格阶梯。
*   永远先算 ROI，再决定用哪个模型。不要用牛刀杀鸡。

#### Prompt Caching：缓存

*   这是长文本应用（Long Context App）的救星。
*   通过识别重复前缀（Prefix），它可以让 API 成本直降 90%，延迟直降 80%。
*   **最佳实践**: 总是把 System Prompt 和大段背景资料放在最前面。

#### Context Management：上下文

*   200k 很大，但也很贵。
*   **Sliding Window**: 最简单，丢弃旧对话。
*   **Summarization**: 最智能，总结旧对话。
*   **Distillation**: 最极客，只提取状态。

#### Routing & Cascading：路由与级联

*   **Router**: 一个聪明的看门人，把简单任务扔给 Haiku，复杂任务交给 Opus。
*   **Cascading**: 让 Haiku 先试，只有在它搞砸（Unit Test Fail）的时候，才请 Sonnet 出山救火。

### 开发者自检清单

- [ ] **缓存命中**：我的应用是否启用了 Prompt Caching？命中率有达到 50% 吗？
- [ ] **模型分级**：我是否全线都在用 Sonnet？即使是简单的“提取名字”任务？
- [ ] **成本监控**：我能否实时看到昨天的 Token 消耗账单？
- [ ] **清理策略**：我的 Context 里是否堆积了大量无效的 HTML 源码或报错日志？

### 下一站：为 AI 加上护栏

已经让 Claude 变得聪明（Skills）、能干（MCP）、便宜（Optimization）。
现在，只剩下一个问题：**它安全吗？**
如果用户让它写一个病毒，它会写吗？如果用户试图通过注入攻击套取数据库密码，它会给吗？

[第十一章](../11_safety/README.md)，将探讨 AI 的 **安全与伦理 (Trust & Safety)**，这是所有 AI 应用上线前的最后一道必答题。

➡️ [安全与伦理](../11_safety/README.md)

---

> 📝 **发现错误或有改进建议？** 欢迎提交 [Issue](https://github.com/yeasy/claude_guide/issues) 或 [PR](https://github.com/yeasy/claude_guide/pulls)。
