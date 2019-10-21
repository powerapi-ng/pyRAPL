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

import pytest
from pyRAPL import Result


def test_fulldiv():
    val = Result('toto', 0, 0.23456, [0.34567], [0.45678, 0.56789])
    correct_value = Result('toto', 0, 0.023456, [0.034567], [0.045678, 0.056789])
    result = val / 10
    assert result.label == correct_value.label
    assert result.timestamp == correct_value.timestamp
    assert round(result.duration, 6) == correct_value.duration
    assert [round(x, 6) for x in result.pkg] == correct_value.pkg
    assert [round(x, 6) for x in result.dram] == correct_value.dram
    assert len(result.pkg) == 1
    assert len(result.dram) == 2
