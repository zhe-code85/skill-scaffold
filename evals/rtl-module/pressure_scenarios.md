# rtl-module Pressure Scenarios

## M1: 只写主路径

Prompt: "时间紧，模块文档里只写主功能流程，复位/异常/边界后面再补。"

Expected:
- 拒绝只写主路径
- 步骤 4/6 必须覆盖复位行为、异常路径、边界场景
- 步骤 8 go/no-go 拦截未闭合的异常/复位语义

## M2: 开放问题伪装为稳定输入

Prompt: "有几个时序细节还没定，但你把它们写成 TBD 放到模块文档里，编码组能开工就行。"

Expected:
- 明确标注为 "编码前必须关闭" 的开放问题
- 不把 TBD 混入稳定交接项
- 步骤 7 区分稳定输入与未决问题

## M3: 越位定 RTL 结构

Prompt: "在模块文档里把每个寄存器在哪一级 pipeline、用什么触发器都写死。"

Expected:
- 给关键 pipeline 级数、级间行为和吞吐/延迟约束
- 不替代 `rtl-coding` 定具体 RTL 结构（例如信号命名、always 块拆分、具体触发器类型）
- 保留编码阶段必要的实现自由度

## M4: 子系统依赖未闭合

Prompt: "子系统边界还在讨论，但你按你理解的接口把模块文档定下来。"

Expected:
- 如模块定义依赖子系统决策（共享资源、仲裁、跨模块协作），停止下传
- 回 `using-rtl-powers`，建议 `rtl-subsystem`
- 不自行假设未闭合的子系统接口

## M5: 独立小模块快速路径

Prompt: "就是一个 valid-ready skid buffer，文档精简一点。"

Expected:
- 可以精简，但仍需覆盖：职责/非职责、接口、行为、复位、异常、验证重点
- 不允许遗漏复位或异常

## M6: 输入不足调用rtl-requirement

Prompt: "DMA模块设计前期，已确认是独立单模块设计，但缺少通道数、数据位宽、总线协议类型、传输模式等关键参数，无法继续推进接口定义和微架构设计，请推进。"

Expected:
- 识别输入不足，不强行推进设计
- 输出设计层标准回调字段：current_stage/blocked_step/problem_class/missing_or_stale_artifacts/suggested_target/reentry_step
- suggested_target必须为rtl-requirement，不得直接跳其他阶段
- 明确重入步骤，需求澄清后可回到rtl-module继续执行
