## 本章小结

在 AI 应用的早期（2023 年），业界关注“它能做什么”；现在，关注点已转向“做这件事要花多少钱”。本章讨论如何降低成本、提高速度。

### 核心知识点回顾

#### Token 经济学

*   Token 是计费单位，也是算力单位。
*   Haiku, Sonnet, Opus 构成明确的价格阶梯。
*   先算 ROI，再决定用哪个模型，不要大材小用。

#### Prompt Caching：缓存

*   长文本应用（Long Context App）从缓存中受益最大。
*   通过识别重复前缀（Prefix），它可以显著降低重复输入成本和首 token 延迟；实际幅度取决于缓存命中率、TTL、模型和输出占比。
*   最佳实践：把稳定的 System Prompt、工具定义和大段背景资料放在动态用户输入之前。

#### Context Management：上下文

*   200K/1M 上下文很大，但也很贵。
*   Sliding Window：最简单，丢弃旧对话。
*   Summarization：总结旧对话。
*   Distillation：只提取状态。

#### Routing & Cascading：路由与级联

*   Router：按复杂度分发请求，简单任务交给 Haiku，复杂任务交给 Opus。
*   Cascading：先让 Haiku 尝试，只有它失败（Unit Test Fail）时才升级到 Sonnet。

### 开发者自检清单

- [ ] **缓存命中**：我的应用是否启用了 Prompt Caching？命中率有达到 50% 吗？
- [ ] **模型分级**：我是否全线都在用 Sonnet？即使是简单的“提取名字”任务？
- [ ] **成本监控**：我能否实时看到昨天的 Token 消耗账单？
- [ ] **清理策略**：我的 Context 里是否堆积了大量无效的 HTML 源码或报错日志？

### 下一章

前面各章让 Claude 更聪明（Skills）、更能干（MCP）、更便宜（Optimization），剩下的问题是它是否安全：用户让它写病毒，它会不会写？用户试图通过注入攻击套取数据库密码，它会不会泄露？

[第十一章](../11_safety/README.md)讨论 AI 的 **安全与伦理 (Trust & Safety)**，这是所有 AI 应用上线前必须回答的问题。

➡️ [安全与伦理](../11_safety/README.md)

---

> 📝 **发现错误或有改进建议？** 欢迎提交 [Issue](https://github.com/yeasy/claude_guide/issues) 或 [PR](https://github.com/yeasy/claude_guide/pulls)。
