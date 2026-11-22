## 本章小结

MCP (Model Context Protocol) 使 AI 应用开发走向标准化：连接数据不再依赖手写胶水代码，而是以“即插即用”的模块方式完成。

### 核心知识点回顾

#### 协议的价值

*   **标准化 (Standardization)**：Client 和 Server 之间通过通用的 JSON-RPC 2.0 协议对话。
*   **解耦 (Decoupling)**：AI 开发者不需要关心底层数据源的实现，工具开发者不需要适配所有 AI 模型。
*   **USB-C 类比**：连接数据像插外设一样简单。

#### 架构三支柱

*   **Resources（资源）**：被动的数据源，供模型“阅读” (Read Context)。
    *   *例：文件内容、数据库表 Schema、日志流。*
*   **Tools（工具）**：主动的操作，供模型“执行” (Take Action)。
    *   *例：提交代码、发送消息、重启服务。*
*   **Prompts（提示）**：预设的模版，供模型“调用” (Access Expertise)。
    *   *例：服务器自带的分析专家模版。*

#### 实战配置

*   **配置文件**：`claude_desktop_config.json` 是核心枢纽。
*   **多源融合**：可以同时挂载 GitHub, SQLite, Filesystem 等多个 Server，组合它们的能力，让 Claude 承担全栈工程师或数据分析师的工作。

#### 自定义开发

*   **MCPServer（Python，1.x 名为 FastMCP）**：基于装饰器，开发快，适合快速验证。
*   **TypeScript SDK**：类型安全，适合构建复杂的生产级 Server。
*   **设计原则**：工具原子化、描述清晰、错误处理得当。

### 开发者自检清单

- [ ] **已配置环境**：我是否成功在 Claude Desktop 中通过 MCP 连上了本地文件夹？
- [ ] **理解权限**：我知道 MCP 本身不强制隔离；实际访问边界取决于宿主审批、Server 实现、进程沙箱、文件系统/API 凭据和配置 scope。
- [ ] **会组合使用**：我尝试过让 Claude 先从数据库查数据，再写到本地文件的跨 Server 操作吗？
- [ ] **能写扩展**：如果找不到现成的 Server，我是否有能力用 Python 快速写一个简单的 Tool 暴露给 Claude？

### 下一章

MCP 解决了“API 连接”的问题，但还有大量软件 **没有 API**，或者 API 极其难用。要让 AI 操作陈旧的 ERP 系统、复杂的图形界面软件或简单的网页，就需要让它 **像人一样看屏幕、点鼠标、敲键盘**。

➡️ [第五章：Computer Use 计算机操控](../05_computer_use/README.md)

---

> 📝 **发现错误或有改进建议？** 欢迎提交 [Issue](https://github.com/yeasy/claude_guide/issues) 或 [PR](https://github.com/yeasy/claude_guide/pulls)。
