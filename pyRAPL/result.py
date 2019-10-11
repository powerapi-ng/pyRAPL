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


@dataclass(frozen=True)
class Result:
    """
    A data class to represent the energy measures

    :var label: measurement label
    :vartype label: str
    :var timestamp: measurement's beginning time
    :vartype timestamp: float
    :var duration:  measurement's duration
    :vartype duration: float
    :var pkg: list of the CPU power consumption (one value for each socket) if None, no CPU power consumption was
              recorded
    :vartype pkg: Optional[List[float]]
    :var dram: list of the RAM power consumption (one value for each socket) if None, no RAM power consumption was
               recorded
    :vartype dram: Optional[List[float]]
    """
    label: str
    timestamp: float
    duration: float
    pkg: Optional[List[float]] = None
    dram: Optional[List[float]] = None
