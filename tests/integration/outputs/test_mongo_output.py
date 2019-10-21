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
import pytest
import pymongo
from mock import patch, Mock

from pyRAPL import Result
from pyRAPL.outputs import MongoOutput

@patch('pymongo.MongoClient')
def test_save(_):

    output = MongoOutput(None, None, None)
    output._collection.insert_many = Mock()
    result = Result('toto', 0, 0.1, [0.1111, 0.2222], [0.3333, 0.4444])
    output.add(result)
    output.save()

    args = output._collection.insert_many.call_args[0][0]

    for i in range(2):
        assert args[i]['label'] == result.label
        assert args[i]['timestamp'] == result.timestamp
        assert args[i]['duration'] == result.duration
        assert args[i]['pkg'] == result.pkg[i]
        assert args[i]['dram'] == result.dram[i]
        assert args[i]['socket'] == i
