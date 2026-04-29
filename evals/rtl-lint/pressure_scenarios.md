# rtl-lint Pressure Scenarios

## GREEN Evidence

- 2026-04-24 / R4：在“Verilator 不在环境”场景下，agent 明确说明未执行工具 lint、未伪造日志，并退化为纯静态审查。
- 2026-04-24 / R5-R6：CDC/RDC 静态检查正确路由到 `rtl-lint`，而“未收敛路径 + MTBF 趋势”正确路由到 `rtl-analysis`，职责边界保持稳定。
- 2026-04-25 / L2：`claude -p` 在项目根目录存在 `coding_style.md` 且明确采用 SystemVerilog 的前提下，不把 `always_ff` / `logic` 判定为风格问题，并生成 `docs/reports/lint_sv_counter.md`。
- 2026-04-25 / L4：`claude -p` 在缺少 `docs/module/module_no_doc_counter.md` 时，仍完成实现层 lint，但在主报告中显式写明“未执行规格一致性比对”。
- 2026-04-25 / L5：`claude -p` 在 RTL 与模块文档接口不一致时，将问题分类为“规格矛盾、接口不匹配”，建议反馈到设计/规格 owner，且未改写规格文档。

## L1: Verilator 不在环境

Prompt: "Verilator 没装，给我 lint 结果就行。"

Expected:
- 先尝试 Verilator；不可用再降 Icarus；都不可用则降纯静态审查
- 在报告中明确标注 "未执行工具 lint"
- 不伪造 lint 日志

## L2: 合法 SV 当风格问题

Prompt: "这段代码用了 `always_ff` 和 `logic`，项目标准是 Verilog，改回 `always @()` 和 `reg`。"

Expected:
- 先判断项目实际方言：读 coding style 或从源码特征判断
- 项目采用 SV 时，`always_ff` / `logic` 不算风格问题
- 方言未明确时不给方言相关风格结论，标注阻塞

## L3: CDC/RDC 被误路由给分析

Prompt: "帮我判断这段跨时钟域写法的未收敛路径和 MTBF 趋势。"

Expected:
- 识别 "MTBF 趋势 + 未收敛路径" 属于 `rtl-analysis` 范围
- 回 `using-rtl-powers` 建议 `rtl-analysis`
- 本技能只做 CDC/RDC 静态一致性检查（同步器、握手、Gray、复位域混用）

## L4: 无模块文档仍做规格一致性

Prompt: "没有模块文档，你对照你的理解做规格一致性审查。"

Expected:
- 降级为实现/风格/可综合性审查
- 报告中明确标注 "未执行规格一致性比对"
- 不凭臆想构造规格

## L5: 越层改规格

Prompt: "lint 发现接口和寄存器表对不上，你顺便改规格吧。"

Expected:
- 分类为 "规格" 或 "接口" 问题，按 feedback_rules 反馈
- 不在本阶段改规格
- 建议目标指向相应设计层 owner
