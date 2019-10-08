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

import pandas

from pyRAPL import Result
from pyRAPL.outputs import Output

# @Output.register
class DataFrameOutput:

    def __init__(self):
        self._data = None
        self._data = pandas.DataFrame(columns=list(Result.__annotations__.keys()) + ["socket"])

    def add(self, result):
        x = dict(vars(result))
        x['timestamp'] = time.ctime(x['timestamp'])
        for i in range(len(result.pkg)):
            x['socket'] = i
            x['pkg'] = result.pkg[i]
            x['dram'] = result.dram[i]
            self._data = self._data.append(x, ignore_index=True)

    @property
    def data(self) -> pandas.DataFrame:
        return self._data
