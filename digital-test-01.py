
import nidaqmx
import time
from nidaqmx.constants import (
    LineGrouping,
    RegenerationMode
)

chs = []

sr = 2
dsig = [0b00, 0b01, 0b10, 0b11, 0b00]

with nidaqmx.Task() as atask, nidaqmx.Task() as dtask:
    atask.ao_channels.add_ao_voltage_chan(
        'Dev4/ao0',
    )
    dtask.do_channels.add_do_chan(
        'Dev4/port0',
        line_grouping=LineGrouping.CHAN_FOR_ALL_LINES
    )

    atask.timing.cfg_samp_clk_timing(rate=sr, source='OnboardClock', samps_per_chan=9)
    dtask.timing.cfg_samp_clk_timing(rate=sr, source='OnboardClock', samps_per_chan=9)
    atask.out_stream.output_buf_size = 5 * 2
    dtask.out_stream.output_buf_size = 5 * 2
    atask.out_stream.regen_mode = RegenerationMode.DONT_ALLOW_REGENERATION
    dtask.out_stream.regen_mode = RegenerationMode.DONT_ALLOW_REGENERATION

    # trigger dtask as soon as atask starts
    atask.triggers.start_trigger.cfg_dig_edge_start_trig(dtask.triggers.start_trigger.term)

    for i in range(1, 5):
        print('1 Channel N Lines N Samples Unsigned Integer Write: ')
        atask.write([-i, -i], auto_start=False)
        dtask.write([dsig[i], dsig[i]], auto_start=False)
        if i == 0:
            atask.start()
            dtask.start()
    atask.write([0])
    dtask.write([0])
    atask.wait_until_done()
    dtask.wait_until_done()
    atask.stop()
    dtask.stop()