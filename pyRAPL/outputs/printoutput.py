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
import time

from pyRAPL import Result
from pyRAPL.outputs import Output


def print_energy(energy):
    s = ""
    for i in range(len(energy)):
        if isinstance(energy[i], float):
            s = s + f"\n\tsocket {i} : {energy[i]: 10.4f} uJ"
        else:
            s = s + f"\n\tsocket {i} : {energy[i]} uJ"
    return s


class PrintOutput(Output):
    """
    Output that print data on standard output

    :param raw: if True, print the raw result class to standard output.
                Otherwise, print a fancier representation of result
    """

    def __init__(self, raw: bool = False):
        Output.__init__(self)

        self._raw = raw

    def _format_output(self, result):
        if self._raw:
            return str(result)
        else:
            s = f"""Label : {result.label}\nBegin : {time.ctime(result.timestamp)}\nDuration : {result.duration:10.4f} us"""
            if result.pkg is not None:
                s += f"""\n-------------------------------\nPKG :{print_energy(result.pkg)}"""
            if result.dram is not None:
                s += f"""\n-------------------------------\nDRAM :{print_energy(result.dram)}"""
                s += '\n-------------------------------'
            return s

    def add(self, result: Result):
        """
        print result on standard output

        :param result: data to print
        """
        print(self._format_output(result))
