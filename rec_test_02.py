import csv
from datetime import datetime
import os
import numpy as np
import nidaqmx as ni
from nidaqmx.constants import AcquisitionType
from nidaqmx.constants import TaskMode
import matplotlib.pyplot as plt

def query_devices():
    local_system = ni.system.System.local()
    driver_version = local_system.driver_version

    print('DAQmx {0}.{1}.{2}'.format(driver_version.major_version, driver_version.minor_version,
                                    driver_version.update_version))

    for device in local_system.devices:
        print('Device Name: {0}, Product Category: {1}, Product Type: {2}'.format(
            device.name, device.product_category, device.product_type))

rec_wf = False
count = 0
counted = False

def rec(read_duration=1, sr=40000, input_mapping=['Dev4/ai0']
):
    samples = []
    thr = 3.95
    nsamples = int(read_duration * sr)
    print("nsample", nsamples)
    with ni.Task() as read_task:
        for i in input_mapping:
            aichan = read_task.ai_channels.add_ai_voltage_chan(i)
            aichan.ai_min = -10
            aichan.ai_max = 10

        read_task.in_stream.input_buf_size = (nsamples * 2)
        read_task.timing.cfg_samp_clk_timing(rate=sr, sample_mode=AcquisitionType.CONTINUOUS)

        def callback(task_handle, every_n_samples_event_type,
            number_of_samples, callback_data):
            read_samples = read_task.read(number_of_samples_per_channel=nsamples)
            avg = np.average(read_samples).round(2)
            passed = avg < thr
            global count
            global counted
            if not counted and passed:
                count += 1
                counted = True
            elif counted and not passed:
                counted = False
            print(">", count, "turns", "(sensor:", format(avg, ".2f"), "V)",  end="\r")
            if rec_wf: samples.extend(read_samples)
            return 0

        read_task.register_every_n_samples_acquired_into_buffer_event(nsamples, callback)
        read_task.start()
        # indata = read_task.read(nsamples)
        input("Press Enter to Stop.\n\n")
    return np.array(samples)


def playrec(
    outdata, sr=40000, input_mapping=['Dev1/ai0'],
    output_mapping=['Dev1/ao0']
):
    nsamples = outdata.shape[0]
    with ni.Task() as read_task, ni.Task() as write_task:
        for o in output_mapping:
            aochan = write_task.ao_channels.add_ao_voltage_chan(o)
            aochan.ao_max = 3.5   # output range of USB-4431
            aochan.ao_min = -3.5
        for i in input_mapping:
            aichan = read_task.ai_channels.add_ai_thrmcpl_chan(i)
            aichan.ai_min = -10
            aichan.ai_max = 10

        for task in (read_task, write_task):
            task.timing.cfg_samp_clk_timing(rate=sr, source='OnboardClock', samps_per_chan=nsamples)
        
        write_task.triggers.start_trigger.cfg_dig_edge_start_trig(read_task.triggers.start_trigger.term)
        write_task.write(outdata, auto_start=False)
        write_task.start()
        indata = read_task.read(nsamples)
        
    return indata

def save_csv(t, temperature):
    now = datetime.now()
    savefolder = os.path.join("data", now.strftime("%Y%m%d"))
    if not os.path.exists("data"): os.mkdir("data")
    if not os.path.exists(savefolder): os.mkdir(savefolder)
    savepath = os.path.join(savefolder, "temperature_" + now.strftime("%H-%M-%S") + ".csv")

    with open(savepath, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["time", "degC"])
        for time, temp in zip(t, temperature):
            writer.writerow([time, temp])

if __name__ == "__main__":
    query_devices()

    sr = 1000 # Hz
    duration = 0.04 # sec
    samples = int(sr * duration)
    indata = rec(duration, sr, input_mapping=["Dev3/ai0"])

    if rec_wf:
        # Plot data
        cw = int(sr / 10)
        cw_half = int(cw / 2)
        t = np.arange(0, indata.shape[0] / sr, 1/sr)
        plt.plot(t, indata, alpha=0.3, color="k")
        # plt.plot(t[cw_half:-cw_half+1], np.convolve(indata, np.ones(cw)/cw, mode="valid"))
        plt.title("Recorded Signal")
        plt.xlabel("time (s)")
        plt.ylabel("Voltage (V)")
        plt.tight_layout()
        plt.show()