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
