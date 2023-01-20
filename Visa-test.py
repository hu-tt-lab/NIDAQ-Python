import pyvisa

rm = pyvisa.ResourceManager()
resource_list = rm.list_resources()
inst = rm.open_resource(resource_list[0])
inst.write(":SOURce1:VOLTage:LEVel:IMMediate:AMPLitude 2.VPP")
