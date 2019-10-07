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

from utils import fs_one_socket, PKG_0_VALUE, DRAM_0_VALUE
import time
import pyRAPL

POWER_CONSUMPTION_PKG = 20000
POWER_CONSUMPTION_DRAM = 30000

def measurable_function(a):
    return 1 + a

def test_nomal_measure_bench(fs_one_socket):
    """
    Test to measure the power consumption of a function using the Measurement class

    - launch the measure
    - write a new value to the RAPL power measurement api file
    - launch a function
    - end the measure

    Test if:
      - the power consumption measured is the delta between the first and the last value in the RAPL power measurement
        file
    """
    pyRAPL.setup()
    measure = pyRAPL.Measurement('toto')
    measure.begin()
    pkg_file = open('/sys/class/powercap/intel-rapl/intel-rapl:0/energy_uj', 'w')
    dram_file = open('/sys/class/powercap/intel-rapl/intel-rapl:0/intel-rapl:0:0/energy_uj', 'w')
    pkg_file.write(str(POWER_CONSUMPTION_PKG) + '\n')
    dram_file.write(str(POWER_CONSUMPTION_DRAM) + '\n')
    pkg_file.close()
    dram_file.close()
    measurable_function(1)
    measure.end()

    assert measure.result.pkg == [(20000 - PKG_0_VALUE) / 1000000]
    assert measure.result.dram == [(POWER_CONSUMPTION_DRAM - DRAM_0_VALUE) / 1000000]
