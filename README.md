# Basic usage

## Measure the energy consumption during a function execution

To measure the energy consumed during the execution of the function `fun()` run the following code

	import pyRAPL
	
	sensor = pyRAPL.PyRAPL()
	sensor.start_record_energy_pkg()
	fun()
	sensor.stop_record_energy_pkg()
	energy = sensor.get_record_pkg_result()
