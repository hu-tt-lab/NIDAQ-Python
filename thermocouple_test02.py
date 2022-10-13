import nidaqmx
from nidaqmx.constants import AcquisitionType
from nidaqmx import stream_readers
import numpy as np
import csv
import time 
from datetime import datetime

sample_rate = 2 # Hz
aqc_time = 10 # sec


samples_to_acq = int(sample_rate * aqc_time + 1)
cont_mode = AcquisitionType.CONTINUOUS

# Acquire data
with nidaqmx.Task() as task:
    now = datetime.now()
    military = now.strftime("%H:%M:%S")
    first_header = ["Event 1"]
    second_header = [f"T. Captura: {military}"]

    task.ai_channels.add_ai_thrmcpl_chan("Dev1/ai0")

    task.timing.cfg_samp_clk_timing(sample_rate, sample_mode=cont_mode, samps_per_chan=samples_to_acq)

    start = time.time()
    print("Starting task...")
    data = np.ndarray((1, samples_to_acq), dtype=np.float64)
    stream_readers.AnalogMultiChannelReader(task.in_stream).read_many_sample(data, samples_to_acq, timeout=10)

# Save to csv
with open("data.csv", "w", newline="") as f:
    writer = csv.writer(f)
    writer.writerow(first_header)
    writer.writerow(second_header)

    writer.writerow("")

    x = np.linspace(0, aqc_time, samples_to_acq)

    for value in range(len(x)):
        writer.writerow([x[value], data[0][value]])

elapsed_time = (time.time() - start)
print(f"Done in {elapsed_time}")