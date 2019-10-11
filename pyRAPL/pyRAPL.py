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
from typing import List, Optional
from pyRAPL import Sensor, Device
import pyRAPL


def setup(devices: Optional[List[Device]] = None, socket_ids: Optional[List[int]] = None):
    """
    Configure which device and CPU socket should be monitored by pyRAPL

    This function must be called before using any other pyRAPL functions

    :param devices: list of monitored devices if None, all the available devices on the machine will be monitored

    :param socket_ids: list of monitored sockets, if None, all the available socket on the machine will be monitored

    :raise PyRAPLCantRecordEnergyConsumption: if the sensor can't get energy information about the given device in parameter

    :raise PyRAPLBadSocketIdException: if the given socket in parameter doesn't exist
    """
    pyRAPL._sensor = Sensor(devices=devices, socket_ids=socket_ids)
