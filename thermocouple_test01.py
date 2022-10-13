import nidaqmx
import matplotlib.pyplot as plt

plt.ion()

ps = 0.1 # Sample period
ns = 100 # Amount of samples
i = 0

with nidaqmx.Task() as task:
    task.ao_channels.add_ao_voltage_chan("Dev1/ao0")
    task.write([5,5,0], auto_start=True)

with nidaqmx.Task() as task:
    task.ai_channels.add_ai_thrmcpl_chan("Dev1/ai0")
    while i < ns:
        data = task.read(number_of_samples_per_channel=1)
        plt.scatter(i, data, color="k")
        plt.pause(ps)
        i = i + 1