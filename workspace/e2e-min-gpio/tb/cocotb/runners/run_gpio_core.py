import os
from pathlib import Path
import shutil
import sys
import xml.etree.ElementTree as ET

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

existing_pythonpath = os.environ.get("PYTHONPATH", "")
os.environ["PYTHONPATH"] = (
    f"{TESTS_DIR}{os.pathsep}{existing_pythonpath}"
    if existing_pythonpath
    else str(TESTS_DIR)
)
os.environ["GPIO_CORE_TRACE_FILE"] = str(TRACE_FILE)
if str(TESTS_DIR) not in sys.path:
    sys.path.insert(0, str(TESTS_DIR))

runner = get_runner(SIM)

sources = [
    HDL_DIR / "gpio_core_cocotb_top.v",
    PROJECT_ROOT / "rtl" / "modules" / "gpio_core" / "gpio_core.v",
]

build_kwargs = {
    "sources": sources,
    "hdl_toplevel": "gpio_core_cocotb_top",
    "build_dir": BUILD_DIR,
    "always": True,
    "log_file": OUT_DIR / "logs" / "compile.log",
}

test_kwargs = {
    "test_module": "test_gpio_core_smoke",
    "testcase": CASE_NAME,
    "hdl_toplevel": "gpio_core_cocotb_top",
    "build_dir": BUILD_DIR,
    "results_xml": str(RESULTS_XML),
    "seed": SEED,
    "plusargs": [f"WAVE={WAVE_FILE}"],
    "extra_env": {
        "GPIO_CORE_TRACE_FILE": str(TRACE_FILE),
        "PYTHONPATH": os.environ["PYTHONPATH"],
    },
    "log_file": OUT_DIR / "logs" / "cocotb.log",
}

if SIM == "verilator":
    build_kwargs["build_args"] = ["--trace-fst", "-Wno-fatal", "+define+SIM_VERILATOR"]
    build_kwargs["waves"] = True
    test_kwargs["waves"] = True
    test_kwargs["test_args"] = ["--trace-file", str(WAVE_FILE)]
elif SIM == "vcs":
    os.environ["PATH"] = f"/tools/synopsys/vcs/O-2018.09-SP2/bin:{os.environ['PATH']}"
    os.environ["VCS_HOME"] = "/tools/synopsys/vcs/O-2018.09-SP2"
    os.environ["VCS_MX_HOME"] = "/tools/synopsys/vcs/O-2018.09-SP2"
    build_kwargs["build_args"] = ["+define+SIM_VCS"]
else:
    raise SystemExit(f"Unsupported SIM={SIM}")

runner.build(**build_kwargs)
runner.test(**test_kwargs)


def _normalize_results_xml(path: Path) -> None:
    tree = ET.parse(path)
    root = tree.getroot()
    suites = [root] if root.tag == "testsuite" else list(root.findall("testsuite"))

    for suite in suites:
        testcases = list(suite.findall("testcase"))
        tests = len(testcases)
        failures = 0
        errors = 0
        skipped = 0
        for testcase in testcases:
            if testcase.find("failure") is not None:
                failures += 1
            if testcase.find("error") is not None:
                errors += 1
            if testcase.find("skipped") is not None:
                skipped += 1
        suite.set("tests", str(tests))
        suite.set("failures", str(failures))
        suite.set("errors", str(errors))
        suite.set("skipped", str(skipped))

    tree.write(path, encoding="unicode")


_normalize_results_xml(RESULTS_XML)


def _ensure_wave_path() -> None:
    if WAVE_FILE.exists():
        return

    fallback = None
    if SIM == "verilator":
        fallback = BUILD_DIR / "gpio_core.fst"
    elif SIM == "vcs":
        fallback = BUILD_DIR / "gpio_core.vpd"

    if fallback is not None and fallback.exists():
        WAVE_FILE.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(fallback, WAVE_FILE)


_ensure_wave_path()
