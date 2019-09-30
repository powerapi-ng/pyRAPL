# MIT License
# Copyright (c) 2018, INRIA
# Copyright (c) 2018, University of Lille
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

import array

from pyRAPL import sensor, output, PyRAPLSensorNotInitializedException, PyRAPLNoEnergyConsumptionRecordStartedException

class Sample:

    def __init__(self):

        if sensor is None:
            raise PyRAPLSensorNotInitializedException

        #: Name of the function that its power consumption is measuring
        self.function_name = None
        #: begining measuring time
        self.begin_timestamp = None
        #: function execution time
        self.duration = None
        #: power consumption data
        #: python array containing the power consumption of each measured device for each monitored socket
        #: [0 + 2*I] -> CPU package power consumption (socket I)
        #: [1 + 2*I] -> DRAM power consumption (socket I)
        self.data = array.array('I', [-1] * sensor.number_of_socket)

        self._measure_launched = False

    def start(self):
        """
        Start the power consumption measure, reset all the previous measure done with this sample
        """

    def stop(self):
        """
        Stop the power consumption measure
        :raise PyRAPLNoEnergyConsumptionRecordStartedException: if no power consumption recording was started
        """

    def save(self):
        """
        Use the predefined output to save this sample
        """
        if output is None:
            pass
        else:
            output.save(self)
