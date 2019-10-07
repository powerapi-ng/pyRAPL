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
from pyRAPL import Sensor, Device, sensor


def setup(devices: Optional[List[Device]] = None, socket_ids: Optional[List[int]] = None):
    """
    Configure the pyRAPL sensor
    :param devices: list of device to get power consumption if None, all the devices available on the machine will
                    be monitored
    :param socket_ids: if None, the API will get the power consumption of the whole machine otherwise, it will
                       get the power consumption of the devices on the given socket package
    :raise PyRAPLCantRecordEnergyConsumption: if the sensor can't get energy information about a device given in
                                              parameter
    :raise PyRAPLBadSocketIdException: if the sensor can't get energy information about a device given in
                                       parameter
    """
    sensor = Sensor(devices=devices, socket_ids=socket_ids)
