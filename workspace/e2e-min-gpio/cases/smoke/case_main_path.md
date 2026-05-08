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
