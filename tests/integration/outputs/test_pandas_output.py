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
import time

from pyRAPL import Result
from pyRAPL.outputs import DataFrameOutput


def assert_line_equal_result(df, n, result):
    assert df.iat[n, 0] == result.label
    assert df.iat[n, 1] == time.ctime(result.timestamp)
    assert df.iat[n, 2] == result.duration
    assert df.iat[n, 3] == result.pkg[0]
    assert df.iat[n, 4] == result.dram[0]
    assert df.iat[n, 5] == 0

    assert df.iat[n + 1, 0] == result.label
    assert df.iat[n + 1, 1] == time.ctime(result.timestamp)
    assert df.iat[n + 1, 2] == result.duration
    assert df.iat[n + 1, 3] == result.pkg[1]
    assert df.iat[n + 1, 4] == result.dram[1]
    assert df.iat[n + 1, 5] == 1

    # assert df.iat[n, 3][1] == result.pkg[1]
    # assert df.iat[n, 4][1] == result.dram[1


def test_dataframe():
    """
    Add 2 result to a dataframe
    """

    output = DataFrameOutput()
    result_list = [
        Result('toto', 0, 0.1, [0.1111, 0.2222], [0.3333, 0.4444]),
        Result('titi', 0, 0.2, [0.5555, 0.6666], [0.7777, 0.8888]),
    ]

    output.add(result_list[0])

    assert_line_equal_result(output.data, 0, result_list[0])

    output.add(result_list[1])

    for i in range(2):
        assert_line_equal_result(output.data, 2 * i, result_list[i])
