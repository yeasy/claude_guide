# Claude 技术指南

* [前言](README.md)

## 第一部分：基础篇

* [第一章：认识 Claude](01_intro/README.md)
  * [1.1 Anthropic 与 Claude 的诞生](01_intro/1.1_born.md)
  * [1.2 Claude 模型家族全景](01_intro/1.2_model_family.md)
  * [1.3 Claude 能做什么](01_intro/1.3_capabilities.md)
  * [1.4 如何选择合适的模型](01_intro/1.4_model_selection.md)

* [第二章：提示工程核心技术](02_prompt/README.md)
  * [2.1 提示词基础：清晰、直接、具体](02_prompt/2.1_basics.md)
  * [2.2 使用 XML 标签结构化指令](02_prompt/2.2_xml.md)
  * [2.3 系统提示词设计](02_prompt/2.3_system_prompt.md)
  * [2.4 少样本学习与示例设计](02_prompt/2.4_few_shot.md)
  * [2.5 思维链与逐步推理](02_prompt/2.5_cot.md)
  * [2.6 输出格式控制](02_prompt/2.6_format.md)
  * [2.7 提示词优化与调试](02_prompt/2.7_optimization.md)

## 第二部分：工具篇

* [第三章：工具](03_tools/README.md)
  * [3.1 工具概述与工作原理](03_tools/3.1_overview.md)
  * [3.2 定义工具 Schema](03_tools/3.2_schema.md)
  * [3.3 处理工具调用结果](03_tools/3.3_results.md)
  * [3.4 多工具编排与复杂流程](03_tools/3.4_orchestration.md)
  * [3.5 高级特性：程序化工具调用](03_tools/3.5_programmatic.md)
  * [3.6 管理大型工具库：工具搜索](03_tools/3.6_tool_search.md)

* [第四章：MCP 模型上下文协议](04_mcp/README.md)
  * [4.1 MCP 是什么：AI 的 USB-C](04_mcp/4.1_intro.md)
  * [4.2 MCP 架构与核心概念](04_mcp/4.2_architecture.md)
  * [4.3 配置与使用 MCP 服务器](04_mcp/4.3_config.md)
  * [4.4 常用 MCP 服务器实践](04_mcp/4.4_practice.md)
  * [4.5 开发自定义 MCP 服务器](04_mcp/4.5_custom.md)

* [第五章：Computer Use 计算机操控](05_computer_use/README.md)
  * [5.1 Computer Use 能力概述](05_computer_use/5.1_overview.md)
  * [5.2 工作原理：截图、识别、行动](05_computer_use/5.2_loop.md)
  * [5.3 环境配置与安全沙箱](05_computer_use/5.3_env.md)
  * [5.4 实战：构建桌面自动化 Agent](05_computer_use/5.4_practical.md)
  * [5.5 局限性与最佳实践](05_computer_use/5.5_best_practices.md)

## 第三部分：进阶篇

* [第六章：Skills 技能系统](06_skills/README.md)
  * [6.1 什么是 Claude Skills](06_skills/6.1_intro.md)
  * [6.2 Skills 的结构与组成](06_skills/6.2_structure.md)
  * [6.3 使用内置 Skills](06_skills/6.3_builtin.md)
  * [6.4 创建自定义 Skills](06_skills/6.4_custom.md)
  * [6.5 Skills 组合与高级用法](06_skills/6.5_combination.md)
  * [6.6 调试与优化 Skills](06_skills/6.6_debugging.md)

* [第七章：Agentic Coding 与 Claude Code](07_coding/README.md)
  * [7.1 Claude 作为编程助手](07_coding/7.1_assistant.md)
  * [7.2 Claude Code CLI 入门](07_coding/7.2_cli.md)
  * [7.3 Claude Code SDK 集成](07_coding/7.3_sdk.md)
  * [7.4 IDE 集成与工作流](07_coding/7.4_ide.md)
  * [7.5 自主编码实践与案例](07_coding/7.5_practical.md)

* [第八章：Agent 架构设计](08_agent/README.md)
  * [8.1 什么是 AI Agent](08_agent/8.1_intro.md)
  * [8.2 Agent 设计模式](08_agent/8.2_patterns.md)
  * [8.3 上下文管理与记忆](08_agent/8.3_memory.md)
  * [8.4 扩展思考](08_agent/8.4_extended_thinking.md)
  * [8.5 多 Agent 协作](08_agent/8.5_collaboration.md)

## 第四部分：实战篇

* [第九章：企业级应用案例](09_practical/README.md)
  * [9.1 智能客服系统](09_practical/9.1_customer_service.md)
  * [9.2 文档处理与知识库](09_practical/9.2_doc_processing.md)
  * [9.3 数据分析助手](09_practical/9.3_data_analysis.md)
  * [9.4 自动化测试与 QA](09_practical/9.4_qa_test.md)

* [第十章：成本优化与性能调优](10_optimization/README.md)
  * [10.1 Token 计费原理](10_optimization/10.1_pricing.md)
  * [10.2 提示缓存](10_optimization/10.2_caching.md)
  * [10.3 上下文窗口管理](10_optimization/10.3_context_mgmt.md)
  * [10.4 模型选择与成本权衡](10_optimization/10.4_selection.md)

* [第十一章：安全与伦理](11_safety/README.md)
  * [11.1 宪法式 AI](11_safety/11.1_cai.md)
  * [11.2 安全使用指南](11_safety/11.2_guardrail.md)
  * [11.3 数据隐私与合规](11_safety/11.3_privacy.md)
  * [11.4 负责任的 AI 应用](11_safety/11.4_responsible.md)
  * [11.5 对抗性攻击与防御](11_safety/11.5_adversarial.md)
  * [11.6 企业级合规与审计](11_safety/11.6_compliance.md)

* [结语：从工具到伙伴](EPILOGUE.md)

## 附录

* [附录 A：Claude API 快速参考](12_appendix/12.1_api_ref.md)
* [附录 B：常见问题解答](12_appendix/12.2_faq.md)
* [附录 C：术语表](12_appendix/12.3_glossary.md)
* [附录 D：延伸阅读与资源](12_appendix/12.4_resources.md)
* [附录 E：Claude 定价与成本参考](12_appendix/12.5_pricing.md)
