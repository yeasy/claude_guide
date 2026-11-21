## 本章小结

第十一章讨论的是如何让 AI 更可靠，而非更强。

### 核心知识点回顾

#### 宪法式 AI

*   **内在约束**: Claude 的训练既基于人类反馈，也基于一套明确的价值观（宪法）。
*   因此它处理敏感话题时更 **有原则**，不会一味讨好用户。

#### 护栏工程

*   不要让模型在没有防护的情况下直接面对用户。
*   **Input Guardrails**: 拦截 Prompt Injection 和 PII。
*   **Output Guardrails**: 过滤有害内容及格式错误。
*   **HITL**: 关键操作必须有人类确认。

#### 数据隐私

*   **API != Training**: 商业 API 数据不用于训练。
*   **Zero Retention**: 对于极致安全需求，可以使用零留存模式，但要逐功能、逐模型核对覆盖范围。
*   **Local Anonymization**: 数据离开本地前先脱敏。

#### 负责任的 AI

*   **Augmentation**: AI 是副驾驶，人类是机长。
*   **Bias Check**: 警惕模型可能存在的偏见，并用反事实测试验证。

### 小结

安全与伦理是 AI 工程化的基础。掌握这些原则，才能构建负责任的 AI 应用。

下一部分进入进阶篇，介绍 Claude 的前沿特性与上下文工程。

➡️ [第十三章：进阶能力](../13_advanced/README.md)

---

> 📝 **发现错误或有改进建议？** 欢迎提交 [Issue](https://github.com/yeasy/claude_guide/issues) 或 [PR](https://github.com/yeasy/claude_guide/pulls)。
