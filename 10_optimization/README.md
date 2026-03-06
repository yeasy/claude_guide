# 第十章 成本优化与性能调优

合理管理成本和优化性能是生产应用的关键。

```mermaid
graph TD
    classDef s1 fill:#E65100,stroke:#333,stroke-width:2px,color:white,font-weight:bold
    classDef s2 fill:#1565C0,stroke:#333,stroke-width:2px,color:white,font-weight:bold
    classDef s3 fill:#2E7D32,stroke:#333,stroke-width:2px,color:white,font-weight:bold
    classDef s4 fill:#7B1FA2,stroke:#333,stroke-width:2px,color:white,font-weight:bold
    classDef center fill:#FFF3E0,stroke:#E65100,stroke-width:3px,color:#333,font-weight:bold

    C["💰 Cost Optimization<br/>Strategies"]:::center
    C --> T["1⃣ Token Pricing<br/>Input/Output<br/>per-token billing"]:::s1
    C --> P["2⃣ Prompt Caching<br/>Cache static context<br/>90% cost reduction"]:::s2
    C --> W["3⃣ Context Window<br/>Manage token budget<br/>Summarize + Trim"]:::s3
    C --> M["4⃣ Model Selection<br/>Haiku < Sonnet < Opus<br/>Right model for task"]:::s4
```

---

## 本章重点

- Token 计费原理
- Prompt Caching 提示缓存
- 上下文窗口管理
- 模型选择与成本权衡

---

## 章节导航

| 章节 | 主题 |
|------|------|
| [10.1](10.1_pricing.md) | Token 计费原理 |
| [10.2](10.2_caching.md) | Prompt Caching 提示缓存 |
| [10.3](10.3_context_mgmt.md) | 上下文窗口管理 |
| [10.4](10.4_selection.md) | 模型选择与成本权衡 |
