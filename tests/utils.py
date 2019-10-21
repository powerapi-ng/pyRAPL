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
import os
import pytest
# import pyfakefs

SOCKET_0_DIR_NAME = '/sys/class/powercap/intel-rapl/intel-rapl:0'
SOCKET_1_DIR_NAME = '/sys/class/powercap/intel-rapl/intel-rapl:1'

PKG_0_FILE_NAME = SOCKET_0_DIR_NAME + '/energy_uj'
PKG_0_VALUE = 12345
PKG_1_FILE_NAME = SOCKET_1_DIR_NAME + '/energy_uj'
PKG_1_VALUE = 54321

DRAM_0_DIR_NAME = SOCKET_0_DIR_NAME + '/intel-rapl:0:0'
DRAM_1_DIR_NAME = SOCKET_1_DIR_NAME + '/intel-rapl:1:0'

DRAM_0_FILE_NAME = DRAM_0_DIR_NAME + '/energy_uj'
DRAM_0_VALUE = 6789
DRAM_1_FILE_NAME = DRAM_1_DIR_NAME + '/energy_uj'
DRAM_1_VALUE = 9876


def write_new_energy_value(val, device, socket_id):
    file_names = {
        Device.PKG: [PKG_0_FILE_NAME, PKG_1_FILE_NAME],
        Device.DRAM: [DRAM_0_FILE_NAME, DRAM_1_FILE_NAME]
    }

    api_file_name = file_names[device][socket_id]
    if not os.path.exists(api_file_name):
        return
    api_file = open(api_file_name, 'w')
    print(str(val) + '\n')
    api_file.write(str(val) + '\n')
    api_file.close()


@pytest.fixture
def empty_fs(fs):
    """
    create an empty file system
    """
    fs.create_file('/sys/devices/system/cpu/present', contents='0')
    fs.create_file('/sys/devices/system/cpu/cpu0/topology/physical_package_id', contents='0')
    return fs


@pytest.fixture
def fs_one_socket(fs):
    """
    create a file system containing energy metric for package and dram on one socket
    """
    fs.create_file('/sys/devices/system/cpu/present', contents='0')
    fs.create_file('/sys/devices/system/cpu/cpu0/topology/physical_package_id', contents='0')

    fs.create_file(SOCKET_0_DIR_NAME + '/name', contents='package-0\n')
    fs.create_file(PKG_0_FILE_NAME, contents=str(PKG_0_VALUE) + '\n')

    fs.create_file(DRAM_0_DIR_NAME + '/name', contents='dram\n')
    fs.create_file(DRAM_0_FILE_NAME, contents=str(DRAM_0_VALUE) + '\n')
    return fs


@pytest.fixture
def fs_two_socket(fs):
    """
    create a file system containing energy metric for package and dram on two socket
    """
    fs.create_file('/sys/devices/system/cpu/present', contents='0-1')
    fs.create_file('/sys/devices/system/cpu/cpu0/topology/physical_package_id', contents='0')
    fs.create_file('/sys/devices/system/cpu/cpu1/topology/physical_package_id', contents='1')

    fs.create_file(SOCKET_0_DIR_NAME + '/name', contents='package-0\n')
    fs.create_file(PKG_0_FILE_NAME, contents=str(PKG_0_VALUE) + '\n')

    fs.create_file(DRAM_0_DIR_NAME + '/name', contents='dram\n')
    fs.create_file(DRAM_0_FILE_NAME, contents=str(DRAM_0_VALUE) + '\n')

    fs.create_file(SOCKET_1_DIR_NAME + '/name', contents='package-1\n')
    fs.create_file(PKG_1_FILE_NAME, contents=str(PKG_1_VALUE) + '\n')

    fs.create_file(DRAM_1_DIR_NAME + '/name', contents='dram\n')
    fs.create_file(DRAM_1_FILE_NAME, contents=str(DRAM_1_VALUE) + '\n')
    return fs


@pytest.fixture
def fs_one_socket_no_dram(fs):
    """
    create a file system containing energy metric for package and gpu and sys on one socket
    """
    fs.create_file('/sys/devices/system/cpu/present', contents='0')
    fs.create_file('/sys/devices/system/cpu/cpu0/topology/physical_package_id', contents='0')
    
    fs.create_file(SOCKET_0_DIR_NAME + '/name', contents='package-0\n')
    fs.create_file(PKG_0_FILE_NAME, contents=str(PKG_0_VALUE) + '\n')

    fs.create_file(SOCKET_0_DIR_NAME + '/intel-rapl:0:0' + '/name', contents='gpu\n')
    fs.create_file(SOCKET_0_DIR_NAME + '/intel-rapl:0:1' + '/name', contents='sys\n')