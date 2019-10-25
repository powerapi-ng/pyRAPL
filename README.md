# PyRAPL

[![License: MIT](https://img.shields.io/pypi/l/pyRAPL)](https://spdx.org/licenses/MIT.html)
[![Build Status](https://img.shields.io/circleci/project/github/powerapi-ng/pyRAPL.svg)](https://circleci.com/gh/powerapi-ng/pyrapl)


# About
pyRAPL is a software toolkit to measure the energy footprint of a host machine along the execution of a piece of Python code.

pyRAPL uses the Intel "_Running Average Power Limit_" (RAPL) technology that estimates power consumption of a CPU.
This technology is available on Intel CPU since the [Sandy Bridge generation](https://fr.wikipedia.org/wiki/Intel#Historique_des_microprocesseurs_produits).

More specifically, pyRAPL can measure the energy consumption of the following CPU domains:
 - CPU socket package 
 - DRAM (for server architectures)
 - GPU (for client architectures)

# Installation

You can install pyRAPL with pip: `pip install pyRAPL`

# Basic usage

Here are some basic usages of pyRAPL. Please note that the reported energy consumption is not only the energy consumption of the code you are running. This includes the **global energy consumption** of all the process running on the machine during this period, thus including the operating system and other applications.
That is why we recommend to eliminate any extra programs that may alter the energy consumption of the machine hosting experiments and to keep **only** the code under measurement (_i.e._, no extra applications, such as graphical interface, background running task...). This will give the closest measure to the real energy consumption of the measured code.

## Decorate a function to measure its energy consumption

To measure the energy consumed by the machine during the execution of the function `fun()` run the following code :

	import pyRAPL

	pyRAPL.setup() 

	@pyRAPL.measure
	def foo():
		# Instructions to be evaluated.

	foo()

This will print in the console the recorded energy consumption of all the monitorable devices of the machine during the execution of function `foo`.

## Configure the decorator specifying the device to monitor

You can easily configure which device and which socket to monitor using the parameters of the `pyRAPL.setup` function. 
For example, the following example only monitors the CPU power consumption on the CPU socket `1`.
By default, **pyRAPL** monitors all the available devices of the CPU sockets.

	import pyRAPL

	pyRAPL.setup(devices=[pyRAPL.Device.PKG], socket_ids=[1])

	@pyRAPL.measure
	def foo():
		# Some stuff ...

	foo()	

You can append the device `pyRAPL.Device.DRAM` to the `devices` parameter list to monitor RAM device too. 

## Running the test multiple times 

For short functions, you can configure the number of runs and it will calculate the mean energy consumption of all runs. 
As an example, if you want to run the evaluation 100 times:

	import pyRAPL

	pyRAPL.setup()
	
	
	@pyRAPL.measure(number=100)
	def fun():
		# Instructions to be evaluated.

	for _ in range(100):
		foo()
	

## Configure the output of the decorator

If you want to handle data with different output than the standard one, you can configure the decorator with an `Output` instance from the `pyRAPL.outputs` module.

As an example, if you want to write the recorded energy consumption in a .csv file:

	import pyRAPL

	pyRAPL.setup()
	
	csv_output = pyRAPL.outputs.CSVOutput('result.csv')
	
	@pyRAPL.measure(output=csv_output)
	def fun():
		# Instructions to be evaluated.

	for _ in range(100):
		fun()
		
	csv_output.save()

This will produce a csv file of 100 lines. Each line containing the energy
consumption recorded during one execution of the function `fun`.
Other predefined `Output` classes exist to export data to *MongoDB* and *Panda*
dataframe.
You can also create your own Output class (see the
[documentation](https://pyrapl.readthedocs.io/en/latest/Outputs_API.html))

## Measure the energy consumption of a piece of code

To measure the energy consumed by the machine during the execution of a given
piece of code, run the following code :

	import pyRAPL

	pyRAPL.setup()
	meter = pyRAPL.Measurement('bar')
	meter.begin()
	# ...
	# Instructions to be evaluated.
	# ...
	meter.end()
	
You can also access the result of the measurements by using the property `meter.result`, which returns a [`Result`](https://pyrapl.readthedocs.io/en/latest/API.html#pyRAPL.Result) object.

You can also use an output to handle this results, for example with the .csv output: `meter.export(csv_output)`

## Measure the energy consumption of a block 

**pyRAPL** allows developers to measure a block of instructions using the keyword  ```with```  as the example below: 

	import pyRAPL
	pyRAPL.setup()
	
	whith pyRAPL.Measurement('bar'):
		# ...
		# Instructions to be evaluated.
		# ...

This will report the energy consumption of the block. To process the measurements instead of printing them, you can use any [`Output`](https://pyrapl.readthedocs.io/en/latest/Outputs_API.html) class that you pass to the `Measurement` object:

	import pyRAPL
	pyRAPL.setup()
	
	dataoutput= pyRAPL.outputs.DataFrameOutput()

	with pyRAPL.Measurement('bar',output=dataoutput):
		# ...
		# Instructions to be evaluated.
    		# ...

	dataoutput.data.head()

# Miscellaneous

## About

**pyRAPL** is an open-source project developed by the [Spirals research group](https://team.inria.fr/spirals) (University of Lille and Inria) that is part of the [powerapi](http://powerapi.org) initiative.

The documentation is available [here](https://pyrapl.readthedocs.io/en/latest/).

## Mailing list

You can follow the latest news and asks questions by subscribing to our <a href="mailto:sympa@inria.fr?subject=subscribe powerapi">mailing list</a>.

## Contributing

If you would like to contribute code, you can do so via GitHub by forking the repository and sending a pull request.

When submitting code, please make every effort to follow existing coding conventions and style in order to keep the code as readable as possible.
