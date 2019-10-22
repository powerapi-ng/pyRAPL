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

from tests.utils import fs_one_socket, write_new_energy_value, PKG_0_VALUE, DRAM_0_VALUE
import pyRAPL

POWER_CONSUMPTION_PKG = 20000
POWER_CONSUMPTION_DRAM = 30000


def measurable_function(a):
    # Power consumption of the function
    write_new_energy_value(POWER_CONSUMPTION_PKG, pyRAPL.Device.PKG, 0)
    write_new_energy_value(POWER_CONSUMPTION_DRAM, pyRAPL.Device.DRAM, 0)
    return 1 + a


class dummyOutput(pyRAPL.outputs.Output):
    data = None

    def add(self, result: pyRAPL.Result):
        self.data = result



def test_context_measure(fs_one_socket):
    """
    Test to measure the energy consumption of a function using the Measurement class

    - launch the measure
    - write a new value to the RAPL power measurement api file
    - launch a function
    - end the measure

    Test if:
      - the energy consumption measured is the delta between the first and the last value in the RAPL power measurement
        file
    """
    pyRAPL.setup()
    out = dummyOutput()
    with pyRAPL.Measurement('toto', output=out):
        measurable_function(1)

    assert out.data.pkg == [(POWER_CONSUMPTION_PKG - PKG_0_VALUE)]
    assert out.data.dram == [(POWER_CONSUMPTION_DRAM - DRAM_0_VALUE)]
