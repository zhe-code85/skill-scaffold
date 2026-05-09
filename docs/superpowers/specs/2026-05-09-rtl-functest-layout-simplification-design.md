# rtl-functest Layout Simplification Design

## Goal

收敛 `rtl-functest` 的运行产物布局和工具入口，解决以下问题：

- 实例目录过深，包含 `run_id` 和 `seed_<n>` 两级目录，用户心智重
- Python 实现脚本在实例目录中以 `*.sh` 软链接暴露，命名与实现错位
- 工具入口散落在每个 case 实例目录，导致目录噪音高
- `PROJECT_ROOT` 与实例目录操作入口混在一起，容易让用户误解“重跑”与“查看波形”的目标对象

本次设计只收敛目录契约、入口命名和重跑语义，不改变：

- case 定义格式
- cocotb 与 sv_tb 的路径判断规则
- `rtl.f` 必须作为实例级事实来源的要求
- `review_pending -> review_pass|fail|blocked` 的人工审核闭环

## Design Decisions

### 1. 去掉 `run_id`

运行目录不再包含批次 ID。每个 case 只保留一份当前/latest 结果。

旧模型：

```text
work/functest/<run_id>/<case>/seed_<seed>/
```

新模型：

```text
work/functest/<case>/
```

这样做的含义是：

- 一个 case 目录只表示该 case 的当前/latest 一次运行
- 同一个 case 再次运行时，默认覆盖旧产物
- 如果用户需要保留历史，应由外部归档或 git/eval 结果文件承担，而不是继续把历史堆在 `work/functest/`

### 2. 去掉 `seed_<n>` 目录

seed 值不再作为目录层级，而是写入 case 目录下的元数据文件。

主记录位置：

- `work/functest/<case>/manifest.json`

`manifest.json` 必须保留：

- `module`
- `case`
- `seed`
- `sim`
- `cmd`
- `runner_status`
- `review_status`
- `status`

### 3. 根层统一工具入口

工具入口统一放在 `work/functest/` 根目录，不再在每个 case 目录下生成入口。

保留的入口名：

```text
work/functest/run_case.py
work/functest/run_cases.py
work/functest/reproduce.py
work/functest/open_wave.py
work/functest/review_case.py
```

这些入口全部使用软链接，目标指向：

```text
skills/rtl-functest/scripts/*.py
```

### 4. 不再生成 `*.sh` 入口

实例目录和根目录中都不再生成：

- `reproduce.sh`
- `open_wave.sh`
- `review_case.sh`

原因：

- 实现本体已经是 Python
- `*.sh -> *.py` 的命名方式制造了错误预期
- 入口已经统一到 `work/functest/` 根目录，继续保留 `*.sh` 没有必要

### 5. case 目录只保留产物

`work/functest/<case>/` 只保留产物与元数据：

```text
work/functest/<case>/
  manifest.json
  results.xml
  rtl.f
  cmd.txt
  env.txt
  logs/
  build/
  waves/
  review/
```

不再放工具入口软链接。

## Command Semantics

### `run_case.py`

标准调用：

```text
work/functest/run_case.py <module> <case> [seed]
```

语义：

- 运行指定 case
- seed 显式传入时，使用该 seed
- seed 未显式传入时，沿用 case 定义中的 `default_seed`
- 若 `work/functest/<case>/` 已存在，则先清空目录中的旧产物，再写入本次运行结果

### `run_case.py --rerun`

重跑调用：

```text
work/functest/run_case.py --rerun <module> <case>
```

语义：

- 读取 `work/functest/<case>/manifest.json`
- 复用旧的 `seed`、`sim` 以及关键运行参数
- 在同一个 case 目录中直接重跑
- 若 `manifest.json` 不存在或关键字段缺失，则返回错误，不做猜测

`--rerun` 是唯一允许“复用旧参数”的路径。普通 `run_case.py` 不读取旧 manifest，避免用户误以为显式运行与重跑是同一动作。

### `run_cases.py`

批量调用仍由：

```text
work/functest/run_cases.py <module> <case-list-or-suite>
```

负责，但输出也落到新的 case 目录模型中。

因为每个 case 只保留 latest 结果，批量运行同一个 case 时会直接更新该 case 目录，不再保留历史 batch 维度。

### `open_wave.py`

使用方式应改成从根层工具入口定位 case：

```text
work/functest/open_wave.py <case>
```

行为：

- 读取 `work/functest/<case>/manifest.json`
- 优先打开 `manifest.json` 中记录的 `waveform.path`
- 若 viewer override 存在，则优先使用 override

### `reproduce.py`

使用方式：

```text
work/functest/reproduce.py <case>
```

行为：

- 读取 `work/functest/<case>/manifest.json`
- 复用原始运行参数
- 本质等价于 `run_case.py --rerun`

### `review_case.py`

使用方式：

```text
work/functest/review_case.py <case> <pass|fail|blocked>
```

行为：

- 定位到 `work/functest/<case>/manifest.json`
- 更新该 case 的 `review_status` 与总状态
- 保留人工审核字段校验

## PROJECT_ROOT Rule

`PROJECT_ROOT` 仍然是包含 `rtl/` 与 `tb/` 的工程根，用于：

- 发现 RTL
- 调用 runner
- 生成 `rtl.f`

但用户与工具的交互入口收敛到 `work/functest/` 根层后，重跑/开波形/收口审核不再依赖用户在实例目录中执行脚本。

实现上应优先：

- 由根层入口显式传递 `PROJECT_ROOT`
- 避免让用户依赖当前 cwd 的隐式根目录猜测

## Migration Plan

### Skill 文档

需要同步修改：

- `skills/rtl-functest/SKILL.md`
- `skills/rtl-functest/references/run_templates.md`

把以下内容统一替换：

- `work/functest/<run_id>/<case>/seed_<seed>/` -> `work/functest/<case>/`
- `reproduce.sh` / `open_wave.sh` / `review_case.sh` -> 根层 `reproduce.py` / `open_wave.py` / `review_case.py`

### 脚本

需要修改：

- `skills/rtl-functest/scripts/functestlib.py`
- 可能涉及 `run_case.py`、`run_cases.py`、`reproduce_case.py`、`open_wave.py`、`review_case.py`

关键改动：

- 去掉 `run_id` 目录逻辑
- 去掉 `seed_<n>` 目录逻辑
- 根层生成 `*.py` 软链接
- 删除实例目录中的 `*.sh` 软链接生成
- 新增 `--rerun` 行为
- 普通运行遇到已存在 case 目录时执行“先清空再运行”

### Fixture / Eval

需要同步更新：

- `workspace/evals/20260508/functest_real_gpio/`
- `workspace/evals/20260509/functest_real_gpio_claude_live/`
- 已引用旧路径的结果文件

## Risks

### 1. 历史 traceability 下降

旧模型天然保留每轮运行历史；新模型只保留 latest。

这是有意识的取舍。该风险由以下方式接受：

- skill 行为证据继续落在 `workspace/evals/<date>/` 结果文件
- 若需要保留历史实例，用户应在运行前自行归档 `work/functest/<case>/`

### 2. 批量运行覆盖旧结果

`run_cases.py` 重跑同一 case 时会覆盖旧目录。这与“只保留 latest”模型一致，不单独引入 batch 历史层。

### 3. 旧脚本调用路径失效

依赖 `./open_wave.sh`、`./reproduce.sh`、`./review_case.sh` 的旧文档和旧习惯会失效，必须同步更新 skill 文案、模板和 eval fixture。

## Verification Plan

修改完成后，至少验证：

1. 单 case 运行：
   - 产物落在 `work/functest/<case>/`
   - `manifest.json` 正确记录 `seed`
2. `--rerun`：
   - 能复用旧 manifest 中的 `seed` / `sim`
3. 根层工具入口：
   - `open_wave.py <case>`
   - `reproduce.py <case>`
   - `review_case.py <case> pass`
4. 行为实测：
   - `claude -p` 仍能在真实 fixture 上跑通
   - 新路径与新入口被正确引用
