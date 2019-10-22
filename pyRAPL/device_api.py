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
from typing import Optional, Tuple, List

from pyRAPL import Device, PyRAPLCantInitDeviceAPI, PyRAPLBadSocketIdException


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


class DeviceAPI:
    """
    API to read energy consumption from sysfs
    """

    def __init__(self, socket_ids: Optional[List[int]] = None):
        """
        :param int socket_ids: if None, the API will get the energy consumption of the whole machine otherwise, it will
                               get the energy consumption of the device on the given socket package
        :raise PyRAPLCantInitDeviceAPI: the machine where is initialised the DeviceAPI have no rapl interface for the
                                        target device
        :raise PyRAPLBadSocketIdException: the machine where is initialised the DeviceAPI has no the requested socket
        """
        all_socket_id = get_socket_ids()
        if socket_ids is None:
            self._socket_ids = all_socket_id
        else:
            for socket_id in socket_ids:
                if socket_id not in all_socket_id:
                    raise PyRAPLBadSocketIdException(socket_id)
            self._socket_ids = socket_ids

        self._socket_ids.sort()

        self._sys_files = self._open_rapl_files()

    def _open_rapl_files(self):
        raise NotImplementedError()

    def _get_socket_directory_names(self) -> List[Tuple[str, int]]:
        """
        :return (str, int): directory name, rapl_id
        """

        def add_to_result(directory_info, result):
            """
            check if the directory info could be added to the result list and add it
            """
            dirname, _ = directory_info
            f_name = open(dirname + '/name', 'r')
            pkg_str = f_name.readline()
            if 'package' not in pkg_str:
                return
            package_id = int(pkg_str[:-1].split('-')[1])

            if self._socket_ids is not None and package_id not in self._socket_ids:
                return
            result.append((package_id, ) + directory_info)

        rapl_id = 0
        result_list = []
        while os.path.exists('/sys/class/powercap/intel-rapl/intel-rapl:' + str(rapl_id)):
            dirname = '/sys/class/powercap/intel-rapl/intel-rapl:' + str(rapl_id)
            add_to_result((dirname, rapl_id), result_list)
            rapl_id += 1

        if len(result_list) != len(self._socket_ids):
            raise PyRAPLCantInitDeviceAPI()

        # sort the result list
        result_list.sort(key=lambda t: t[0])
        # return info without socket ids
        return list(map(lambda t: (t[1], t[2]), result_list))

    def energy(self) -> Tuple[float, ...]:
        """
        Get the energy consumption of the device since the last CPU reset
        :return float tuple: a tuple containing the energy consumption (in J) the device on each socket
                             the Nth value of the tuple correspond to the energy consumption of the device on the Nth
                             socket
        """
        result = [-1] * (self._socket_ids[-1] + 1)
        for i in range(len(self._sys_files)):
            device_file = self._sys_files[i]
            device_file.seek(0, 0)
            result[self._socket_ids[i]] = float(device_file.readline())
        return tuple(result)


class PkgAPI(DeviceAPI):

    def __init__(self, socket_ids: Optional[int] = None):
        DeviceAPI.__init__(self, socket_ids)

    def _open_rapl_files(self):
        directory_name_list = self._get_socket_directory_names()

        rapl_files = []
        for (directory_name, _) in directory_name_list:
            rapl_files.append(open(directory_name + '/energy_uj', 'r'))
        return rapl_files


class DramAPI(DeviceAPI):

    def __init__(self, socket_ids: Optional[int] = None):
        DeviceAPI.__init__(self, socket_ids)

    def _open_rapl_files(self):
        directory_name_list = self._get_socket_directory_names()

        def get_dram_file(socket_directory_name, rapl_socket_id, ):
            rapl_device_id = 0
            while os.path.exists(socket_directory_name + '/intel-rapl:' + str(rapl_socket_id) + ':' +
                                 str(rapl_device_id)):
                dirname = socket_directory_name + '/intel-rapl:' + str(rapl_socket_id) + ':' + str(rapl_device_id)
                f_device = open(dirname + '/name', 'r')
                if f_device.readline() == 'dram\n':
                    return open(dirname + '/energy_uj', 'r')
                rapl_device_id += 1
            raise PyRAPLCantInitDeviceAPI()

        rapl_files = []
        for (socket_directory_name, rapl_socket_id) in directory_name_list:
            rapl_files.append(get_dram_file(socket_directory_name, rapl_socket_id))

        return rapl_files


class DeviceAPIFactory:
    """
    Factory Returning DeviceAPI
    """
    @staticmethod
    def create_device_api(device: Device, socket_ids: Optional[int]) -> DeviceAPI:
        """
        :param device: the device corresponding to the DeviceAPI to be created
        :param socket_ids: param that will be passed to the constructor of the DeviceAPI instance
        :return: a DeviceAPI instance
        """
        if device == Device.PKG:
            return PkgAPI(socket_ids)
        if device == Device.DRAM:
            return DramAPI(socket_ids)
