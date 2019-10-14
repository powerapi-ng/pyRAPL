# PyRAPL

[![License: MIT](https://img.shields.io/pypi/l/pyRAPL)](https://spdx.org/licenses/MIT.html)
[![Build Status](https://img.shields.io/circleci/project/github/powerapi-ng/powerapi.svg)](https://circleci.com/gh/powerapi-ng/powerapi)


# About
pyRAPL is a toolkit that measures the energy consumption of a machine during the execution of a python code.

pyRAPL uses the intel "Running Average Power Limit" (RAPL) technology that estimate power consumption of internal devices. This technology is only available on Intel CPU with Sandy Bridge architecture or higher.

pyRAPL can measure the energy consumption of the following devices :

 - CPU socket package 
 - RAM (only on Xeon CPU architecture)

# Installation

You can install pyRAPL with pip : `pip install pyRAPL`

# Basic usage

Here are some basic usages of pyRAPL. Please understand that the measured energy consumption is not only the energy consumption of the code you are running. It's the **global energy consumption** of all the process running on the machine during this period. This includes also the operating system and other applications.
That's why we recommend eliminating any extra programs that may alter the energy consumption of the machine where we run the experiments and keep **only** the code we want to measure its energy consumption (no extra applications such as graphical interface, background running task ...). This will give the closest measure to the real energy consumption of the measured code.

## Decorate a function to measure its energy consumption

To measure the energy consumed by the machine during the execution of the function `fun()` run the following code :

	import pyRAPL

	pyRAPL.setup() 

	@pyRAPL.measure
	def fun():
		# Some stuff ...

	fun()

This will print the recorded energy consumption of all the monitorable devices of the machine during the execution of function `fun`.

## Configure the decorator specifying the device to monitor

You can easly specify which device and which socket to monitor using the parameters of the `pyRAPL.setup` function. 
For example, here, we only monitor the CPU power consumption on the socket `1`.
By default, **pyRAPL** monitors all the available devices of the machine's sockets.

	import pyRAPL

	pyRAPL.setup(devices=[pyRAPL.Device.PKG], socket_ids=[1])

	@pyRAPL.measure
	def fun():
		# Some stuff ...

	fun()	

You can append the device `pyRAPL.Device.DRAM` to the `devices` parameter list to monitor RAM device too. 

## Configure the output of the decorator

If you want to handle data with different output than the standard one, you can configure the decorator with an `Output` instance from the `pyRAPL.outputs` module.

As an example if you want to write the recorded energy consumption in a csv file :


	import pyRAPL

	pyRAPL.setup()
	
	csv_output = pyRAPL.outputs.CSVOutput('result.csv')
	
	@pyRAPL.measure(output=csv_output)
	def fun():
		# Some stuff ...

	for _ in range(100):
		fun()
		
	csv_output.save() 

This will produce a csv file of 100 lines. Each line containing the energy
consumption recorded during one execution of the function `fun`.
Other predefined Output classes exist to export data to *Mongodb* and *Panda*
dataframe.
You can also create your own Output class (see the
[documentation](https://pyrapl.readthedocs.io/en/latest/Outputs_API.html))

## Measure the energy consumption of a piece of code

To measure the energy consumed by the machine during the execution of a given
piece of code, run the following code :

	import pyRAPL

	pyRAPL.setup()
	measure = pyRAPL.Measurement('toto')
    measure.begin()
	
	# ...
	# Piece of code to measure energy consumption 
    # ...
	
	measure.end()
	
You can get the result of the measures using the property : `measure.result` this will return a [`Result`](https://pyrapl.readthedocs.io/en/latest/API.html#pyRAPL.Result) instance.

You can also use an output to handle this results, for example with the csv output : `measure.export(csv_output)`


# Miscellaneous

## About

PyRAPL is an open-source project developed by the [Spirals research group](https://team.inria.fr/spirals) (University of Lille and Inria) that take part of the [powerapi](http://powerapi.org) project.

The documentation is available [here](https://pyrapl.readthedocs.io/en/latest/).

## Mailing list

You can follow the latest news and asks questions by subscribing to our <a href="mailto:sympa@inria.fr?subject=subscribe powerapi">mailing list</a>.

## Contributing

If you would like to contribute code you can do so through GitHub by forking the repository and sending a pull request.

When submitting code, please make every effort to follow existing conventions and style in order to keep the code as readable as possible.
