import nidaqmx as ni
import numpy as np

fs = 40000
ps = 1 / fs
dur = 5
n_samp = dur * fs

freq = 10

t = np.arange(0, 10, ps)
sig = np.sin(2 * np.pi * t * freq)

with ni.Task() as task:
    task.ao_channels.add_ao_voltage_chan("Dev4/ao0")
    task.timing.cfg_samp_clk_timing(
        rate=fs,
        samps_per_chan = n_samp
    )
    task.write(sig, auto_start=False)
    task.start()

    task.wait_until_done()
    task.stop()
    
with ni.Task() as task:
    task.ao_channels.add_ao_voltage_chan("Dev4/ao0")
    task.write([0])