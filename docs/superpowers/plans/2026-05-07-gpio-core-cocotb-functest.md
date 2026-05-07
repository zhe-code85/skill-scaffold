# GPIO Core Cocotb Functest Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Add a real cocotb-driven `rtl-functest` path for `workspace/e2e-min-gpio` while keeping the existing `sv_tb` smoke path intact, and verify real `SIM=verilator` plus attempted `SIM=vcs` runs through the standard runner contract.

**Architecture:** Keep the existing `tb/cocotb/runners/run_case.sh` symlinked skill entrypoint, then add a project-local `Makefile_gpio_core` and `run_gpio_core.py` so `run_case.sh` resolves to `runner_kind=cocotb_make`. Use a thin HDL wrapper to expose DUT ports for cocotb and to own simulator-specific wave dumping. Use the cocotb 2.0 `cocotb_tools.runner.get_runner(...)` API from the project-local venv Python, with `set-verilator` sourced before all Verilator runs.

**Tech Stack:** cocotb 2.0.1, cocotb_tools runner API, Verilator 5.046, Synopsys VCS, bash runner glue, Verilog-2001 wrapper HDL.

---

### Task 1: Lock the Red Baseline

**Files:**
- Create: `scripts/tests/test-gpio-core-cocotb-functest`
- Test: `bash scripts/tests/test-gpio-core-cocotb-functest`

- [ ] **Step 1: Write the failing regression script**

```bash
#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "$0")/../.." && pwd)"
PROJECT_ROOT="$ROOT_DIR/workspace/e2e-min-gpio"
RUN_ID="test_gpio_core_cocotb_verilator_$$"
INSTANCE_DIR="$PROJECT_ROOT/work/functest/$RUN_ID/case_main_path/seed_1"
MANIFEST="$INSTANCE_DIR/manifest.json"

read_manifest_field() {
    local manifest="$1"
    local field="$2"
    python3 - "$manifest" "$field" <<'PY'
import json
import sys

with open(sys.argv[1], encoding="utf-8") as f:
    data = json.load(f)

value = data
for part in sys.argv[2].split("."):
    value = value[part]
print(value)
PY
}

bash -lc '
    set -euo pipefail
    cd "'"$ROOT_DIR"'"
    . ./set-verilator
    cd "'"$PROJECT_ROOT"'"
    RUN_ID="'"$RUN_ID"'" SIM=verilator tb/cocotb/runners/run_case.sh gpio_core case_main_path 1
'

if [ ! -f "$MANIFEST" ]; then
    echo "missing manifest: $MANIFEST" >&2
    exit 1
fi

if [ "$(read_manifest_field "$MANIFEST" sim)" != "verilator" ]; then
    echo "expected SIM=verilator manifest" >&2
    exit 1
fi

if [ "$(read_manifest_field "$MANIFEST" runner_kind)" != "cocotb_make" ]; then
    echo "expected runner_kind=cocotb_make" >&2
    exit 1
fi

if [ "$(read_manifest_field "$MANIFEST" status)" != "review_pending" ]; then
    echo "expected status=review_pending" >&2
    exit 1
fi

wave_path="$(read_manifest_field "$MANIFEST" waveform.path)"
if [ -z "$wave_path" ] || [ ! -f "$wave_path" ]; then
    echo "expected waveform file recorded in manifest" >&2
    exit 1
fi
```

- [ ] **Step 2: Run the regression and verify it fails for the right reason**

Run:

```bash
bash scripts/tests/test-gpio-core-cocotb-functest
```

Expected: FAIL. The current project should not satisfy `runner_kind=cocotb_make`; it should either fall back to `svtb_make` or fail before a project-local cocotb Makefile exists.

- [ ] **Step 3: Commit the red test**

```bash
git add scripts/tests/test-gpio-core-cocotb-functest
git commit -m "test: add red gpio core cocotb functest regression"
```

### Task 2: Add the Cocotb HDL Wrapper and Python Test

**Files:**
- Create: `workspace/e2e-min-gpio/tb/cocotb/hdl/gpio_core_cocotb_top.v`
- Create: `workspace/e2e-min-gpio/tb/cocotb/tests/test_gpio_core_smoke.py`
- Test: `bash scripts/tests/test-gpio-core-cocotb-functest`

- [ ] **Step 1: Write the HDL wrapper that owns wave dumping**

```verilog
`timescale 1ns/1ps

module gpio_core_cocotb_top;
    reg  [7:0] data_out;
    reg  [7:0] dir;
    reg  [7:0] gpio_in;
    wire [7:0] gpio_out;
    wire [7:0] gpio_oe;
    wire [7:0] data_in;

    string wave_file;

    gpio_core dut (
        .data_out(data_out),
        .dir(dir),
        .gpio_in(gpio_in),
        .gpio_out(gpio_out),
        .gpio_oe(gpio_oe),
        .data_in(data_in)
    );

    initial begin
`ifdef SIM_VCS
        if (!$value$plusargs("WAVE=%s", wave_file)) begin
            wave_file = "gpio_core.vpd";
        end
        $vcdplusfile(wave_file);
        $vcdpluson(0, gpio_core_cocotb_top);
`elsif SIM_VERILATOR
        if (!$value$plusargs("WAVE=%s", wave_file)) begin
            wave_file = "gpio_core.fst";
        end
        $dumpfile(wave_file);
        $dumpvars(0, gpio_core_cocotb_top);
`endif
    end
endmodule
```

- [ ] **Step 2: Write the cocotb smoke testcase**

```python
import os
from pathlib import Path

import cocotb
from cocotb.triggers import Timer
from cocotb.utils import get_sim_time


TRACE_ENV = "GPIO_CORE_TRACE_FILE"


def _u8(signal) -> int:
    return int(signal.value) & 0xFF


def _trace_path() -> Path:
    path = Path(os.environ[TRACE_ENV])
    path.parent.mkdir(parents=True, exist_ok=True)
    return path


def _write_trace(line: str) -> None:
    with _trace_path().open("a", encoding="utf-8") as trace:
        trace.write(line + "\n")


def _log_state(dut, label: str) -> None:
    line = (
        f"TRACE {int(get_sim_time(unit='ps'))} {label} "
        f"data_out={_u8(dut.data_out):02x} "
        f"dir={_u8(dut.dir):02x} "
        f"gpio_in={_u8(dut.gpio_in):02x} "
        f"gpio_out={_u8(dut.gpio_out):02x} "
        f"gpio_oe={_u8(dut.gpio_oe):02x} "
        f"data_in={_u8(dut.data_in):02x}"
    )
    cocotb.log.info(line)
    _write_trace(line)


def _check_eq(label: str, actual: int, expected: int) -> None:
    assert actual == expected, f"{label}: actual={actual:02x} expected={expected:02x}"


@cocotb.test()
async def case_main_path(dut) -> None:
    trace_path = _trace_path()
    trace_path.write_text("", encoding="utf-8")

    dut.data_out.value = 0x00
    dut.dir.value = 0x00
    dut.gpio_in.value = 0x00
    await Timer(1, unit="ns")
    _log_state(dut, "baseline")
    _check_eq("baseline_gpio_out", _u8(dut.gpio_out), 0x00)
    _check_eq("baseline_gpio_oe", _u8(dut.gpio_oe), 0x00)
    _check_eq("baseline_data_in", _u8(dut.data_in), 0x00)

    dut.data_out.value = 0xA5
    dut.dir.value = 0xFF
    dut.gpio_in.value = 0x3C
    await Timer(1, unit="ns")
    _log_state(dut, "main_path")
    _check_eq("main_path_gpio_out", _u8(dut.gpio_out), 0xA5)
    _check_eq("main_path_gpio_oe", _u8(dut.gpio_oe), 0xFF)
    _check_eq("main_path_data_in", _u8(dut.data_in), 0x3C)

    dut.dir.value = 0x96
    await Timer(1, unit="ns")
    _log_state(dut, "dir_update")
    _check_eq("dir_update_gpio_oe", _u8(dut.gpio_oe), 0x96)
    _check_eq("dir_update_data_in", _u8(dut.data_in), 0x3C)

    dut.gpio_in.value = 0xC3
    await Timer(1, unit="ns")
    _log_state(dut, "input_update")
    _check_eq("input_update_gpio_out", _u8(dut.gpio_out), 0xA5)
    _check_eq("input_update_gpio_oe", _u8(dut.gpio_oe), 0x96)
    _check_eq("input_update_data_in", _u8(dut.data_in), 0xC3)

    cocotb.log.info("PASS case=case_main_path")
    _write_trace("PASS case=case_main_path")
```

- [ ] **Step 3: Run the red regression again and confirm it still fails**

Run:

```bash
bash scripts/tests/test-gpio-core-cocotb-functest
```

Expected: FAIL again, now because the project still lacks the cocotb project runner (`tb/cocotb/runners/Makefile_gpio_core`), not because the testcase assets are missing.

- [ ] **Step 4: Commit the wrapper and testcase**

```bash
git add \
  workspace/e2e-min-gpio/tb/cocotb/hdl/gpio_core_cocotb_top.v \
  workspace/e2e-min-gpio/tb/cocotb/tests/test_gpio_core_smoke.py
git commit -m "test: add gpio core cocotb smoke testcase"
```

### Task 3: Add the Cocotb Project Runner and Make Verilator Pass

**Files:**
- Create: `workspace/e2e-min-gpio/tb/cocotb/runners/run_gpio_core.py`
- Create: `workspace/e2e-min-gpio/tb/cocotb/runners/Makefile_gpio_core`
- Modify: `workspace/e2e-min-gpio/cases/smoke/case_main_path.md`
- Test: `bash scripts/tests/test-gpio-core-cocotb-functest`

- [ ] **Step 1: Write the Python runner that binds cocotb 2.0 to the project layout**

```python
import os
from pathlib import Path

from cocotb_tools.runner import get_runner


PROJECT_ROOT = Path(os.environ["PROJECT_ROOT"]).resolve()
OUT_DIR = Path(os.environ["OUT"]).resolve()
BUILD_DIR = Path(os.environ["SIM_BUILD"]).resolve()
RESULTS_XML = Path(os.environ["COCOTB_RESULTS_FILE"]).resolve()
WAVES_DIR = Path(os.environ["WAVES_DIR"]).resolve()
CASE_NAME = os.environ["CASE"]
SEED = os.environ["SEED"]
SIM = os.environ["SIM"]

TESTS_DIR = PROJECT_ROOT / "tb" / "cocotb" / "tests"
HDL_DIR = PROJECT_ROOT / "tb" / "cocotb" / "hdl"
TRACE_FILE = OUT_DIR / "review" / f"{CASE_NAME}_trace.log"
WAVE_FILE = WAVES_DIR / (f"{CASE_NAME}.fst" if SIM == "verilator" else f"{CASE_NAME}.vpd")

if SIM == "verilator":
    build_args = ["--trace-fst", "-Wno-fatal", "+define+SIM_VERILATOR"]
    test_args = ["--trace", "--trace-file", str(WAVE_FILE)]
elif SIM == "vcs":
    os.environ["PATH"] = f"/tools/synopsys/vcs/O-2018.09-SP2/bin:{os.environ['PATH']}"
    os.environ["VCS_HOME"] = "/tools/synopsys/vcs/O-2018.09-SP2"
    os.environ["VCS_MX_HOME"] = "/tools/synopsys/vcs/O-2018.09-SP2"
    build_args = ["+define+SIM_VCS"]
    test_args = []
else:
    raise SystemExit(f"Unsupported SIM={SIM}")

runner = get_runner(SIM)
runner.build(
    sources=[
        HDL_DIR / "gpio_core_cocotb_top.v",
        PROJECT_ROOT / "rtl" / "modules" / "gpio_core" / "gpio_core.v",
    ],
    hdl_toplevel="gpio_core_cocotb_top",
    build_dir=BUILD_DIR,
    always=True,
    build_args=build_args,
    log_file=OUT_DIR / "logs" / "compile.log",
)

existing_pythonpath = os.environ.get("PYTHONPATH", "")
extra_env = {
    "GPIO_CORE_TRACE_FILE": str(TRACE_FILE),
    "PYTHONPATH": (
        f"{TESTS_DIR}{os.pathsep}{existing_pythonpath}"
        if existing_pythonpath
        else str(TESTS_DIR)
    ),
}

runner.test(
    test_module="test_gpio_core_smoke",
    testcase=CASE_NAME,
    hdl_toplevel="gpio_core_cocotb_top",
    build_dir=BUILD_DIR,
    results_xml=str(RESULTS_XML),
    seed=SEED,
    plusargs=[f"WAVE={WAVE_FILE}"],
    test_args=test_args,
    extra_env=extra_env,
    log_file=OUT_DIR / "logs" / "cocotb.log",
)
```

- [ ] **Step 2: Write the project-local cocotb Makefile**

```make
SHELL := /bin/bash

PROJECT_ROOT := $(abspath $(CURDIR)/../../..)
REPO_ROOT := $(abspath $(PROJECT_ROOT)/../..)
PYTHON_BIN ?= /home/yanzhe/workspace/cocotb-setup/.venv/bin/python
RUNNER_PY := $(PROJECT_ROOT)/tb/cocotb/runners/run_gpio_core.py

CASE ?= case_main_path
SEED ?= 1
OUT ?= $(PROJECT_ROOT)/work/functest/manual
SIM_BUILD ?= $(OUT)/build
WAVES_DIR ?= $(OUT)/waves
COCOTB_RESULTS_FILE ?= $(OUT)/results.xml

.PHONY: all

all:
	@mkdir -p "$(OUT)/logs" "$(OUT)/review" "$(SIM_BUILD)" "$(WAVES_DIR)"
	@set -euo pipefail; \
	if [ "$(SIM)" = "verilator" ]; then \
		. "$(REPO_ROOT)/set-verilator"; \
	fi; \
	PROJECT_ROOT="$(PROJECT_ROOT)" \
	OUT="$(OUT)" \
	SIM_BUILD="$(SIM_BUILD)" \
	COCOTB_RESULTS_FILE="$(COCOTB_RESULTS_FILE)" \
	WAVES_DIR="$(WAVES_DIR)" \
	CASE="$(CASE)" \
	SEED="$(SEED)" \
	SIM="$(SIM)" \
	"$(PYTHON_BIN)" "$(RUNNER_PY)"
```

- [ ] **Step 3: Update the stable case definition to mention the cocotb path**

```markdown
# case_main_path

- `case_name`: `case_main_path`
- `module`: `gpio_core`
- `intent`: 以单个 smoke case 覆盖 `verification_input_gpio_core.md` 的主功能通路和 `data_in` 与 `dir` 无耦合这一实现敏感点。
- `source_requirements`: `F1`、`F2`、`F3`、`F4`、`B4`、`S2`
- `test_impl`:
  - `tb/sv_tb/tests/test_gpio_core_smoke.v` 中 `case_main_path`
  - `tb/cocotb/tests/test_gpio_core_smoke.py` 中 `case_main_path`，顶层 wrapper 为 `tb/cocotb/hdl/gpio_core_cocotb_top.v`
- `default_seed`: `1`
- `wave_review_points`:
  - baseline 阶段 `data_out=00 dir=00 gpio_in=00` 时，`gpio_out/gpio_oe/data_in` 都为 `00`
  - main_path 阶段 `data_out=A5 dir=FF gpio_in=3C` 时，三路输出分别稳定为 `A5/FF/3C`
  - dir_update 阶段仅更新 `dir=96`，`gpio_oe` 跟随到 `96`，`data_in` 继续保持 `3C`
  - input_update 阶段仅更新 `gpio_in=C3`，`data_in` 跟随到 `C3`，`gpio_out/gpio_oe` 保持 `A5/96`
```

- [ ] **Step 4: Re-run the regression and verify Verilator now passes through `cocotb_make`**

Run:

```bash
bash scripts/tests/test-gpio-core-cocotb-functest
```

Expected: PASS. The manifest at `workspace/e2e-min-gpio/work/functest/test_gpio_core_cocotb_verilator_*/case_main_path/seed_1/manifest.json` should report:

```text
sim=verilator
runner_kind=cocotb_make
runner_status=pass
status=review_pending
waveform.format=FST
```

- [ ] **Step 5: Commit the cocotb runner path**

```bash
git add \
  workspace/e2e-min-gpio/tb/cocotb/runners/run_gpio_core.py \
  workspace/e2e-min-gpio/tb/cocotb/runners/Makefile_gpio_core \
  workspace/e2e-min-gpio/cases/smoke/case_main_path.md
git commit -m "test: add gpio core cocotb functest runner"
```

### Task 4: Run Real Functest Instances and Close the Wave Review Loop

**Files:**
- Modify: `workspace/e2e-min-gpio/work/functest/gpio_core_cocotb_verilator_20260507/case_main_path/seed_1/review/wave_review.md`
- Modify: `workspace/e2e-min-gpio/work/functest/gpio_core_cocotb_vcs_20260507/case_main_path/seed_1/review/wave_review.md`
- Test: real `run_case.sh` invocations for `SIM=verilator` and `SIM=vcs`

- [ ] **Step 1: Run a fresh real Verilator cocotb functest instance**

Run:

```bash
bash -lc '
    set -euo pipefail
    cd /home/yanzhe/workspace/skill-rtl
    . ./set-verilator
    cd workspace/e2e-min-gpio
    RUN_ID=gpio_core_cocotb_verilator_20260507 SIM=verilator \
      tb/cocotb/runners/run_case.sh gpio_core case_main_path 1
'
```

Expected: exit `0`, with `manifest.json` reporting `runner_kind=cocotb_make`, `runner_status=pass`, `status=review_pending`, and a real `waves/case_main_path.fst`.

- [ ] **Step 2: Perform the manual wave review close-out for the Verilator run**

Write this file in the instance directory:

```markdown
# Wave Review

verdict: pass
summary: baseline, main path, dir update, and input update all match the gpio_core straight-through contract
issue_class: none
checked_points:
- baseline stage keeps gpio_out gpio_oe data_in at 00
- main_path stage drives A5 FF 3C through the three datapaths
- dir_update only changes gpio_oe while data_in remains 3C
- input_update only changes data_in while gpio_out gpio_oe remain A5 96
```

Then run:

```bash
cd /home/yanzhe/workspace/skill-rtl/workspace/e2e-min-gpio/work/functest/gpio_core_cocotb_verilator_20260507/case_main_path/seed_1
./review_case.sh pass
```

Expected: `manifest.json` status becomes `review_pass`, and the run root `summary.csv` refreshes to `review_pass`.

- [ ] **Step 3: Attempt a real VCS cocotb functest instance**

Run:

```bash
cd /home/yanzhe/workspace/skill-rtl/workspace/e2e-min-gpio
RUN_ID=gpio_core_cocotb_vcs_20260507 SIM=vcs \
  tb/cocotb/runners/run_case.sh gpio_core case_main_path 1
```

Expected: one of these two outcomes is acceptable:

```text
Outcome A:
  runner_kind=cocotb_make
  runner_status=pass
  status=review_pending
  waveform.format=VPD

Outcome B:
  runner_kind=cocotb_make
  status=result_failed
  review_status=blocked
  logs/compile.log shows a real cocotb + VCS compile/elab attempt
```

The unacceptable outcome is falling back to `runner_kind=svtb_make`.

- [ ] **Step 4: If VCS passes, close the wave review; if it fails, preserve the blocked evidence**

Pass path:

```bash
cd /home/yanzhe/workspace/skill-rtl/workspace/e2e-min-gpio/work/functest/gpio_core_cocotb_vcs_20260507/case_main_path/seed_1
./open_wave.sh
cat > review/wave_review.md <<'EOF'
# Wave Review

verdict: pass
summary: vcs cocotb path matches the gpio_core straight-through contract in all four review stages
issue_class: none
checked_points:
- baseline stage keeps gpio_out gpio_oe data_in at 00
- main_path stage drives A5 FF 3C through the three datapaths
- dir_update only changes gpio_oe while data_in remains 3C
- input_update only changes data_in while gpio_out gpio_oe remain A5 96
EOF
./review_case.sh pass
```

Blocked path:

```bash
python3 - <<'PY'
import json
from pathlib import Path

manifest = Path("/home/yanzhe/workspace/skill-rtl/workspace/e2e-min-gpio/work/functest/gpio_core_cocotb_vcs_20260507/case_main_path/seed_1/manifest.json")
data = json.loads(manifest.read_text(encoding="utf-8"))
assert data["runner_kind"] == "cocotb_make"
assert data["status"] == "result_failed"
assert data["review_status"] == "blocked"
print("vcs blocked evidence preserved")
PY
```

- [ ] **Step 5: Commit the finished implementation**

```bash
git add \
  workspace/e2e-min-gpio/tb/cocotb \
  workspace/e2e-min-gpio/cases/smoke/case_main_path.md \
  scripts/tests/test-gpio-core-cocotb-functest
git commit -m "test: add gpio core cocotb functest path"
```
