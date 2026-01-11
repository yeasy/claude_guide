## 本章小结：万物互联的基石

MCP (Model Context Protocol) 标志着 AI 应用开发进入了一个标准化的新时代。它终结了“手写胶水代码连接数据”的蛮荒时期，开启了“即插即用”的模块化时代。

### 核心知识点回顾

#### 协议的价值
*   **标准化 (Standardization)**：Client 和 Server 之间通过通用的 JSON-RPC 2.0 协议对话。
*   **解耦 (Decoupling)**：AI 开发者不需要关心底层数据源的实现，工具开发者不需要适配所有 AI 模型。
*   **USB-C 类比**：让连接数据变得像插外设一样简单。

#### 架构三支柱 (The Three Pillars)
*   **Resources (资源)**：被动的数据源，供模型“阅读” (Read Context)。
    *   *例：文件内容、数据库表 Schema、日志流。*
*   **Tools (工具)**：主动的操作，供模型“执行” (Take Action)。
    *   *例：提交代码、发送消息、重启服务。*
*   **Prompts (提示)**：预设的模版，供模型“调用” (Access Expertise)。
    *   *例：服务器自带的分析专家模版。*

#### 实战配置
*   **配置文件**：`claude_desktop_config.json` 是核心枢纽。
*   **多源融合**：我们可以同时挂载 GitHub, SQLite, Filesystem 等多个 Server，通过组合它们的能力，让 Claude 瞬间变身为全栈工程师或数据分析师。

#### 自定义开发
*   **FastMCP (Python)**：基于装饰器的极速开发体验，适合快速验证。
*   **TypeScript SDK**：类型安全，适合构建复杂的生产级 Server。
*   **设计原则**：工具原子化、描述清晰化、错误处理优雅化。

### 开发者自检清单

- [ ] **已配置环境**：我是否成功在 Claude Desktop 中通过 MCP 连上了本地文件夹？
- [ ] **理解权限**：我知道 MCP Server 只能访问我显式授权的文件或 API。
- [ ] **会用组合拳**：我尝试过让 Claude 先从数据库查数据，再写到本地文件的跨 Server 操作吗？
- [ ] **能写扩展**：如果找不到现成的 Server，我是否有能力用 Python 快速写一个简单的 Tool 暴露给 Claude？

### 下一站：打破数字世界的这堵墙

MCP 解决了“API 连接”的问题。但这个世界上还有大量软件**没有 API**，或者 API 极其难用。我们如何让 AI 操作那些陈旧 ERP 系统、复杂的图形界面软件，或者简单的网页？

答案是：**像人一样，去看，去点，去敲键盘。**

➡️ [第五章：Computer Use 计算机控制](../05_computer_use/README.md)
