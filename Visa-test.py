import pyvisa
import time

rm = pyvisa.ResourceManager()
resource_list = rm.list_resources()
inst = rm.open_resource(resource_list[0])
inst.write(":OUTPut1:STATe ON")

voltages = [0, 5, 10, 15, 18]
for voltage in voltages:
    print(f"Setting voltage to {voltage}")
    inst.write(f":SOURce1:VOLTage:LEVel:IMMediate:AMPLitude {voltage}.VPP")
    time.sleep(1)
    inst.write(f"*TRG")
    time.sleep(1)

inst.write(f":SOURce1:VOLTage:LEVel:IMMediate:AMPLitude 0VPP")
inst.write(":OUTPut1:STATe OFF")