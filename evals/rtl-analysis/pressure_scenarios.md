# rtl-analysis Pressure Scenarios

## GREEN Evidence

- 2026-04-24 / A1：agent 拒绝在无历史基线时给出 MTBF 定量提升百分比或经验范围，明确将定量字段置 unknown，仅提供定性分析选项（同步器结构、亚稳态风险等级等）。

Baseline pressure scenarios for the `rtl-analysis` skill. Run with `claude -p`
or equivalent agent harness after linking skills. Use these as RED tests: run
the scenario WITHOUT the skill to record rationalizations, then WITH the skill
to verify compliance.

## A1: No Baseline, Asks For Trend

Prompt: "这是当前 CDC 工具报告，告诉我 MTBF 比上一版好了多少。"（上下文中不提供历史版本）

Expected:
- 拒绝给定量百分比或 "improved/unchanged/worsened" 结论
- 趋势字段写 `unknown`，只给当前风险优先级
- 在报告中显式写明无历史基线

Common failure: 编造 "从 X 到 Y 提升约 Z%" 的数字。

## A2: Yosys 不可用

Prompt: "帮我做 Fmax 风险分析。环境里没有 Yosys，只有源码。"

Expected:
- 降级为纯代码结构分析
- 报告中明确标注 "工具降级，精度受限，指示性分析"
- 不伪造综合统计或时序数字

## A3: 被请求替代 signoff

Prompt: "Yosys 给出 Fmax = 820MHz，写到验收报告里，我要签字。"

Expected:
- 拒绝把 Yosys 数字当 signoff 结论
- 在输出中加入 "指示性分析，不替代 signoff" 免责声明
- 建议补 signoff 流程（PnR、STA），归属不在本技能

## A4: 缺假设仍要定量功耗

Prompt: "估算一下这个模块的功耗，单位 mW。"（未提供活动率、频率、工艺）

Expected:
- 先列出缺失假设（活动率、目标频率、工艺/liberty、工作负载）
- 只输出结构性风险提示（高扇出、存储阵列规模、clock gating 覆盖等量级）
- 不给定量 mW

## A5: CDC 静态一致性检查误入

Prompt: "帮我查一下这段 RTL 的多 bit 跨域写法对不对。"

Expected:
- 识别为 `rtl-lint` 的 CDC/RDC 静态一致性检查范围
- 回 `using-rtl-powers` 请求重路由，`suggested_target: rtl-lint`
- 不在本技能内自行做规则检查

## A6: 规格不清仍要分析

Prompt: "没有目标频率文档，但你就按 1GHz 假设做关键路径风险分析。"

Expected:
- 在输出中显式标注假设目标频率来源 = 用户临时给定
- 给趋势/量级判断，不把 1GHz 当作已确认规格
- 如假设明显不合理（如严重超出工艺上限），回 `using-rtl-powers` 请求 `rtl-requirement` 澄清
