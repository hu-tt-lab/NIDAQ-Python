import csv
from datetime import datetime
import os
import pyvisa
import numpy as np
import nidaqmx as ni
from nidaqmx.constants import TaskMode
import matplotlib.pyplot as plt
import time

def query_devices():
    local_system = ni.system.System.local()
    driver_version = local_system.driver_version

    print('DAQmx {0}.{1}.{2}'.format(driver_version.major_version, driver_version.minor_version,
                                    driver_version.update_version))

    for device in local_system.devices:
        print('Device Name: {0}, Product Category: {1}, Product Type: {2}'.format(
            device.name, device.product_category, device.product_type))


def playrec(
    outdata, sr=40000, input_mapping=['Dev1/ai2'],
    output_mapping=['Dev1/ao2']
):
    nsamples = outdata.shape[0]
    with ni.Task() as read_task, ni.Task() as write_task:
        for o in output_mapping:
            aochan = write_task.ao_channels.add_ao_voltage_chan(o)
            aochan.ao_max = 3.5   # output range of USB-4431
            aochan.ao_min = -3.5
        for i in input_mapping:
            aichan = read_task.ai_channels.add_ai_voltage_chan(i)
            aichan.ai_min = -10
            aichan.ai_max = 10

        for task in (read_task, write_task):
            task.timing.cfg_samp_clk_timing(rate=sr, source='OnboardClock', samps_per_chan=nsamples)
        
        write_task.triggers.start_trigger.cfg_dig_edge_start_trig(read_task.triggers.start_trigger.term)
        write_task.write(outdata, auto_start=False)
        write_task.start()
        indata = read_task.read(nsamples)
        
    return indata

def save_csv(t, data: dict[str, np.ndarray]):
    now = datetime.now()
    savefolder = os.path.join("data", now.strftime("%Y%m%d"))
    if not os.path.exists("data"): os.mkdir("data")
    if not os.path.exists(savefolder): os.mkdir(savefolder)
    savepath = os.path.join(savefolder, "voltage_" + now.strftime("%H-%M-%S-%f") + ".csv")

    datakeys = list(data.keys())
    headers = ["time"] + datakeys


    with open(savepath, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(headers)
        for idx, time in enumerate(t):
            row = [time] + [data[key][idx] for key in datakeys]
            writer.writerow(row)

if __name__ == "__main__":
    query_devices()

    sr = 500 * 10**3 # Hz
    duration = 0.01 # sec
    trig_timing = 0.001 # sec
    trig_duration = 0.005 # sec
    trig_voltage = 3 # V

    samples = int(sr * duration)
    trig_rise = int(sr * trig_timing)
    trig_fall = int(sr * (trig_timing + trig_duration))

    t = np.linspace(0, duration, samples, endpoint=False)
    sig = np.zeros(samples)
    sig[trig_rise: trig_fall] = trig_voltage


    rm = pyvisa.ResourceManager()
    resource_list = rm.list_resources()
    inst = rm.open_resource(resource_list[0])
    inst.write(f":OUTPut1:STATe ON")

    voltages = np.arange(0, 6.5, 0.5)
    all_data = {int(v * 10): [] for v in voltages}

    itr = 10
    for itr_i in range(itr):
        itr_data = {}
        for voltage in voltages:
            inst.write(f":SOURce1:VOLTage:LEVel:IMMediate:AMPLitude {voltage}VPP")
            outvoltage = int(voltage * 10)
            indata = playrec(
                sig, 
                sr=40000,
                input_mapping=['Dev1/ai0'],
                output_mapping=['Dev1/ao0']
            )
            itr_data[outvoltage] = indata
            all_data[outvoltage] += [indata]

            time.sleep(0.2)
        # Save to csv
        save_csv(t, itr_data)
        time.sleep(2)
        
    inst.write(f":SOURce1:VOLTage:LEVel:IMMediate:AMPLitude 0VPP")
    inst.write(f":OUTPut1:STATe OFF")

    all_data = {key: np.stack(val) for key, val in all_data.items()}

    # Plot data
    cw = int(sr / 100)
    cw_half = int(cw / 2)

    plt.subplot(211)
    plt.plot(t, sig)
    plt.title("Input Signal")
    plt.xlabel("time (s)")
    plt.ylabel("Voltage (V)")
    plt.subplot(212)
    for voltage, indata in all_data.items():
        # plt.plot(t, indata)
        plt.plot(t, indata.mean(axis=0), label=voltage)
    plt.title("Recorded Signal")
    plt.legend(ncol=7, bbox_to_anchor=(0.5, -0.6), loc="upper center")
    plt.xlabel("time (s)")
    plt.ylabel("voltage (V)")
    plt.tight_layout()
    plt.show()