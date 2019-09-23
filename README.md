# Basic usage

## Measure the energy consumption during a function execution

To measure the energy consumed during the execution of the function `fun()` run the following code

	import pyRAPL
	
	sensor = pyRAPL.PyRAPL()
	sensor.record([pyRAPL.Device.PKG, pyRAPL.Device.DRAM])
	fun()
	sensor.stop()
	energy_pkg = sensor.recorded_energy(pyRAPL.Device.PKG)
    energy_dram = sensor.recorded_energy(pyRAPL.Device.DRAM)
