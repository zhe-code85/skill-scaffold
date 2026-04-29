# RTL Routing Pressure Scenarios

These scenarios cover behavior that must remain stable when editing the RTL skill set.
Run them with `claude -p` or an equivalent agent harness after linking the skills.

## RED Baseline Before 2026-04-24 Edits

Mechanical checks on the current working tree showed these failures:

- Direct cross-skill wording exists: `rg '(^|[ ->，])转 `rtl-|回到 `using-rtl-powers`，转|回 `using-rtl-powers`.*转|直接跳转到 `rtl-' skills/*/SKILL.md`
- Execution callback fields are only explicit in `using-rtl-powers/SKILL.md`, not in `execution_preamble.md`.
- `using-rtl-powers/SKILL.md` is 485 words.

## GREEN Evidence After 2026-04-24 Edits

- R5 with `claude -p` routed CDC/RDC static checking to `rtl-lint`.
- R3 initially failed by omitting exact callback fields and suggesting `rtl-requirement`; after tightening `using-rtl-powers`, `execution_preamble.md`, and `feedback_rules.md`, rerun output preserved all 6 fields and suggested `rtl-module`.

## Scenarios

### R1: Ambiguous RTL Request

Prompt: "我要做一个 DMA 模块，需求还比较粗，帮我推进。"

Expected: enter `using-rtl-powers`, determine current grain, and avoid routing directly to `rtl-requirement`.

### R2: Standalone Module Start

Prompt: "先设计一个独立 valid-ready skid buffer，接口和行为由你整理。"

Expected: route to `rtl-module`; do not force `rtl-architecture` or `rtl-subsystem`.

### R3: Coding Finds Spec Conflict

Prompt: "使用 rtl-coding 实现这个模块，但模块文档里的复位值和寄存器表冲突。"

Expected: stop coding and return a `using-rtl-powers` reroute request with `current_stage`, `blocked_step`, `problem_class`, `missing_or_stale_artifacts`, `suggested_target`, and `reentry_step`.

### R4: Tools Unavailable

Prompt: "用 rtl-lint 检查这个 RTL；如果 Verilator 不在环境里也要给我结果。"

Expected: do not fabricate lint logs; report the unavailable tool path and use the documented fallback.

### R5: CDC/RDC Static Check

Prompt: "检查这段 RTL 的多 bit 跨时钟域写法和复位域混用是否正确。"

Expected: route to `rtl-lint`, not `rtl-analysis`.

### R6: CDC/RDC Report Trend

Prompt: "已有 CDC 工具报告，帮我判断未收敛路径和 MTBF 趋势。"

Expected: route to `rtl-analysis`; if no history or baseline exists, report trend as `unknown`.
