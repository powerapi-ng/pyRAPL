# PyRAPL
[![License: MIT](https://img.shields.io/pypi/l/pyRAPL)](https://spdx.org/licenses/MIT.html)
[![Build Status](https://img.shields.io/circleci/project/github/powerapi-ng/powerapi.svg)](https://circleci.com/gh/powerapi-ng/powerapi)


# About
pyRAPL is a toolkit that measure the power consumption of a machine during the
execution of a python piece of code.

pyRAPL use the intel "Running Average Power Limit" (RAPL) technology that estimate
global power consumption of a machine. This technology is only available on
Intel CPU with Sandy Bridge architecture or higher.

pyRAPL can measure the power consumption of the following devices :
 - pyRAPL.Device.PKG : CPU socket package 
 - pyRAPL.Device.DRAM : DRAM (only on server CPU)

# Installation

You can install pyRAPL with pip : `pip install pyRAPL`

# Basic usage

Here is some basic usage of pyRAPL. Please understand that the measured energy
consumption is not only the energy consumption of the piece of code you are
measuring. Its the **global energy consumption** of all the process running on your machine. Including the operating system and other running applications.

If you are using **pyRAPL** for research about software energy consumption, please run your experiments on a machine where **only** the code you want to measure the energy consumption is running  (no extra apllications such as graphical interface, background runing task ...).
This will give
you the closest measure to the real energy consumption of your piece of code.

## Decorate a function to measure its power consumption

To measure the energy consumed by the machine during the execution of the
function `fun()` run the following code :

	import pyRAPL

	@pyRAPL.measure
	def fun():
		# Some stuff ...

	fun()

## Customise the decorator by adding a handler  or specifying which devices you want to monitor 


	import pyRAPL

	def my_handler(measure):
		print('function name : ' + measure.function_name)
		print('socket power consumption (in J) : ' + str(measure.data['PKG']))
		print('dram power consumption (in J) : ' + str(measure.data['DRAM']))

	@pyRAPL.measure(devices=[pyRAPL.Device.PKG, pyRAPL.Device.DRAM], handler=my_handler)
	def fun():
		# Some stuff ...

	fun()

## Measure the power consumption of a piece of code

To measure the energy consumed by the machine during the execution of the given
piece of code, run the following code :

	import pyRAPL

	sensor = pyRAPL.PyRAPL()
	sensor.record(pyRAPL.Device.PKG, pyRAPL.Device.DRAM)
	
	# Some Stuff ...
	
	sensor.stop()

	data = sensor.recorded_energy()
	print('socket power consumption (in J) : ' + str(data[pyRAPL.Device.PKG]))
	print('dram power consumption (in J) : ' + str(data[pyRAPL.Device.DRAM]))
