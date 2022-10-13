import nidaqmx.system

system = nidaqmx.system.System.local()
for device in system.devices:
    print(device.name, device.product_category.name, device.product_type)
