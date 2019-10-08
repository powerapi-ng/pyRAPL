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
import os
from typing import List
from .output import *

@Output.register
class CSVOutput:

    def __init__(self, filename):
        self.filename = filename
        self.header = ",".join(list(Result.__annotations__.keys()) + ["socket"]) + "\n"
        self._data = []

    def add(self, result):
        x = dict(vars(result))
        x['timestamp'] = x['timestamp']
        for i in range(len(result.pkg)):
            x['socket'] = i
            x['pkg'] = result.pkg[i]
            x['dram'] = result.dram[i]
            self._data.append(x.copy())

    @property
    def data(self) -> List:
        return self._data

    def save(self):
        """"
        Save the curent data in a csv file . If the file exists it will append the results in the end and the file
        otherwise it will create a new file.
        After saving. the data will be removed from the RAM memeory
        """
        cond = os.path.exists(self.filename)
        with open(self.filename, "a+") as f:
            if not cond:
                f.writelines(self.header)
            for i in self._data:
                s = ",".join([str(j) for j in i.values()]) + "\n"
                f.writelines(s)
        del self._data
        self._data = []
