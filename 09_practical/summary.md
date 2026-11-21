## 本章小结

技术的价值在于应用。
本章从代码编辑器转向复杂的真实商业场景。

### 核心知识点回顾

#### 客户服务

*   客服 Agent 应当解决问题，不能推卸责任。
*   用 **RAG** 提供知识，用 **Tools** 提供操作能力，用 **Persona** 设定语气。
*   **Human Handoff** 不是失败，而是负责任的做法。

#### 文档处理

*   **Claude Vision** 让 OCR 变成了 “OCR + Understanding”。
*   从合同比对到发票录入，AI 正在改变 Back-office 的工作流。
*   关键点在于 **Structured Output** (JSON)，这是连接 AI 与 ERP 的桥梁。

#### 数据分析

*   **Code Interpreter** 模式比单纯的 LLM 推理更可靠：让 AI 写代码计算，而不是心算。
*   **Text-to-SQL** 打开了数仓的大门，但必须做好权限隔离和语句审查。

#### 质量保证

*   AI 在 QA 中的作用不限于写单测。
*   **Visual Regression Testing** 利用 AI 的视觉能力发现 UI 错位，这是传统工具做不到的。
*   **Log Analysis** 利用 AI 从海量日志中定位根因。

### 开发者自检清单

- [ ] **高频场景**：我选择的落地场景是否是高频、重复且枯燥的？（如发票录入）
- [ ] **容错设计**：如果 AI 判错了发票金额，我的系统有对应的审核流程 (HITL) 吗？
- [ ] **数据安全**：在处理客户数据时，我是否进行了脱敏？是否符合 GDPR？
- [ ] **用户预期**：我是否明确告知用户对面是 AI？

### 下一章

企业应用必须核算成本。
GPT-5.5-pro 和 Claude Opus 能力很强，但价格也高。如果应用每天有 100 万次调用，每一分钱的 Token 成本都会被放大。
要让 AI 更快、更省，可以借助提示缓存、批处理和模型分层路由，目标是把账单降低一个数量级。

[第十章](../10_optimization/README.md)介绍 **Optimization & Tuning**。

➡️ [成本优化与性能调优](../10_optimization/README.md)

---

> 📝 **发现错误或有改进建议？** 欢迎提交 [Issue](https://github.com/yeasy/claude_guide/issues) 或 [PR](https://github.com/yeasy/claude_guide/pulls)。
