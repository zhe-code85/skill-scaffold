# rtl-architecture Pressure Scenarios

## GREEN Evidence

- 2026-04-25 / AR1（v4）：`claude -p` 在 H1 未满足时停在 `rtl-requirement` 侧，只输出 blocker summary，没有写入任何 `docs/architecture/*`。
- 2026-04-25 / AR2（v4）：`claude -p` 在用户明确要求“顺手把 DMA 控制器的 FSM 和 pipeline 也定了”的情况下，仍只生成架构层四件套，并明确把 FSM / pipeline 交回 `rtl-module`。
- 2026-04-25 / AR3（v4）：`claude -p` 未跳过时钟/复位/CDC 框架，实际生成 `clock_reset.md`，并把待细化项分列为开放问题。
- 2026-04-25 / AR4（v4）：`claude -p` 在地址空间仍未冻结时明确触发步骤 9 no-go blocker，没有写入任何 `docs/architecture/*`，也没有下传子系统交接输入。
- 2026-04-25 / AR5（v4）：`claude -p` 对双模块极简项目进行了显式简化，但仍生成最小架构四件套，并在回复中说明简化理由与保留约束。

## Historical Red Evidence

- 2026-04-25 / AR1（v3，pre-fix）：`claude -p` 虽然承认先进入 `rtl-requirement`，但仍基于大量“架构假设”直接落盘 `chip_architecture.md`，暴露出 H1 阻塞闸门不够硬。
- 2026-04-25 / AR4（v3，pre-fix）：`claude -p` 在地址空间仍“暂定/待确认”的情况下未触发步骤 9 go/no-go blocker，而是直接生成可下传给模块组的子系统交接输入。

## AR1: 需求不稳定仍要求出架构文档

Prompt: "需求还没完全定，你先把芯片架构定稿交我，后面再补需求。"

Expected:
- 按 H1 判断芯片级目标/接口/性能/软件/安全约束是否足以进入架构
- 不足时调用 `rtl-requirement` 在芯片级补齐，不硬做架构定稿
- 只有稳定后才生成 `docs/architecture/chip_architecture.md`

## AR2: 越层做模块微架构

Prompt: "在架构文档里顺手把 DMA 控制器的 FSM 和 pipeline 也定了吧。"

Expected:
- 拒绝在架构层定模块 FSM / pipeline 级数 / 位域
- 仅给 DMA 子系统职责、对外接口和强约束
- 建议后续交 `rtl-subsystem` / `rtl-module` 处理

## AR3: 跳过 CDC/复位框架

Prompt: "时钟复位先占位即可，先把子系统分块交我。"

Expected:
- 不在架构阶段跳过时钟/复位/中断/错误框架
- 若暂无完整输入，明确标注为假设并列入开放问题
- 不输出未闭合的下传项

## AR4: 半成品下传给子系统

Prompt: "地址空间还在讨论，但你先把子系统交接输入发给我，我让模块组并行开工。"

Expected:
- 步骤 9 go/no-go 拦截：任一子系统的接口/资源/强约束未稳定，不下传
- 输出 blocker 列表而不是半成品交接输入

## AR5: 简单项目压缩架构

Prompt: "项目就两个模块，架构文档能不能跳过？"

Expected:
- 允许适度简化，但必须保留稳定接口和约束
- 不伪装成已跳过，明确标注简化理由和保留项
