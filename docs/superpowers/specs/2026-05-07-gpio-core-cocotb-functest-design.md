# GPIO Core Cocotb Functest Design

## Goal

在 `workspace/e2e-min-gpio` 中保留现有 `sv_tb` smoke 路径，同时新增一条真正由 cocotb 驱动的 `rtl-functest` 自测链路，使 `gpio_core` 可以通过标准 runner 入口分别尝试 `SIM=verilator` 和 `SIM=vcs`，并把波形审核结果按实例目录契约落盘。

## Context

当前 `gpio_core` 已有一条可工作的 `sv_tb` 降级路径：

- `SIM=verilator` 已通过 `tb/sv_tb/runners/Makefile_gpio_core` 跑通
- `SIM=vcs` 仍卡在本机 VCS 链接阶段，尚未产出可审核波形
- 机器上存在可用的 cocotb 安装，但仅位于 `/home/yanzhe/workspace/cocotb-setup/.venv/bin/python`
- 默认 `python` / `python3` 指向的解释器无法导入 cocotb

因此，这次设计的重点不是替换现有 smoke，而是在不破坏当前证据链的前提下，补一条显式绑定 venv 的 cocotb 正常路径。

## Chosen Approach

选择在项目内新增 `tb/cocotb/tests/` 和 `tb/cocotb/runners/Makefile_gpio_core`，并让 `rtl-functest` 现有 `run_case.sh` 直接命中该 Makefile。

这样做的理由：

1. `rtl-functest` 已优先支持 `tb/cocotb/runners/Makefile_<module>`，不需要先改技能脚本契约
2. Makefile 可以显式绑定 cocotb venv 解释器，绕开系统默认 Python 不含 cocotb 的问题
3. 现有 `sv_tb` runner 可完整保留，便于对比 cocotb 路径和旧 smoke 路径的行为一致性

## Alternatives Considered

### A. 直接依赖 `tb/cocotb/tests/*.py` + `pytest`

优点是结构常见；缺点是当前 `run_case.sh` 的 pytest harness 探测与执行默认使用系统 `python3`，而系统 `python3` 无法导入 cocotb。除非先改技能脚本解释器策略，否则这条路会把环境不确定性放大。

### B. 把现有 `sv_tb` 目录直接改造成 cocotb 主路径

优点是路径数量更少；缺点是会把“资产形态是 SV”与“执行链路由 cocotb 驱动”混在一起，弱化对两条路径的可追溯性，也会影响当前已经形成的 `sv_tb` 证据。

### C. 在项目内并行保留 `sv_tb`，新增明确的 cocotb Makefile 路径

这是本次选择。它最符合 `rtl-functest` 的 runner 优先级和可追溯性要求，也最容易在后续结果中清楚区分“旧 smoke”与“cocotb 正路”。

## Scope

### In Scope

- 为 `gpio_core` 新增一条 cocotb 自测路径
- 通过 `rtl-functest` 标准 runner 分别尝试 `SIM=verilator` 和 `SIM=vcs`
- 复用现有 `case_main_path` 语义，保证 cocotb 与现有 smoke 的主路径检查点一致
- 为成功运行的实例执行波形审核和 `review_case.sh` 收口

### Out of Scope

- 不删除或重构现有 `sv_tb` smoke 资产
- 不扩展到 feature/negative/corner 回归矩阵
- 不为 VCS 工具链问题引入仓库级全局环境修复机制
- 不修改 `rtl-functest` 技能契约，除非实测暴露出明确 runner 缺口

## Test Semantics

新的 cocotb case 继续围绕 `case_main_path`，保持与现有 smoke 一致的四个检查阶段：

1. `baseline`
2. `main_path`
3. `dir_update`
4. `input_update`

每个阶段都记录可追溯日志，并检查以下核心行为：

- `gpio_out == data_out`
- `gpio_oe == dir`
- `data_in == gpio_in`
- `data_in` 不受 `dir` 影响

这覆盖 `verification_input_gpio_core.md` 中的 `F1-F4` 和 `B1/B4`，也能延续当前 `sv_tb` 路径的主路径证据。

## File Layout

计划新增或修改的核心文件如下：

- 新增 `workspace/e2e-min-gpio/tb/cocotb/tests/test_gpio_core_smoke.py`
  - 负责 cocotb testcase 和主路径断言
- 新增 `workspace/e2e-min-gpio/tb/cocotb/runners/Makefile_gpio_core`
  - 负责统一调用 cocotb、选择 simulator、输出结果文件和波形
- 如有必要新增 `workspace/e2e-min-gpio/tb/cocotb/runners/run_gpio_core.py`
  - 负责集中封装 simulator 参数，避免 Makefile 过重
- 可能小幅调整 `workspace/e2e-min-gpio/cases/smoke/case_main_path.md`
  - 若需要补充 cocotb 对应的 `test_impl` 描述和波形审核关注点

现有 `tb/sv_tb/...` 文件保持不动，作为并行对照路径保留。

## Runtime Design

### Verilator

- 目标路径：`SIM=verilator tb/cocotb/runners/run_case.sh gpio_core case_main_path 1`
- cocotb 通过显式 venv Python 启动
- 目标波形格式为 `FST`
- 成功后进入人工波形审核，写 `review/wave_review.md` 并执行 `./review_case.sh pass`

### VCS

- 目标路径：`SIM=vcs tb/cocotb/runners/run_case.sh gpio_core case_main_path 1`
- 优先尝试标准 cocotb + VCS 路径
- 目标波形格式优先 `FSDB` 或 `VPD`，以工具链真实产物为准
- 如果继续卡在已有的机器级链接问题，则保留失败实例与日志，状态诚实反映为 `result_failed` / `review_blocked`

本设计不承诺“VCS 必定通过”，只承诺“VCS 会走真正的 cocotb 尝试，并留下合规证据”。

## Cocotb Environment Binding

项目内 cocotb runner 必须显式使用：

```text
/home/yanzhe/workspace/cocotb-setup/.venv/bin/python
```

不能依赖裸 `python` / `python3`，因为当前默认解释器无法导入 cocotb。优先把解释器路径写入项目 Makefile 或本地 runner，而不是修改用户 shell 环境。

## Wave Review Contract

对每个成功生成波形的 cocotb 实例，仍沿用 `rtl-functest` 的标准收口方式：

1. 打开实例目录中的 `open_wave.sh`
2. 依据 `case_main_path` 的 `wave_review_points` 人工检查
3. 记录 `review/wave_review.md`
4. 执行 `./review_case.sh pass|fail|blocked`

如果 viewer 不可用但波形文件存在，结果必须明确记录为环境阻塞，而不是跳过审核后宣称技能级通过。

## Verification Plan

实现后至少验证以下内容：

1. `SIM=verilator` 的 cocotb 路径能通过标准 `run_case.sh` 跑通
2. 产出 `results.xml`、标准实例目录和 `FST` 波形
3. `open_wave.sh` 对 Verilator 实例给出真实 viewer 结果
4. `review_case.sh` 能把成功实例从 `review_pending` 收口到 `review_pass`
5. `SIM=vcs` 会走 cocotb 路径尝试，不会错误落回 `sv_tb`
6. 若 VCS 失败，`manifest.json` 和日志能清楚说明失败发生在 cocotb + VCS 实际尝试过程中

## Risks

### R1. 默认 Python 与 cocotb venv 不一致

风险最大，也最确定。解决策略是项目内显式绑定 cocotb 解释器，避免依赖 PATH。

### R2. VCS 机器级链接问题继续存在

这不是 `gpio_core` 逻辑问题，也不是 cocotb testcase 本身的问题。若复现，应在结果中保留其为环境或工具链阻塞，而不把失败归因到 DUT 行为。

### R3. Cocotb 与现有 `sv_tb` 检查语义漂移

若 cocotb 检查点和现有 smoke 分叉，后续 evidence 会难以比较。解决策略是复用现有四阶段主路径语义，并在日志命名上保持一致。

## Success Criteria

满足以下条件即可认为本次设计完成目标：

- 项目内新增一条清晰、可追踪的 cocotb 自测路径
- `rtl-functest` 能优先命中该 cocotb runner
- `SIM=verilator` 与 `SIM=vcs` 都完成一次真实 cocotb 尝试
- 每次尝试都留下标准实例目录证据
- 对于成功生成波形的实例，人工审核与状态收口完整闭环
