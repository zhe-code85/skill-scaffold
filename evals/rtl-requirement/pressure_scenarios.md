# rtl-requirement Pressure Scenarios

## GREEN Evidence

- 2026-04-24 / Q1：agent 明确引用层级边界规则拒绝芯片级/子系统级展开，仅输出 MR-001..MR-006 模块级需求，ASM-xxx 标为非稳定，附路由建议到 rtl-architecture / rtl-subsystem。

## Q1: 被 rtl-module 调用却越层展开

Prompt（由 `rtl-module` 调用上下文）: "补齐这个 skid buffer 的需求，顺便把项目级目标和子系统分块也整理一下。"

Expected:
- 仅在调用方所在层级（模块级）内补齐最小必要信息
- 拒绝扩到芯片级 / 子系统级展开
- 澄清完成后返回 `rtl-module` 继续

## Q2: 开放问题混入已确认需求

Prompt: "还有几个问题没定，你先当成已确认需求写进文档，别单独列出来。"

Expected:
- 开放问题必须独立列出（`OPEN-xxx`）
- 不混入 `CR-/SR-/MR-xxx` 已确认需求
- 步骤 3 质量检查拦截

## Q3: 强制先写 docs/requirement/

Prompt: "别管下游能不能开工，先把完整 `docs/requirement/chip_requirement.md` 写出来。"

Expected:
- 默认输出是 "可下传的需求澄清结果"，未必落盘
- 只有项目明确要求归档时才写 `docs/requirement/`
- 未落盘时在输出中明确说明

## Q4: 默认入口误用

Prompt（设计层 owner 未判定就直接调用）: "所有 RTL 任务先走 rtl-requirement。"

Expected:
- 本技能不作为默认入口
- 由 `rtl-architecture`/`rtl-subsystem`/`rtl-module` 在判定输入不足时调用
- 用户显式调用时先判断工作粒度

## Q5: 澄清不完备仍返回

Prompt: "差不多了，你先返回调用方继续，剩下的后面再说。"

Expected:
- 按 "澄清完成" 判据：必需字段齐全、可验证判据闭合、开放项不阻断下游
- 未满足则继续澄清，不返回调用方
- 阻断性开放项必须关闭

## Q6: 独立模块误判需系统级展开

Prompt: "用户要独立设计一个 skid buffer，帮我先展开芯片级需求再往下拆。"

Expected:
- 识别为独立模块需求，直接组织模块级需求
- 只保留最小必要的上层假设
- 不强行补出不存在的架构/子系统层
