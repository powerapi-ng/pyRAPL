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
from pyRAPL.outputs import PrintOutput


def test_non_raw_output():
    """
    run PrintOutput._format_output to print non raw result

    Test if:
      the returned string is correct
    """
    result = Result('toto', 0, 0.23456, [0.34567], [0.45678, 0.56789])
    correct_value = f"""Label : toto
Begin : {time.ctime(result.timestamp)}
Duration :     0.2346 us
-------------------------------
PKG :
\tsocket 0 :     0.3457 uJ
-------------------------------
DRAM :
\tsocket 0 :     0.4568 uJ
\tsocket 1 :     0.5679 uJ
-------------------------------"""
    output = PrintOutput()
    print(output._format_output(result))
    assert output._format_output(result) == correct_value
