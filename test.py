from typing import Sequence
import nidaqmx.system

system = nidaqmx.system.System.local()
device = system.devices["Dev1"]
phys_chan = device.ai_physical_chans["ai0"]
