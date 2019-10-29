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
import os
import re

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


def cpu_ids() -> List[int]:
    """
    return the cpu id of this machine
    """
    api_file = open('/sys/devices/system/cpu/present', 'r')

    cpu_id_tmp = re.findall('\d+|-', api_file.readline().strip())
    cpu_id_list = []
    for i in range(len(cpu_id_tmp)):
        if cpu_id_tmp[i] == '-':
            for cpu_id in range(int(cpu_id_tmp[i - 1]) + 1, int(cpu_id_tmp[i + 1])):
                cpu_id_list.append(int(cpu_id))
        else:
            cpu_id_list.append(int(cpu_id_tmp[i]))
    return cpu_id_list


def get_socket_ids() -> List[int]:
    """
    return cpu socket id present on the machine
    """
    socket_id_list = []
    for cpu_id in cpu_ids():
        api_file = open('/sys/devices/system/cpu/cpu' + str(cpu_id) + '/topology/physical_package_id')
        socket_id_list.append(int(api_file.readline().strip()))
    return list(set(socket_id_list))


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

        self._socket_ids = get_socket_ids() if socket_ids is None else socket_ids
        self._sockets = [RAPLSensorAPI(i, devices) for i in self._socket_ids]
        # self._devices = [ *i._devices for i in self._sockets] 
        self._devices = []
        self._offsets = []  # map each device with its socket 
        for i in self._sockets:
            self._devices += i._devices
            self._offsets += [i._socket_id] * len(i._devices)


    def energy(self) -> SubstractableList:
        """
        get the energy consumption of all the monitored devices
        :return: a tuple containing the energy consumption of each device for each socket. The tuple structure is :
                 (pkg energy socket 0, dram energy socket 0, core energy socket 0, core energy socket 1 ..., pkg energy socket N, dram energy socket N)
        """
        results = []
        for i in self._sockets:
            results += i.energy()
        return SubstractableList(results)


class SensorAPI:
    """
        API to read energy consumption for a sensor
    """

    def __init__(self, socket_id: int, devices: List[str] = None):
        self._socket_id = socket_id
        self._devices = devices

    def get_available_devices(self):
        """
        list the available devices present on this sensor
        """
        raise NotImplementedError()

    def energy(self):
        """
        Get the energy consumption of all the registred devices in the Sensor
        :return float tuple: a tuple containing the energy consumption (in uJ) the device on each socket
                            the Nth value of the tuple correspond to the energy consumption of the Nth device on the socket based on their registration order
        """
        raise NotImplementedError()


class RAPLSensorAPI(SensorAPI):

    def __init__(self, socket_id, devices=None):
        super().__init__(socket_id, devices=devices)
        self.get_available_devices()
        self._devices = list(self._available_devices.keys()) if devices is None else devices
        self._sys_files = [open(self._available_devices[f], 'r') for f in self._devices]
        self.count_devices = len(self._devices)
        del (self._available_devices)

    def get_available_devices(self):

        self._available_devices = {}

        def add_RAPL_device(path):
            """
            return the available devices present in a socket
            """
            try:
                with open(path + '/name') as f:
                    name = f.readline()[:-1]
                device_path = path + '/energy_uj'
                assert os.path.exists(device_path)
                self._available_devices[name] = device_path
            except FileNotFoundError as f:
                fname = f.filename.split('/')[-2]
                logging.warning(f'there is no device in {fname} but we will explore its sub-tree')

            for f in os.listdir(path):
                if f.startswith('intel-rapl:'):
                    add_RAPL_device(path + '/' + f)

        path = "/sys/devices/virtual/powercap/intel-rapl/intel-rapl:" + str(self._socket_id)
        if not os.path.exists(path):
            raise PyRAPLBadSocketIdException(self._socket_id)

        add_RAPL_device(path)
        self._available_devices['pkg'] = self._available_devices.pop('package-' + str(self._socket_id))

    def energy(self):
        result = [-1] * self.count_devices
        for i in range(self.count_devices):
            device_file = self._sys_files[i]
            device_file.seek(0, 0)
            result[i] = float(device_file.readline())
        return result

