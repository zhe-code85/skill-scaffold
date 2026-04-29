# RTL Eval Manifest

本文件是 `evals/` 的场景注册表，用于把 scenario ID、所属 suite 和当前证据来源对齐。

证据状态说明：

- `result-file`：有独立结果文件落盘在 `workspace/evals/` 或 legacy `work/results/evals/`
- `indirect-result`：通过其他 suite 的结果文件间接覆盖
- `inline-evidence`：仅在对应 `pressure_scenarios.md` 的 `GREEN Evidence` 中记录
- `missing`：尚未发现可追溯证据

## rtl-analysis

| ID | 标题 | 证据状态 | 当前证据 |
| --- | --- | --- | --- |
| A1 | No Baseline, Asks For Trend | `inline-evidence` | `evals/rtl-analysis/pressure_scenarios.md` |
| A2 | Yosys 不可用 | `missing` | 无 |
| A3 | 被请求替代 signoff | `missing` | 无 |
| A4 | 缺假设仍要定量功耗 | `missing` | 无 |
| A5 | CDC 静态一致性检查误入 | `indirect-result` | `work/results/evals/20260424/R5_cdc_static_check.md` |
| A6 | 规格不清仍要分析 | `missing` | 无 |

## rtl-architecture

| ID | 标题 | 证据状态 | 当前证据 |
| --- | --- | --- | --- |
| AR1 | 需求不稳定仍要求出架构文档 | `result-file` | `work/results/evals/20260425/AR1_unstable_requirement.md` |
| AR2 | 越层做模块微架构 | `result-file` | `work/results/evals/20260425/AR2_no_module_microarch.md` |
| AR3 | 跳过 CDC/复位框架 | `result-file` | `work/results/evals/20260425/AR3_clock_reset_not_skipped.md` |
| AR4 | 半成品下传给子系统 | `result-file` | `work/results/evals/20260425/AR4_no_half_baked_handoff.md` |
| AR5 | 简单项目压缩架构 | `result-file` | `work/results/evals/20260425/AR5_simplified_architecture.md` |

## rtl-coding

| ID | 标题 | 证据状态 | 当前证据 |
| --- | --- | --- | --- |
| C1 | 跳过 CBB/IP 复用 | `result-file` | `workspace/evals/20260429/C1_must_check_cbb_reuse.md` |
| C2 | 用编码阶段补规格 | `indirect-result` | `work/results/evals/20260424/R3_coding_spec_conflict.md` |
| C3 | 不产 verification_input | `result-file` | `workspace/evals/20260429/C3_must_produce_verification_input.md` |
| C4 | 只完成主路径 | `result-file` | `workspace/evals/20260429/C4_no_main_path_only.md` |
| C5 | 手写时钟门控 | `result-file` | `workspace/evals/20260429/C5_no_comb_clock_gating.md` |
| C6 | 规格矛盾埋进注释 | `result-file` | `workspace/evals/20260429/C6_no_comment_masking.md` |
| C7 | 编码规范证据闭环 | `result-file` | `workspace/evals/20260429/C7_coding_output_compliance_live.md` |
| CP1 | 中等复杂度正向产物验收 | `result-file` | `workspace/evals/20260429/CP1_medium_complexity_output_compliance.md` |

## rtl-functest

| ID | 标题 | 证据状态 | 当前证据 |
| --- | --- | --- | --- |
| F1 | 工具全部不可用 | `inline-evidence` | `evals/rtl-functest/pressure_scenarios.md` |
| F2 | 绕过 cocotb 优先级 | `missing` | 无 |
| F3 | 不读 verification_input | `missing` | 无 |
| F4 | 膨胀成正式验证 | `missing` | 无 |
| F5 | 忽略波形压缩策略 | `missing` | 无 |

## rtl-lint

| ID | 标题 | 证据状态 | 当前证据 |
| --- | --- | --- | --- |
| L1 | Verilator 不在环境 | `indirect-result` | `work/results/evals/20260424/R4_tool_unavailable.md` |
| L2 | 合法 SV 当风格问题 | `result-file` | `work/results/evals/20260425/L2_sv_dialect_style.md` |
| L3 | CDC/RDC 被误路由给分析 | `indirect-result` | `work/results/evals/20260424/R5_cdc_static_check.md` + `work/results/evals/20260424/R6_cdc_report_analysis.md` |
| L4 | 无模块文档仍做规格一致性 | `result-file` | `work/results/evals/20260425/L4_missing_module_doc.md` |
| L5 | 越层改规格 | `result-file` | `work/results/evals/20260425/L5_spec_feedback.md` |

## rtl-module

| ID | 标题 | 证据状态 | 当前证据 |
| --- | --- | --- | --- |
| M1 | 只写主路径 | `result-file` | `workspace/evals/20260429/M1_no_main_path_only.md` |
| M2 | 开放问题伪装为稳定输入 | `result-file` | `workspace/evals/20260429/M2_tbd_must_block_coding.md` |
| M3 | 越位定 RTL 结构 | `result-file` | `workspace/evals/20260429/M3_no_over_spec_impl.md` |
| M4 | 子系统依赖未闭合 | `result-file` | `workspace/evals/20260429/M4_block_on_unclosed_subsystem.md` |
| M5 | 独立小模块快速路径 | `result-file` | `workspace/evals/20260429/M5_skid_buffer_output_compliance.md` |
| M6 | 输入不足调用rtl-requirement | `result-file` | `workspace/evals/20260429/M6_requirement_callback_only.md` |

## rtl-requirement

| ID | 标题 | 证据状态 | 当前证据 |
| --- | --- | --- | --- |
| Q1 | 被 rtl-module 调用却越层展开 | `inline-evidence` | `evals/rtl-requirement/pressure_scenarios.md` |
| Q2 | 开放问题混入已确认需求 | `missing` | 无 |
| Q3 | 强制先写 docs/requirement/ | `missing` | 无 |
| Q4 | 默认入口误用 | `missing` | 无 |
| Q5 | 澄清不完备仍返回 | `missing` | 无 |
| Q6 | 独立模块误判需系统级展开 | `missing` | 无 |

## rtl-routing

| ID | 标题 | 证据状态 | 当前证据 |
| --- | --- | --- | --- |
| R1 | Ambiguous RTL Request | `result-file` | `work/results/evals/20260424/R1_ambiguous_request.md` |
| R2 | Standalone Module Start | `result-file` | `work/results/evals/20260424/R2_standalone_module.md` |
| R3 | Coding Finds Spec Conflict | `result-file` | `work/results/evals/20260424/R3_coding_spec_conflict.md` |
| R4 | Tools Unavailable | `result-file` | `work/results/evals/20260424/R4_tool_unavailable.md` |
| R5 | CDC/RDC Static Check | `result-file` | `work/results/evals/20260424/R5_cdc_static_check.md` |
| R6 | CDC/RDC Report Trend | `result-file` | `work/results/evals/20260424/R6_cdc_report_analysis.md` |

## rtl-subsystem

`P1` 是正向交付物验收场景，因此在 `S1`-`S5` 之外有意使用 `P` 前缀。

| ID | 标题 | 证据状态 | 当前证据 |
| --- | --- | --- | --- |
| S1 | 只列模块名 | `result-file` | `workspace/evals/20260429/S1_no_module_name_only.md` |
| S2 | 架构不稳仍细化子系统 | `result-file` | `workspace/evals/20260429/S2_no_subsystem_on_unstable_arch.md` |
| S3 | 下沉到模块内部 FSM | `result-file` | `workspace/evals/20260429/S3_no_module_microarch.md` |
| S4 | 跳过子系统层 | `result-file` | `workspace/evals/20260429/S4_skip_subsystem_only_when_allowed.md` |
| S5 | CDC 标注缺失 | `result-file` | `workspace/evals/20260429/S5_cdc_must_be_closed.md` |
| P1 | 真实生成子系统交付物 | `result-file` | `workspace/evals/20260429/P1_subsystem_output_compliance.md` |

## rtl-verification

| ID | 标题 | 证据状态 | 当前证据 |
| --- | --- | --- | --- |
| V1 | 规格不清仍堆 case | `inline-evidence` | `evals/rtl-verification/pressure_scenarios.md` |
| V2 | 环境不可用伪造回归 | `missing` | 无 |
| V3 | 与 functest 边界混淆 | `missing` | 无 |
| V4 | 跳过功能覆盖模型 | `missing` | 无 |
| V5 | 默认 VCD 波形 | `missing` | 无 |
| V6 | 协议合规性缺失 | `missing` | 无 |
