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
