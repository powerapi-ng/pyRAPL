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

from pyRAPL import Device, DeviceAPIFactory, PyRAPLCantInitDeviceAPI, PyRAPLCantRecordEnergyConsumption
from pyRAPL import PyRAPLBadSocketIdException


class SubstractableList(list):
    """
    Substract each element of a list to another list except if they are negative numbers
    """
    def __sub__(self, other):
        if len(other) != len(self):
            raise ValueError("List are not of the same length")
        return [a - b if a >= 0 and b >= 0 else -1 for a, b in zip(self, other)]


class Sensor:
    """
    Global singleton that return global energy consumption about monitored devices
    """

    def __init__(self, devices: Optional[List[Device]] = None, socket_ids: Optional[List[int]] = None):
        """
        :param devices: list of device to get energy consumption if None, all the devices available on the machine will
                        be monitored
        :param socket_ids: if None, the API will get the energy consumption of the whole machine otherwise, it will
                           get the energy consumption of the devices on the given socket package
        :raise PyRAPLCantRecordEnergyConsumption: if the sensor can't get energy information about a device given in
                                                  parameter
        :raise PyRAPLBadSocketIdException: if the sensor can't get energy information about a device given in
                                           parameter
        """
        self._available_devices = []
        self._device_api = {}
        self._socket_ids = None

        tmp_device = devices if devices is not None else [Device.PKG, Device.DRAM]
        for device in tmp_device:
            try:
                self._device_api[device] = DeviceAPIFactory.create_device_api(device, socket_ids)
                self._available_devices.append(device)
            except PyRAPLCantInitDeviceAPI:
                if devices is not None:
                    raise PyRAPLCantRecordEnergyConsumption(device)
            except PyRAPLBadSocketIdException as exn:
                raise exn

        if not self._available_devices:
            raise PyRAPLCantRecordEnergyConsumption(None)

        self._socket_ids = socket_ids if socket_ids is not None else list(self._device_api.values())[0]._socket_ids

    def energy(self) -> SubstractableList:
        """
        get the energy consumption of all the monitored devices
        :return: a tuple containing the energy consumption of each device for each socket. The tuple structure is :
                 (pkg energy socket 0, dram energy socket 0, ..., pkg energy socket N, dram energy socket N)
        """
        result = SubstractableList([-1, -1] * (self._socket_ids[-1] + 1))
        # print((result, self._socket_ids))
        for device in self._available_devices:
            energy = self._device_api[device].energy()
            for socket_id in range(len(energy)):
                result[socket_id * 2 + device] = energy[socket_id]
        return result
