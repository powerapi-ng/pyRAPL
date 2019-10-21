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
"""
This module contains class that will be used by the ``measure`` decorator or the ``Measurement.export`` method to export
recorded measurement

example with the  ``measure decorator``::

    output_instance = pyRAPL.outputs.XXXOutput(...)

    @pyRAPL.measure(output=output_instance)
    def foo():
        ...

example with the ``Measurement.export`` function::

    measure = pyRAPL.Measurement('label')
    ...
    output_instance = pyRAPL.outputs.XXXOutput(...)
    measure.export(output_instance)

You can define your one output by inherit from the ``Output`` class and implements the ``add`` method.
This method will receive the measured energy consumption data as a ``Result`` instance and must handle it.

For example, the ``PrintOutput.add`` method will print the ``Result`` instance.
"""
import logging

from .output import Output
from .buffered_output import BufferedOutput
from .printoutput import PrintOutput
from .csvoutput import CSVOutput

try:
    from .mongooutput import MongoOutput

except ImportError:
    logging.warning("imports error \n You need to install pymongo>=3.9.0 in order to use MongoOutput ")

try:
    from .dataframeoutput import DataFrameOutput

except ImportError:
    logging.warning("imports error \n  You need to install pandas>=0.25.1 in order to use DataFrameOutput ")
