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

from pyRAPL import Result
from pyRAPL.outputs import BufferedOutput


class CSVOutput(BufferedOutput):
    """
    Write the recorded measure in csv format on a file

    if the file already exists, the result will be append to the end of the file, otherwise it will create a new file.

    This instance act as a buffer. The method ``add`` add data to the buffer and the method ``save`` append each data
    in the buffer at the end of the csv file. After that, the buffer is flushed

    :param filename: file's name  were the result will be written

    :param separator: character used to separate columns in the csv file

    :param append: Turn it to False to delete file if it already exist.
    """
    def __init__(self, filename: str, separator: str = ',', append: bool = True):
        BufferedOutput.__init__(self)
        self._separator = separator
        self._buffer = []
        self._filename = filename

        # Create file with header if it not exist or if append is False
        if not os.path.exists(self._filename) or not append:
            header = separator.join(list(Result.__annotations__.keys()) + ['socket']) + '\n'

            with open(self._filename, 'w+') as csv_file:
                csv_file.writelines(header)

    def _output_buffer(self):
        """
        Append the data at the end of the csv file
        :param data: data to write
        """
        with open(self._filename, 'a+') as csv_file:
            for data in self._buffer:
                line = self._separator.join([str(column) for column in data.values()]) + '\n'
                csv_file.writelines(line)
