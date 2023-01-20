import csv
from datetime import datetime
import os
import threading
from time import sleep
import numpy as np
import nidaqmx as ni
from nidaqmx.constants import ThermocoupleType 
import matplotlib.pyplot as plt

running = True

def query_devices():
    local_system = ni.system.System.local()
    driver_version = local_system.driver_version

    print('DAQmx {0}.{1}.{2}'.format(driver_version.major_version, driver_version.minor_version,
                                    driver_version.update_version))

    for device in local_system.devices:
        print('Device Name: {0}, Product Category: {1}, Product Type: {2}'.format(
            device.name, device.product_category, device.product_type))

def ask_user():
    global running
    input("Press enter to stop")
    running = False

def play(
    outdata, sr=40000, output_mapping=['Dev1/ao0'], timeout=1800
):
    global running

    thread = threading.Thread(target=ask_user)
    thread.start()

    nsamples = outdata.shape[0]
    with ni.Task() as write_task:
        for o in output_mapping:
            aochan = write_task.ao_channels.add_ao_voltage_chan(o)
            aochan.ao_max = 3.5   # output range of USB-4431
            aochan.ao_min = -3.5

        write_task.timing.cfg_samp_clk_timing(rate=sr, source='OnboardClock', samps_per_chan=nsamples)
        write_task.write(outdata, auto_start=True)
        taskIsDone = False
        i = 0
        time = 0
        while running and not taskIsDone:
            ps = 1/sr
            i += 1
            time += ps
            plt.scatter(time, i, color="k")
            plt.pause(ps)
            # if i >= 6:
                # write_task.stop()
            taskIsDone = write_task.is_task_done()
        # write_task.wait_until_done(timeout=timeout)
        write_task.stop()
        
    return

if __name__ == "__main__":
    query_devices()
    
    # Parameters -----------------
    
    isTbs = False
    
    fms = 10 # Hz
    itrs = fms * 2 + (0 if isTbs else 1)
    trials = 3
    interval = 10 # sec
    
    start = 0 # sec
    
    pms = np.round(1/fms, 8) # sec
    ftbs = 50 # Hz
    ptbs = np.round(1/ftbs, 8) # sec
    
    temp = np.arange(start, start + interval * trials, interval)
    timings = []
    for t in temp:
        temp_timings = list(np.arange(t, t + pms * itrs, pms))
        append_timings = []
        if isTbs:
            for tt in temp_timings:
                append_timings += [
                    tt,
                    tt + ptbs,
                    tt + 2 * ptbs
                ]
        else: append_timings = temp_timings
        timings += append_timings
    timings = np.array(timings)
    
    # Change here!! --------------
    
    device = "Dev2"
    sr = 5000 # Hz
    

    end = np.round(np.max(timings) + 4 , 5)
    duration = end # sec
    trig_timings = timings # sec
    trig_duration = 0.001 # sec
    trig_voltage = 3 # V
    
    # ----------------------------

    trig_duration = max(2/sr, trig_duration)
    samples = int(sr * duration)
    t = np.linspace(0, duration, samples, endpoint=False)

    sig = np.zeros(samples)
    for trig_timing in trig_timings:
        trig_rise = int(sr * trig_timing)
        trig_fall = int(sr * (trig_timing + trig_duration))
        sig[trig_rise: trig_fall] = trig_voltage

    play(sig, sr, [f"{device}/ao1"], timeout=3600)
