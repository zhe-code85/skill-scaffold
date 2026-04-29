# rtl-subsystem Pressure Scenarios

## GREEN Evidence

- 2026-04-29 / S1：见 `workspace/evals/20260429/S1_no_module_name_only.md`
- 2026-04-29 / S2：见 `workspace/evals/20260429/S2_no_subsystem_on_unstable_arch.md`
- 2026-04-29 / S3：见 `workspace/evals/20260429/S3_no_module_microarch.md`
- 2026-04-29 / S4：见 `workspace/evals/20260429/S4_skip_subsystem_only_when_allowed.md`
- 2026-04-29 / S5：见 `workspace/evals/20260429/S5_cdc_must_be_closed.md`
- 2026-04-29 / P1：见 `workspace/evals/20260429/P1_subsystem_output_compliance.md`

## S1: 只列模块名

Prompt: "把子系统拆成 A/B/C 三个模块就行，其他让模块组自己定。"

Expected:
- 拒绝以模块名列表作为输出
- 为每个模块给出稳定边界：职责、输入输出接口、配置/状态接口、依赖关系、强约束、开放问题
- 步骤 7 go/no-go 拦截不完整交接

## S2: 架构不稳仍细化子系统

Prompt: "顶层总线拓扑还在讨论，但你先把这个子系统细化到模块边界。"

Expected:
- 若顶层接口/地址/时钟复位框架必须先由芯片级裁决，停止下传
- 回 `using-rtl-powers`，建议 `rtl-architecture`
- 不伪装依赖全局的子系统为已收敛

## S3: 下沉到模块内部 FSM

Prompt: "子系统文档里顺便把仲裁器的 FSM 也写了吧。"

Expected:
- 只给概要级边界和接口契约
- 拒绝下沉到 FSM / pipeline 级数 / 寄存器位域
- 内部微架构留给 `rtl-module`

## S4: 跳过子系统层

Prompt: "项目只有 2 个模块，子系统层直接跳过。"

Expected:
- 验证 "模块数 ≤ 3 且无 CDC 且无共享资源仲裁" 才允许
- 跳过时显式声明 "本次有意跳过子系统层" 及理由
- 条件不满足时拒绝跳过

## S5: CDC 标注缺失

Prompt: "子系统里有 2 个时钟域，但跨域信号先不标，后面再补。"

Expected:
- 步骤 5 必须标注模块间 CDC 接口（哪些信号跨域、同步机制）
- 不下传未标注 CDC 接口的子系统设计

## P1: 真实生成子系统交付物

Prompt: "顶层接口、地址空间、时钟复位框架都已稳定。请为一个独立子系统完成正式设计交付，输出 `docs/subsystem/subsystem_<name>.md`，覆盖子系统边界与对外接口、模块划分、模块协作关系、数据流、控制流、资源组织、各模块边界定义、假设与风险。每个模块都要写清职责、输入输出接口、配置/状态接口、模块间依赖、必须遵守的强约束、开放问题/假设。"

Expected:
- 生成 `docs/subsystem/subsystem_<name>.md`
- 文档包含：子系统边界与对外接口、模块划分、模块协作关系、数据流、控制流、资源组织、各模块边界定义、假设与风险
- 每个模块都具备六项边界字段：模块职责、输入输出接口、配置/状态接口、模块间依赖、必须遵守的强约束、开放问题/假设
- 模块协作关系、资源组织、数据流/控制流与边界定义相互一致，可直接作为 `rtl-module` 下游输入
- 不以模块名列表替代交付，不下沉到 FSM / pipeline 级数 / 寄存器位域
