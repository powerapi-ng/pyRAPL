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

from typing import Optional, List
from dataclasses import dataclass

@dataclass(frozen = True)
class Result:
    """
    A data class to represent the energy measures 
    """ 

    label: str 
    timestamp: float 
    duration: float 
    pkg: Optional[List[float]] = None
    dram: Optional[List[float]] = None

    # def __init__(self, label: str, timestamp: float, duration: float, pkg: Optional[List[float]] = None,
    #              dram: Optional[List[float]] = None):
    #     """
    #     :param label: the name of the Measurement
    #     :param [float] timestamp: The begining of the measurement (in seconds )
    #     :param [float] duration: The execution time (in seconds)n
    #     :param tuple [float] pkg: The energy consumption of  CPU of different sockets  (in Joules )
    #     :param tuple[float] dram: The energy consumption of DRAM in different sockets (in Joules)
    #     """
    #     self.label = label
    #     self.timestamp = timestamp
    #     self.duration = duration
    #     self.pkg = pkg.copy() if pkg is not None else None
    #     self.dram = dram.copy() if dram is not None else None

    #     def __str__(self):
    #         s = 'label : ' + self.label
    #         s += 'ts : ' + str(self.timestamp)
    #         s += 'duration : ' + str(self.duration)
    #         s += 'pkg : ' + str(self.pkg)
    #         s += 'dram : ' + str(self.dram)
    #         return s


    #     def __repr__(self):
    #         s = 'label : ' + self.label
    #         s += 'ts : ' + str(self.timestamp)
    #         s += 'duration : ' + str(self.duration)
    #         s += 'pkg : ' + str(self.pkg)
    #         s += 'dram : ' + str(self.dram)
    #         return s
