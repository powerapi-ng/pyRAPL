# MIT License
# Copyright (c) 2019, INRIA
# Copyright (c) 2019, University of Lille
# All rights reserved.
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
import functools

from time import time_ns
from pyRAPL import Result
from pyRAPL.outputs import PrintOutput, Output
import pyRAPL


def empty_energy_result(energy_result):
    """
    Return False if the energy_result list contains only negative numbers, True otherwise
    """
    return functools.reduce(lambda acc, x: acc or (x >= 0), energy_result, False)


class Measurement:
    """
    measure the energy consumption of devices on a bounded period

    Beginning and end of this period are given by calling ``begin()`` and ``end()`` methods

    :param label: measurement label

    :param output: default output to export the recorded energy consumption. If None, the PrintOutput will be used
    """

    def __init__(self, label: str, output: Output = None):
        self.label = label
        self._energy_begin = None
        self._ts_begin = None
        self._results = None
        self._output = output if output is not None else PrintOutput()

        self._sensor = pyRAPL._sensor

    def begin(self):
        """
        Start energy consumption recording
        """
        self._energy_begin = self._sensor.energy()
        self._ts_begin = time_ns()

    def __enter__(self):
        """use Measurement as a context """
        self.begin()

    def __exit__(self, exc_type, exc_value, traceback):
        """use Measurement as a context """
        self.end()
        if(exc_type is None):
            self.export()

    def end(self):
        """
        End energy consumption recording
        """
        ts_end = time_ns()
        energy_end = self._sensor.energy()

        delta = energy_end - self._energy_begin
        duration = ts_end - self._ts_begin
        pkg = delta[0::2]  # get odd numbers
        pkg = pkg if empty_energy_result(pkg) else None  # set result to None if its contains only -1
        dram = delta[1::2]  # get even numbers
        dram = dram if empty_energy_result(dram) else None  # set result to None if its contains only -1

        self._results = Result(self.label, self._ts_begin / 1000000000, duration / 1000, pkg, dram)

    def export(self, output: Output = None):
        """
        Export the energy consumption measures to a given output

        :param output: output that will handle the measure, if None, the default output will be used
        """
        if output is None:
            self._output.add(self._results)
        else:
            output.add(self._results)

    @property
    def result(self) -> Result:
        """
        Access to the measurement data
        """
        return self._results


def measureit(_func=None, *, output: Output = None, number: int = 1):
    """
    Measure the energy consumption of monitored devices during the execution of the decorated function (if multiple runs it will measure the mean energy)

    :param output: output instance that will receive the power consummation data
    :param number: number of iteration in the loop in case you need multiple runs or the code is too fast to be measured
    """

    def decorator_measure_energy(func):
        @functools.wraps(func)
        def wrapper_measure(*args, **kwargs):
            sensor = Measurement(func.__name__, output)
            sensor.begin()
            for i in range(number):
                val = func(*args, **kwargs)
            sensor.end()
            sensor._results = sensor._results / number
            sensor.export()
            return val
        return wrapper_measure

    if _func is None:
        # to ensure the working system when you call it with parameters or without parameters
        return decorator_measure_energy
    else:
        return decorator_measure_energy(_func)
