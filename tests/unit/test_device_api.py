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

import pytest

from pyRAPL import PkgAPI, DramAPI, DeviceAPIFactory, Device, PyRAPLCantInitDeviceAPI, PyRAPLBadSocketIdException
from pyRAPL.device_api import cpu_ids, get_socket_ids
from tests.utils import PKG_0_FILE_NAME, PKG_0_VALUE, PKG_1_FILE_NAME, PKG_1_VALUE
from tests.utils import DRAM_0_FILE_NAME, DRAM_0_VALUE, DRAM_1_FILE_NAME, DRAM_1_VALUE
from tests.utils import empty_fs, fs_one_socket, fs_two_socket, fs_one_socket_no_dram

class DeviceParameters:
    def __init__(self, device_class, socket0_filename, socket0_value, socket1_filename, socket1_value):
        print(device_class.__name__)
        self.device_class = device_class
        self.socket0_filename = socket0_filename
        self.socket0_value = socket0_value
        self.socket1_filename = socket1_filename
        self.socket1_value = socket1_value

@pytest.fixture(params=[DeviceParameters(PkgAPI, PKG_0_FILE_NAME, PKG_0_VALUE, PKG_1_FILE_NAME, PKG_1_VALUE),
                        DeviceParameters(DramAPI, DRAM_0_FILE_NAME, DRAM_0_VALUE, DRAM_1_FILE_NAME, DRAM_1_VALUE)])
def device_api_param(request):
    """
    parametrize a test with PkgAPI and DramAPI
    """
    print(request.param.device_class.__name__)
    return request.param

##########
# CPU ID #
##########
def test_cpu_ids_normal_interval(fs):
    fs.create_file('/sys/devices/system/cpu/present', contents='1-3')
    assert cpu_ids() == [1, 2, 3]


def test_cpu_ids_normal_list(fs):
    fs.create_file('/sys/devices/system/cpu/present', contents='1,3')
    assert cpu_ids() == [1, 3]


def test_cpu_ids_interval_and_list(fs):
    fs.create_file('/sys/devices/system/cpu/present', contents='1,3-5')
    assert cpu_ids() == [1, 3, 4, 5]


def test_cpu_ids_shuffuled_interval_and_list(fs):
    fs.create_file('/sys/devices/system/cpu/present', contents='2,3-6,11,1')
    assert cpu_ids() == [2, 3, 4, 5, 6, 11, 1]


#############
# SOCKET ID #
#############
def test_socket_ids(fs):
    fs.create_file('/sys/devices/system/cpu/present', contents='0-2')
    fs.create_file('/sys/devices/system/cpu/cpu0/topology/physical_package_id', contents='0')
    fs.create_file('/sys/devices/system/cpu/cpu1/topology/physical_package_id', contents='1')
    fs.create_file('/sys/devices/system/cpu/cpu2/topology/physical_package_id', contents='0')
    assert get_socket_ids() == [0, 1]


#############
# INIT TEST #
#############
def test_init_no_rapl_files(empty_fs, device_api_param):
    """
    create a DeviceAPI (PkgAPI and DramAPI) instance with a filesystem without rapl api files
    Test if:
      - a PyRAPLCantInitDeviceAPI is raised
    """
    with pytest.raises(PyRAPLCantInitDeviceAPI):
        device_api_param.device_class()


def test_init_psys_files_one_sockets(fs_one_socket, device_api_param):
    """
    create a DeviceAPI (PkgAPI and DramAPI) instance with a filesystem containing rapl files for socket 0 and psys
    domain
    Test if:
      - the attribute DeviceAPI._sys_files is a list of length 1
      - the attribute DeviceAPI._sys_files contains a file (test the file's name)
    """
    fs_one_socket.create_file('/sys/class/powercap/intel-rapl/intel-rapl:1/name', contents='psys\n')

    device_api = device_api_param.device_class()
    assert isinstance(device_api._sys_files, list)
    assert len(device_api._sys_files) == 1
    assert device_api._sys_files[0].name == device_api_param.socket0_filename


def test_init_psys_files_two_sockets(fs):
    """
    create a DeviceAPI (PkgAPI and DramAPI) instance with a filesystem containing rapl files for socket 0 and 1 and psys
    domain
    Test if:
      - the attribute DeviceAPI._sys_files is a list of length 2
      - the attribute DeviceAPI._sys_files contains two file (test the file's name)
    """
    fs.create_file('/sys/devices/system/cpu/present', contents='0-1')
    fs.create_file('/sys/devices/system/cpu/cpu0/topology/physical_package_id', contents='0')
    fs.create_file('/sys/devices/system/cpu/cpu1/topology/physical_package_id', contents='1')

    fs.create_file('/sys/class/powercap/intel-rapl/intel-rapl:0/name', contents='package-0\n')
    fs.create_file(PKG_0_FILE_NAME, contents=str(PKG_0_VALUE) + '\n')

    fs.create_file('/sys/class/powercap/intel-rapl/intel-rapl:1/name', contents='psys\n')

    fs.create_file('/sys/class/powercap/intel-rapl/intel-rapl:2/name', contents='package-1\n')
    fs.create_file('/sys/class/powercap/intel-rapl/intel-rapl:2/energy_uj', contents=str(PKG_1_VALUE) + '\n')

    device_api = PkgAPI()
    assert isinstance(device_api._sys_files, list)
    assert len(device_api._sys_files) == 2
    assert device_api._sys_files[0].name == PKG_0_FILE_NAME
    assert device_api._sys_files[1].name == '/sys/class/powercap/intel-rapl/intel-rapl:2/energy_uj'


def test_init_one_file_one_socket(fs_one_socket, device_api_param):
    """
    create a DeviceAPI (PkgAPI and DramAPI) instance to measure energy consumption of device on socket 0
    The filesystem contains a rapl file for the socket 0
    Test if:
      - the attribute DeviceAPI._sys_files is a list of length 1
      - the attribute DeviceAPI._sys_files contains a file (test the file's name)
    """
    device_api = device_api_param.device_class()
    assert isinstance(device_api._sys_files, list)
    assert len(device_api._sys_files) == 1
    assert device_api._sys_files[0].name == device_api_param.socket0_filename


def test_init_two_files_one_socket(fs_two_socket, device_api_param):
    """
    create a DeviceAPI (PkgAPI and DramAPI) instance to measure energy consumption of device on socket 0
    The filesystem contains a rapl file for the socket 0 and 1
    Test if:
      - the attribute DeviceAPI._sys_files is a list of length 1
      - the attribute DeviceAPI._sys_files contains a file (test the file's name)
    """
    device_api = device_api_param.device_class(socket_ids=[0])
    assert isinstance(device_api._sys_files, list)
    assert len(device_api._sys_files) == 1
    assert device_api._sys_files[0].name == device_api_param.socket0_filename


def test_init_two_files_last_socket(fs_two_socket, device_api_param):
    """
    create a DeviceAPI (PkgAPI and DramAPI) instance to measure energy consumption of device on socket 1
    The filesystem contains a rapl file for the socket 0 and 1
    Test if:
      - the attribute DeviceAPI._sys_files is a list of length 1
      - the attribute DeviceAPI._sys_files contains one files (test the file's name)
    """
    device_api = device_api_param.device_class(socket_ids=[1])

    assert isinstance(device_api._sys_files, list)
    assert len(device_api._sys_files) == 1

    assert device_api._sys_files[0].name == device_api_param.socket1_filename


def test_init_one_file_two_socket(fs_one_socket, device_api_param):
    """
    create a DeviceAPI (PkgAPI and DramAPI) instance to measure energy consumption of device on socket 0 and 1
    The filesystem contains a rapl file for the socket 0
    Test if:
      - a PyRAPLBadSocketIdException is raised
    """
    with pytest.raises(PyRAPLBadSocketIdException):
        device_api_param.device_class(socket_ids=[0, 1])


def test_init_two_files_two_socket(fs_two_socket, device_api_param):
    """
    create a DeviceAPI (PkgAPI and DramAPI) instance to measure energy consumption of device on socket 0 and 1
    The filesystem contains a rapl file for the socket 0 and 1
    Test if:
      - the attribute DeviceAPI._sys_files is a list of length 2
      - the attribute DeviceAPI._sys_files contains two files (test the file's name)
    """
    device_api = device_api_param.device_class(socket_ids=[0, 1])

    assert isinstance(device_api._sys_files, list)
    assert len(device_api._sys_files) == 2

    assert device_api._sys_files[0].name == device_api_param.socket0_filename
    assert device_api._sys_files[1].name == device_api_param.socket1_filename


def test_init_two_files_all_socket(fs_two_socket, device_api_param):
    """
    create a DeviceAPI (PkgAPI and DramAPI) instance to measure energy consumption of device on socket 0 and 1
    The filesystem contains a rapl file for the socket 0 and 1
    Test if:
      - the attribute DeviceAPI._sys_files is a list of length 2
      - the attribute DeviceAPI._sys_files contains two files (test the file's name)
    """
    device_api = device_api_param.device_class()

    assert isinstance(device_api._sys_files, list)
    assert len(device_api._sys_files) == 2

    assert device_api._sys_files[0].name == device_api_param.socket0_filename
    assert device_api._sys_files[1].name == device_api_param.socket1_filename

def test_init_dram_api_without_dram_files(fs_one_socket_no_dram):
    """
    create a DramAPI instance to measure energy consumption of device on socket 0
    The file system contains a rapl file for the socket 0 but no dram support
    Test if:
      - a PyRAPLCantInitDeviceAPI is raised
    """
    with pytest.raises(PyRAPLCantInitDeviceAPI):
        DramAPI()


##########
# ENERGY #
##########
def test_energy_one_file_socket_0(device_api_param, fs_one_socket):
    """
    create a DeviceAPI (PkgAPI and DramAPI) instance to measure energy consumption of device on socket 0
    use the energy function to get the energy consumption
    The filesystem contains a rapl file for the socket 0
    Test if:
      - the returned value is a tuple of length 1 containing float
      - the first value of the tuple is the energy consumption of the corresponding device on socket 0
    """
    device_api = device_api_param.device_class()

    energy = device_api.energy()
    assert isinstance(energy, tuple)
    assert len(energy) == 1
    assert isinstance(energy[0], float)

    assert energy[0] == device_api_param.socket0_value


def test_energy_two_files_socket_0(device_api_param, fs_two_socket):
    """
    create a DeviceAPI (PkgAPI and DramAPI) instance to measure energy consumption of device on socket 0
    use the energy function to get the energy consumption
    The filesystem contains a rapl file for the socket 0 and 1
    Test if:
      - the returned value is a tuple of length 1 containing float
      - the first value of the tuple is the energy consumption of the corresponding device on socket 0
    """
    device_api = device_api_param.device_class(socket_ids=[0])

    energy = device_api.energy()
    assert isinstance(energy, tuple)
    assert len(energy) == 1
    assert isinstance(energy[0], float)

    assert energy[0] == device_api_param.socket0_value


def test_energy_two_files_socket_1(device_api_param, fs_two_socket):
    """
    create a DeviceAPI (PkgAPI and DramAPI) instance to measure energy consumption of device on socket 1
    use the energy function to get the energy consumption
    The filesystem contains a rapl file for the socket 0 and 1
    Test if:
      - the returned value is a tuple of length 2 containing float
      - the first value of the tuple is -1
      - the second value of the tuple is the energy consumption of the corresponding device on socket 1
    """
    device_api = device_api_param.device_class(socket_ids=[1])

    energy = device_api.energy()
    assert isinstance(energy, tuple)
    assert len(energy) == 2

    assert energy[0] == -1
    assert isinstance(energy[1], float)
    assert energy[1] == device_api_param.socket1_value


def test_energy_two_files_socket_0_1(device_api_param, fs_two_socket):
    """
    create a DeviceAPI (PkgAPI and DramAPI) instance to measure energy consumption of device on socket 0 and 1
    use the energy function to get the energy consumption
    The filesystem contains a rapl file for the socket 0 and 1
    Test if:
      - the returned value is a tuple of length 2 containing float
      - the first value of the tuple is the energy consumption of the corresponding device on socket 0
      - the second value of the tuple is the energy consumption of the corresponding device on socket 1
    """
    device_api = device_api_param.device_class(socket_ids=[0, 1])

    energy = device_api.energy()
    assert isinstance(energy, tuple)
    assert len(energy) == 2
    for val in energy:
        assert isinstance(val, float)

    assert energy[0] == device_api_param.socket0_value
    assert energy[1] == device_api_param.socket1_value


def test_energy_two_files_socket_all(device_api_param, fs_two_socket):
    """
    create a DeviceAPI (PkgAPI and DramAPI) instance to measure energy consumption of device on all socket
    use the energy function to get the energy consumption
    The filesystem contains a rapl file for the socket 0 and 1
    Test if:
      - the returned value is a tuple of length 2 containing float
      - the first value of the tuple is the energy consumption of the corresponding device on socket 0
      - the second value of the tuple is the energy consumption of the corresponding device on socket 1
    """
    device_api = device_api_param.device_class()

    energy = device_api.energy()
    assert isinstance(energy, tuple)
    assert len(energy) == 2
    for val in energy:
        assert isinstance(val, float)

    assert energy[0] == device_api_param.socket0_value
    assert energy[1] == device_api_param.socket1_value


def test_energy_two_files_socket_1_0(device_api_param, fs_two_socket):
    """
    create a DeviceAPI (PkgAPI and DramAPI) instance to measure energy consumption of device on socket 1 and 0
    use the energy function to get the energy consumption
    The filesystem contains a rapl file for the socket 0 and 1
    Test if:
      - the returned value is a tuple of length 2 containing float
      - the first value of the tuple is the energy consumption of the corresponding device on socket 0
      - the second value of the tuple is the energy consumption of the corresponding device on socket 1
    """
    device_api = device_api_param.device_class(socket_ids=[1, 0])

    energy = device_api.energy()
    assert isinstance(energy, tuple)
    assert len(energy) == 2
    for val in energy:
        assert isinstance(val, float)

    assert energy[0] == device_api_param.socket0_value
    assert energy[1] == device_api_param.socket1_value


###########
# FACTORY #
###########
def test_creating_dram_device(fs_two_socket):
    """
    use the DeviceAPIFactory to create a DramAPI instance
    Test if:
      - the returned instance is an instance of DramAPI
    """
    assert isinstance(DeviceAPIFactory.create_device_api(Device.DRAM, None), DramAPI)


def test_creating_pkg_device(fs_two_socket):
    """
    use the DeviceAPIFactory to create a PkgAPI instance
    Test if:
      - the returned instance is an instance of PkgAPI
    """
    assert isinstance(DeviceAPIFactory.create_device_api(Device.PKG, None), PkgAPI)
