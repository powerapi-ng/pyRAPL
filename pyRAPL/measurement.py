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

from typing import List
from time import time
from pyRAPL import sensor, Result
from pyRAPL import PrintOutput, Output
from pyRAPL import Result
import pyRAPL

class Measurement:
    """
    An object used to record the energy measurement between two instances
    """
    def __init__(self, label: str, output: Output = None):
        self.label = label
        self._energy_begin = None
        self._ts_begin = None
        self._results = None
        self._output = output if output is not None  else PrintOutput()

        self.sensor = pyRAPL.__sensor


    def begin(self):
        """
        To start recording
        """
        self._energy_begin = self.sensor.energy()
        self._ts_begin = time()

    def end(self):
        ts_end = time()
        energy_end = self.sensor.energy()

        delta = energy_end - self._energy_begin
        duration = ts_end - self._ts_begin
        pkg = delta[0::2]  # get odd numbers
        dram = delta[1::2]  # get even numbers

        self._results = Result(self.label, self._ts_begin, duration, pkg, dram)

    def export(self, output=None):
        if output is None:
            self._output.add(self._results)
        else:
            output.add(self._results)


    @property
    def result(self) -> Result:
        return self._results



def measure(_func=None, *, output: Output = None):
    """ a decorator to measure the energy consumption of a function recorded by PyRAPL
    :param Output output : to handle the results recorded from pyrapl
    """


    def decorator_measure_energy(func):
        @functools.wraps(func)
        def wrapper_measure(*args, **kwargs):
            sensor = Measurement(func.__name__, output)
            sensor.begin()
            val = func(*args, **kwargs)
            sensor.end()
            sensor.export()
            return val
        return wrapper_measure

    if _func is None:
        # to ensure the working system when you call it with parameters or without parameters
        return decorator_measure_energy
    else:
        return decorator_measure_energy(_func)
