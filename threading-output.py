import nidaqmx as ni
from nidaqmx import stream_writers, constants
import concurrent.futures
import time
import numpy as np

start = time.perf_counter()

fs = 800000
dur = 2
n_samp = fs * dur
iterations = 10
max_hz = 1000

def get_wf(i):
    print(f"{i}: Start wf generation.")
    time.sleep(0.5)
    print(f"{i}: Stop wf generation.")
    t = np.linspace(0, dur, n_samp)
    return np.sin(2 * (i % max_hz) * np.pi * t) * (i % 2 + 1)

task = ni.Task()
try:
    task.ao_channels.add_ao_voltage_chan("Dev4/ao0")
    task.timing.cfg_samp_clk_timing(
        rate=fs,
        samps_per_chan=n_samp * iterations
    )

    task.out_stream.output_buf_size = n_samp * 2
    task.out_stream.wait_mode = constants.WaitMode.YIELD
    task.out_stream.regen_mode = constants.RegenerationMode.DONT_ALLOW_REGENERATION
    print(task.out_stream.output_buf_size)

    for i in range(iterations):
        if i == 0:
            wf = get_wf(i)
            task.write(wf, auto_start=False)
            task.start()

        wf = get_wf(i+1)

        print(f"{i}: Write start", task.out_stream.curr_write_pos)
        task.write(wf, auto_start=False)
        print(f"{i}: Write end")

    task.wait_until_done()
    task.stop()



except Exception as err:
    print(err)
finally:
    task.close()

end = time.perf_counter()

print(f"Finished in {end - start} sec")