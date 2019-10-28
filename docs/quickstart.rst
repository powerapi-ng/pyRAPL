Quickstart
**********

Installation
============

You can install **pyRAPL** with pip : ``pip install pyRAPL``

Basic usage
===========

Here are some basic usages of **pyRAPL**. Please note that the reported energy consumption is not only the energy consumption of the code you are running. This includes the *global energy consumption* of all the process running on the machine during this period, thus including the operating system and other applications.
That is why we recommend to eliminate any extra programs that may alter the energy consumption of the machine hosting experiments and to keep only the code under measurement (*i.e.*, no extra applications, such as graphical interface, background running task...). This will give the closest measure to the real energy consumption of the measured code.

Here are some basic usages of pyRAPL. Please understand that the measured energy consumption is not only the energy consumption of the code you are running. It's the **global energy consumption** of all the process running on the machine during this period. This includes also the operating system and other applications.
That's why we recommend eliminating any extra programs that may alter the energy consumption of the machine where we run the experiments and keep **only** the code we want to measure its energy consumption (no extra applications such as graphical interface, background running task ...). This will give the closest measure to the real energy consumption of the measured code.

Decorate a function to measure its energy consumption
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

To measure the energy consumed by the machine during the execution of the
function ``foo()`` run the following code::

  import pyRAPL

  pyRAPL.setup()

  @pyRAPL.measureit
  def foo():
    # Instructions to be evaluated.

  foo()

This will print the recorded energy consumption of all the monitorable devices of the machine during the execution of function ``fun``.

Configure the decorator specifying the device to monitor
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

You can easly configure which device and which socket to monitor using the parameters of the ``pyRAPL.setup`` function. 
For example, the following example only monitors the CPU power consumption on the CPU socket ``1``.
By default, **pyRAPL** monitors all the available devices of the CPU sockets::

  import pyRAPL

  pyRAPL.setup(devices=[pyRAPL.Device.PKG], socket_ids=[1])

  @pyRAPL.measureit
  def foo():
    # Instructions to be evaluated.

  foo()	

You can append the device ``pyRAPL.Device.DRAM`` to the ``devices`` parameter list to monitor RAM device too. 

Running the test multiple times
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

For short functions, you can configure the number of runs and it will calculate the mean energy consumption of all runs. 
As an example if you want to run the evaluation 100 times ::

  import pyRAPL

  pyRAPL.setup()
	
  @pyRAPL.measureit(number=100)
  def foo():
      # Instructions to be evaluated.

  for _ in range(100):
      foo()


Configure the output of the decorator
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

If you want to handle data with different output than the standard one, you can configure the decorator with an ``Output`` instance from the ``pyRAPL.outputs`` module.

As an example if you want to write the recorded energy consumption in a csv file ::

  import pyRAPL

  pyRAPL.setup()
  
  csv_output = pyRAPL.outputs.CSVOutput('result.csv')
  
  @pyRAPL.measureit(output=csv_output)
  def foo():
    # Some stuff ...

  for _ in range(100):
    foo()
  
  csv_output.save()

This will produce a csv file of 100 lines. Each line containing the energy
consumption recorded during one execution of the function `fun`.
Other predefined Output classes exist to export data to *MongoDB* and *Panda*
dataframe. You can also create your own Output class (see the
documentation_)

.. _documentation: https://pyrapl.readthedocs.io/en/latest/Outputs_API.html

Measure the energy consumption of a piece of code
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

To measure the energy consumed by the machine during the execution of a given
piece of code, run the following code::

  import pyRAPL

  pyRAPL.setup()
  measure = pyRAPL.Measurement('bar')
  measure.begin()
  
  # ...
  # Instructions to be evaluated.
  # ...
  
  measure.end()
	
You can also access the result of the measurements using the property : ``measure.result`` which returns a Result_ instance.

.. _Result: https://pyrapl.readthedocs.io/en/latest/API.html#pyRAPL.Result

You can also use an output to handle this results, for example with the csv output : ``measure.export(csv_output)``


Measure the energy consumption of a block
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

**pyRAPL** allows also to measure a block of instructions using the Keyword ``with`` as the example below::


  import pyRAPL 
  pyRAPL.setup()

  with pyRAPL.Measurement('bar'):
    # ...
    # Instructions to be evaluated.
    # ...

	
This will print in the console the energy consumption of the block. 
To handle the measures instead of just printing them you can use any Output_ class that you pass to the Measurement object 

.. _Output: https://pyrapl.readthedocs.io/en/latest/Outputs_API.html

::

  import pyRAPL
  pyRAPL.setup()

  dataoutput= pyRAPL.outputs.DataFrameOutput()  
  with pyRAPL.Measurement('bar',output=dataoutput):
  
    # ...
    # Instructions to be evaluated.
    # ...
  
  dataoutput.data.head()

