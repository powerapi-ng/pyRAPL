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
from typing import List

from pyRAPL import Result
from pyRAPL.outputs import Output


class BufferedOutput(Output):
    """
    Use a buffer to batch the output process

    The method ``add`` add data to the buffer and the method ``save`` outputs each data in the buffer. After that, the
    buffer is flushed

    Implement the abstract method ``_output_buffer`` to define how to output buffered data
    """

    def __init__(self):
        Output.__init__(self)
        self._buffer = []

    def add(self, result):
        """
        Add the given data to the buffer

        :param result: data that must be added to the buffer
        """
        x = dict(vars(result))
        x['timestamp'] = x['timestamp']
        for i in range(len(result.pkg)):
            x['socket'] = i
            x['pkg'] = result.pkg[i]
            x['dram'] = result.dram[i]
            self._buffer.append(x.copy())

    @property
    def buffer(self) -> List[Result]:
        """
        Return the buffer content

        :return: a list of all the ``Result`` instances contained in the buffer
        """
        return self._buffer

    def _output_buffer(self):
        """
        Abstract method

        Output all the data contained in the buffer

        :param data: data to output
        """
        raise NotImplementedError()

    def save(self):
        """
        Output each data in the buffer and empty the buffer
        """
        self._output_buffer()
        self._buffer = []
