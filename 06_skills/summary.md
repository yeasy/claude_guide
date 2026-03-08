## 本章小结：打造你的 AI 专家团队

本章介绍了如何通过 **Skills** 将 Claude 从一个通用全才变成特定领域的专家。

### 核心知识点回顾

#### 概念定义

*   **Skills = System Prompt + Tools + Knowledge**。
*   它不同于简单的 Prompt，它是一个包含完整上下文和可执行能力的 **软件包**。
*   核心理念是 **On-Demand Loading (按需加载)**：只在需要时才注入上下文，节省 Token 并减少干扰。

#### 工程化结构

*   一个 Skill 就是一个文件夹。
*   **`manifest.json`**：定义元数据和触发词。
*   **`skill.md`**：定义角色和流程。
*   **`docs/`**：外挂知识库 (RAG)。
*   **`examples/`**：Few-Shot 样本。

#### 多层级应用

*   **Built-in Skills**：开箱即用，覆盖文档分析、数据清洗、可视化等通用需求。
*   **Custom Skills**：企业自定义，覆盖内部合规、私有代码框架、特殊业务流程。

#### 组合与编排

*   **Chaining (串行)**：调研 -> 写作 -> 合规。
*   **Routing (路由)**：根据用户意图，自动分发给最合适的 Expert Skill。

### 开发者自检清单

- [ ] **结构规范**：我的 Skill 文件夹里是否包含了 `manifest.json` 和 `skill.md`？
- [ ] **示例丰富**：我是否提供了至少 3 个 Few-Shot 示例来固定输出格式？
- [ ] **高内聚**：我的 Skill 是否专注于解决单一领域的问题，而不是试图包罗万象？
- [ ] **文档清晰**：如果是企业内部 Skill，我是否挂载了最新的内部文档？

### 下一站：代码的艺术

有了 Skills，我们离真正的自动化又近了一步。
在所有的 Skill 中，最重要的莫过于 **Coding Skill**。因为代码即法律（Code is Law），代码即世界。
如何让 Claude 写出高质量、无 Bug、可维护的代码？如何让它甚至能自己修 Bug？

让我们进入[第七章](../07_coding/README.md)，探索 Claude 最被程序员称道的能力——**Agentic Coding**。

➡️ [Agentic Coding 智能编程](../07_coding/README.md)
