import nidaqmx
import matplotlib.pyplot as plt

plt.ion()

fs = 1000
ps = 1 / fs # Sample period
dur = 1 # sec
ns = int(fs * dur) # Amount of samples
i = 0

with nidaqmx.Task() as task:
    task.ai_channels.add_ai_thrmcpl_chan("Dev4/ai0")
    while i < ns:
        data = task.read(number_of_samples_per_channel=1)
        if i % 100 == 0:
            # plt.scatter(i, data, color="k")
            print(i, data)
        # plt.pause(ps)
        i = i + 1