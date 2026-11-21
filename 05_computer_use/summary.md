## 本章小结

Computer Use 使大模型从“聊天机器人”走向能够直接操作软件的“操作者 (Agent)”。

### 核心知识点回顾

#### 范式转移

*   **API-First vs GUI-First**：API 是给机器用的，GUI 是给人用的。Computer Use 让 AI 能像人一样通过 GUI 工作，解决了 99% 的软件没有 API 带来的集成难题。
*   **视觉弹性**：基于视觉的识别（“点击那个蓝色的登录按钮”）比固定选择器（`#login-btn-v2`）更能适应轻微 UI 变化，但仍需要截图校验、重试、日志和人工确认。

#### 工作原理

*   这是一个 **OODA 循环**：观察（截图）-> 判断（视觉模型）-> 决策(ReAct) -> 行动（鼠标/键盘）。
*   **三大工具**：`computer`（操作键鼠）、`bash_20250124`（命令行）和 `text_editor_20250728` / `str_replace_based_edit_tool`（文本编辑）构成了 Claude 的基本工具集。

#### 安全至上

*   Computer Use 能力强，风险也高。
*   **Docker 隔离** 是底线，绝不能在无隔离的主机上直接运行。
*   **HITL（人机回环）** 是关键操作的最后防线。

#### 最佳实践

*   **混合架构**：能用 SQL 查库，就不要让 AI 去点数据库管理软件的 GUI。API + Computer Use = 最佳 ROI。
*   **提示工程**：在此模式下，Prompt 需要包含屏幕分辨率、视觉特征描述（Visual Grounding）等新要素。

### 开发者自检清单

- [ ] **沙箱环境**：我是否在 Docker 中运行 Demo，而不是在我的个人 MacBook 主机上？
- [ ] **权限控制**：我是否限制了容器的网络访问，防止数据外泄？
- [ ] **成本意识**：我是否意识到每一步操作都伴随着高额的截图 Token 消耗？
- [ ] **容错设计**：我的代码里是否包含了 `try-retry` 逻辑，以应对 UI 加载慢或点击失效的情况？

### 下一章

具备 Computer Use 后，Claude 像一个刚入职的实习生，能看懂屏幕、会点鼠标。
要胜任更专业的岗位，还需要掌握特定领域的“专业技能”，比如编写高质量的 Python 代码，或撰写符合 SEO 规范的文章。

下一章介绍为 Claude 提供这类技能的 **Skills**。

➡️ [第六章：Skills 技能系统](../06_skills/README.md)

---

> 📝 **发现错误或有改进建议？** 欢迎提交 [Issue](https://github.com/yeasy/claude_guide/issues) 或 [PR](https://github.com/yeasy/claude_guide/pulls)。
