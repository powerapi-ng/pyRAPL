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
from pyRAPL import Device


class PyRAPLException(Exception):
    """Parent class of all PyRAPL exception
    """


class PyRAPLNoEnergyConsumptionRecordedException(PyRAPLException):
    """Exception raised when a function recorded_energy() is executed without stopping consumption recording before
    """


class PyRAPLNoEnergyConsumptionRecordStartedException(PyRAPLException):
    """Exception raised when a function stop() is executed without starting consumption recording before"""


class PyRAPLCantRecordEnergyConsumption(PyRAPLException):
    """Exception raised when starting recording energy consumption for a device but no energy consumption metric is
    available for this device

    :var device: device that couldn't be monitored (if None, Any device on the machine could be monitored)
    :vartype device: Device
    """
    def __init__(self, device: Device):
        PyRAPLException.__init__(self)
        self.device = device


class PyRAPLCantInitDeviceAPI(PyRAPLException):
    """
    Exception raised when trying to initialise a DeviceAPI instance on a machine that can't support it. For example,
    initialise a DramAPI on a machine without dram rapl interface will throw a PyRAPLCantInitDeviceAPI
    """


class PyRAPLBadSocketIdException(PyRAPLException):
    """
    Exception raised when trying to initialise PyRAPL on a socket that doesn't exist on the machine

    :var socket_id: socket that doesn't exist
    :vartype socket_id: int
    """

    def __init__(self, socket_id: int):
        PyRAPLException.__init__(self)
        self.socket_id = socket_id
