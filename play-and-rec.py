import numpy as np
import nidaqmx as ni
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

if __name__ == "__main__":
    query_devices()

    sr = 40000
    duration = 1
    t = np.linspace(0, duration, sr*duration, endpoint=False)
    sig = 1 * np.sin(1*2*np.pi*t)

    indata = playrec(sig)
    plt.plot(t, indata)
    plt.plot(t, sig)
    plt.show()