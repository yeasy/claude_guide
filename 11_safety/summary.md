## 本章小结：AI 的安全带

第十一章不是关于“如何让 AI 更强”，而是关于“如何让 AI 更可靠”。

### 核心知识点回顾

#### 宪法式 AI

*   **内在约束**: Claude 不仅是基于人类反馈训练的，更是基于一套明确的价值观（宪法）训练的。
*   这使得它在处理敏感话题时更加 **有原则**，而不是一味讨好用户。

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

### 小结

安全与伦理是 AI 工程化不可或缺的基石。掌握了这些原则，你就为构建负责任的 AI 应用打好了基础。

接下来，我们将进入进阶篇，探索 Claude 的前沿特性与上下文工程。

➡️ [第十三章：进阶能力](../13_advanced/README.md)

---

> 📝 **发现错误或有改进建议？** 欢迎提交 [Issue](https://github.com/yeasy/claude_guide/issues) 或 [PR](https://github.com/yeasy/claude_guide/pulls)。
