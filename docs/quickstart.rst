Quickstart
**********

Installation
============

You can install pyRAPL with pip : ``pip install pyRAPL``

Basic usage
===========

Here is some basic usage of pyRAPL. Please understand that the measured energy
consumption is not only the energy consumption of the piece of code you are
running. Its the **global energy consumption** of all the process running on
your machine. Including the operating system and other running applications.

If you are using **pyRAPL** for research about software energy consumption,
please run your experiments on a machine where **only** the code you want to
measure the energy consumption is running (no extra applications such as
graphical interface, background running task ...).  This will give you the
closest measure to the real energy consumption of your piece of code.

Decorate a function to measure its power consumption
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

To measure the energy consumed by the machine during the execution of the
function ``fun()`` run the following code::

  import pyRAPL

  pyRAPL.setup()

  @pyRAPL.measure
  def fun():
    # Some stuff ...

  fun()

This will print the power consumption of all the monitorable devices of your
machine, recorded during the execution of function ``fun``, on the standard output.

Configure the decorator specifying the device to monitor
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

You can specify which device to monitor and which socket to monitor using the
parameter of the ``pyRAPL.setup`` function. For example, here, we only monitor the
CPU power consumption on the socket ``1``. By default, all the devices of the
machine on all the socket are monitored::

  import pyRAPL

  pyRAPL.setup(devices=[pyRAPL.Device.PKG], socket_ids=[1])

  @pyRAPL.measure
  def fun():
    # Some stuff ...

  fun()	

You can append the device ``pyRAPL.Device.DRAM`` to the ``devices`` parameter list to
also monitor RAM device

Configure the output of the decorator
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

If you want to handle data with different output than standard output, you can
configure the decorator with ``Output`` instance from the ``pyRAPL.outputs`` module.

For example if you want to write the recorded power consumption on a csv file::

  import pyRAPL

  pyRAPL.setup()
  
  csv_output = pyRAPL.outputs.CSVOutput('result.csv')
  
  @pyRAPL.measure(output=csv_output)
  def fun():
    # Some stuff ...

  for _ in range(100):
    fun()
  
  csv_output.save()

This will produce a csv file of 100 lines. Each line containing the power
consumption recorded during one execution of the function ``fun``

Predefined Output class exists to export data to Mongodb and Panda
dataframe. You can also create your own Output class (see the
documentation_)

.. _documentation: https://pyrapl.readthedocs.io/en/latest/Outputs_API.html

Measure the power consumption of a piece of code
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

To measure the energy consumed by the machine during the execution of a given
piece of code, run the following code::

  import pyRAPL

  pyRAPL.setup()
  measure = pyRAPL.Measurement('toto')
  measure.begin()
  
  # ...
  # Piece of code to measure power consumption 
  # ...
  
  measure.end()
	
You can get the result of the measure using the property : ``measure.result`` this will return a Result_ instance.

.. _Result: https://pyrapl.readthedocs.io/en/latest/API.html#pyRAPL.Result

You can also use an output to handle this result, for example with the csv output : ``measure.export(csv_output)``
