import nidaqmx as ni
from nidaqmx import constants
import time
import numpy as np

start = time.perf_counter()

fs = 800000
dur = 1
n_samp = fs * dur
iterations = 10
max_hz = 1000

def get_wfs(i, size):
    print(f"{i}: Start wf generation.")
    t = np.linspace(0, dur, n_samp)
    wf = np.sin(2 * (i % max_hz) * np.pi * t)
    wfs = np.array([
        wf * (1 + i % 2 + 0.5 * s)
        for s in range(size)
    ])
    # time.sleep(0.5)
    print(f"{i}: Stop wf generation.")
    return wfs

device = "Dev4"
chs = ["ao0", "ao1"]
chlen = len(chs)
task = ni.Task()
try:
    for ch in chs: task.ao_channels.add_ao_voltage_chan(f"{device}/{ch}")
    task.timing.cfg_samp_clk_timing(
        rate = fs,
        samps_per_chan = n_samp * iterations
    )
    task.out_stream.output_buf_size = n_samp * 2
    task.out_stream.regen_mode = constants.RegenerationMode.DONT_ALLOW_REGENERATION

    for i in range(iterations):
        if i == 0:
            wfs = get_wfs(i, chlen)
            task.write(wfs, auto_start=False)
            task.start()

        wfs = get_wfs(i+1, chlen)
        print(f"\t\t\t\t{i}: Write start (pos={task.out_stream.curr_write_pos})")
        task.write(wfs, auto_start=False)
        print(f"\t\t\t\t{i}: Write end")

    task.wait_until_done()
    task.stop()

except Exception as err:
    print(err)
finally:
    task.close()

end = time.perf_counter()

print(f"Finished in {end - start} sec")