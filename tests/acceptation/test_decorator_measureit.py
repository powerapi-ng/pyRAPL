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
# from mock import patch
# import time

import pyRAPL

POWER_CONSUMPTION_PKG = 20000
POWER_CONSUMPTION_DRAM = 30000
NUMBER_OF_ITERATIONS = 5


def test_decorator_measureit(fs_one_socket):
    """
    Test to measure the energy consumption of a function using the measure decorator

    - decorate a function with the measure decorator and use a CSVOutput
    - launch the function
    - read the produced csv file

    Test if:
      - the file contains 1 line + 1 header
      - a line contains the DRAM energy consumption
      - a line contains the PKG energy consumption
    """
    pyRAPL.setup()

    csv_output = pyRAPL.outputs.CSVOutput('output.csv')

    @pyRAPL.measureit(output=csv_output, number=NUMBER_OF_ITERATIONS)
    def measurable_function(a):
        # Power consumption of the function
        write_new_energy_value(POWER_CONSUMPTION_PKG, pyRAPL.Device.PKG, 0)
        write_new_energy_value(POWER_CONSUMPTION_DRAM, pyRAPL.Device.DRAM, 0)
        return 1 + a

    measurable_function(1)

    csv_output.save()

    csv = open('output.csv', 'r')

    # flush header
    csv.readline()

    n_lines = 0
    for line in csv:
        n_lines += 1
        content = line.split(',')
        print(content)
        assert content[0] == 'measurable_function'
        assert content[3] == str((POWER_CONSUMPTION_PKG - PKG_0_VALUE) / NUMBER_OF_ITERATIONS)
        assert content[4] == str((POWER_CONSUMPTION_DRAM - DRAM_0_VALUE) / NUMBER_OF_ITERATIONS)

    assert n_lines == 1
