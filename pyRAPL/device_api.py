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
from typing import Optional, Tuple, List

from pyRAPL import PyRAPLCantInitDeviceAPI


class DeviceAPI:
    """
    API to read energy power consumption from sysfs
    """

    def __init__(self, socket_ids: Optional[int] = None):
        """
        :param int socket_ids: if None, the API will get the power consumption of the whole machine otherwise, it will
                               get the power consumption of the device on the given socket package
        :raise PyRAPLCantInitDeviceAPI: the machine where is initialised the DeviceAPI have no rapl interface for the
                                        target device
        :raise PyRAPLBadSocketIdException: the machine where is initialised the DeviceAPI has no the requested socket
        """
        self._socket_ids = socket_ids
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
            package_id = int(f_name.readline()[:-1].split('-')[1])

            if self._socket_ids is not None and package_id not in self._socket_ids:
                pass
            else:
                result.append((package_id, ) + directory_info)

        rapl_id = 0
        result_list = []
        while os.path.exists('/sys/class/powercap/intel-rapl/intel-rapl:' + str(rapl_id)):
            dirname = '/sys/class/powercap/intel-rapl/intel-rapl:' + str(rapl_id)
            add_to_result((dirname, rapl_id), result_list)
            rapl_id += 1

        # check if the required sockets were found
        if self._socket_ids is not None and len(self._socket_ids) != len(result_list):
            raise PyRAPLCantInitDeviceAPI()
        # check if socket files were found
        if not result_list:
            raise PyRAPLCantInitDeviceAPI()

        # sort the result list and remove unused informations
        result_list.sort(key=lambda t: t[0])
        return list(map(lambda t: (t[1], t[2]), result_list))

    def energy(self) -> Tuple[float, ...]:
        """
        Get the power consumption of the device since the last CPU reset
        :return float tuple: a tuple containing the power consumption (in J) the device on each socket
                             the Nth value of the tuple correspond to the power consumption of the device on the Nth
                             socket
        """


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
