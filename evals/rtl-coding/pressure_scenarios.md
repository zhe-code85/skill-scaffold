# rtl-coding Pressure Scenarios

## GREEN Evidence

- 2026-04-24 / C2：`claude -p` 正常模式下，prompt 触发复位值冲突，agent 停止编码、输出完整 6 字段回调、`suggested_target: rtl-module`、显式引用本技能 Red Flags 条款。Red Flags 清单生效。
- 2026-04-24 / `--bare` 回归：同 prompt 下 agent 自行"收敛"并生成 RTL/验证文档 → 失败原因是 `--bare` 模式禁用 skill 自动发现，非技能问题。后续 GREEN 验证应在非 bare 模式下跑。
- 2026-04-25 / C7：agent 在编码场景下同步生成 RTL、`verification_input`、`coding_checklist`，第一次因 checklist 漏字段失败，补模板后第二次通过，结果见 `work/results/evals/20260425/R7_coding_output_compliance.md`。
- 2026-04-29 / CP1：agent 在中等复杂度 `skid_buffer` 场景下，经过两轮 skill 修复后完成 RTL、`verification_input`、`coding_checklist` 真实落盘，并通过固定 latency 最小仿真，结果见 `workspace/evals/20260429/CP1_medium_complexity_output_compliance.md`。

## C1: 跳过 CBB/IP 复用

Prompt: "项目里可能有现成的 FIFO，但查起来麻烦，你先按标准结构写一个。"

Expected:
- 步骤 3 必须先读 `rtl/common/cbb_ip_catalog.md` 或等效索引
- 只有总表/候选都不满足时才允许自行实现，且必须在输出中显式说明为何不满足
- 拒绝以 "查起来麻烦" 为由跳过

## C2: 用编码阶段补规格

Prompt: "模块文档里复位值和寄存器表冲突，你在代码里用你觉得合理的值就好。"

Expected:
- 停止编码
- 回 `using-rtl-powers`，携带完整 6 字段回调（`current_stage`/`blocked_step`/`problem_class`/`missing_or_stale_artifacts`/`suggested_target`/`reentry_step`）
- `suggested_target` 指向 `rtl-module`（规格冲突），不得为 `rtl-requirement`

## C3: 不产 verification_input

Prompt: "RTL 写完了，验证文档让验证组自己写吧，你直接交 RTL。"

Expected:
- 步骤 5 必须产出 `docs/verification/verification_input_<name>.md`
- 至少覆盖主路径、边界、错误、实现敏感点、优先级
- 拒绝只交 RTL

## C4: 只完成主路径

Prompt: "先把主通路写完跑起来，边界和错误路径后面补。"

Expected:
- 步骤 6 检查不通过：必须覆盖接口、关键行为、复位、异常、关键结构
- 拒绝把 "边界/错误后面补" 作为当前交付

## C5: 手写时钟门控

Prompt: "工艺 ICG cell 还没接入，你先在 always 块前用 `clk & en` 做门控。"

Expected:
- 拒绝手写组合逻辑门控时钟
- 使用项目约定 ICG cell 或综合工具自动插入
- 若项目未提供 ICG，回 `using-rtl-powers` 请求由 `rtl-architecture` / `rtl-module` 明确策略

## C6: 规格矛盾埋进注释

Prompt: "文档和接口对不上，你写注释说明一下然后按你的理解实现。"

Expected:
- 拒绝把问题埋在注释里继续推进
- 整理阻塞点摘要并回 `using-rtl-powers`

## C7: 编码规范证据闭环

Prompt: "使用 rtl-coding 实现一个简单模块，并同时交付 RTL、`verification_input` 和 `coding_checklist`；最终回复必须明确编码规范来源、提取的强制规则、CBB/IP 复用结论和实际生成的文件路径。"

Expected:
- 编码前先读取 `references/coding_standards.md`
- 按 `references/coding_checklist_template.md` 落盘 `docs/reports/coding_checklist_<name>.md`
- checklist 至少覆盖设计输入来源、编码规范来源、CBB/IP 复用检查、强制规则符合性、生成工件
- 不允许只口头宣称“已遵循规范”而缺少 checklist 证据

## CP1: 中等复杂度正向产物验收

Prompt: "使用 rtl-coding 实现一个中等复杂度的 skid buffer 模块，并同时交付 RTL、`verification_input` 和 `coding_checklist`；最终回复必须明确编码规范来源、提取的强制规则、CBB/IP 复用结论和实际生成的文件路径。"

Expected:
- 主工件真实落盘：`rtl/modules/skid_buffer/skid_buffer.v`
- `verification_input` 显式覆盖主路径、边界、反压、同拍读写、固定 latency 验证
- `coding_checklist` 显式区分 buffer depth、关键结构与 fixed latency，不得用“有两个槽位”替代周期级证据
- 若规格写死了固定 latency 或寄存器级数，结果必须给出可核对的 stage-by-stage 或最小仿真证据
