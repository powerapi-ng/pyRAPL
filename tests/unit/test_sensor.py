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

from pyRAPL import Sensor, Device, PkgAPI
from pyRAPL import PyRAPLCantRecordEnergyConsumption, PyRAPLCantRecordEnergyConsumption, PyRAPLBadSocketIdException
from tests.utils import PKG_0_VALUE, PKG_1_VALUE, DRAM_0_VALUE, DRAM_1_VALUE
from tests.utils import empty_fs, fs_one_socket, fs_two_socket, fs_one_socket_no_dram


########
# INIT #
########
def test_no_rapl_api(empty_fs):
    """
    create an instance of Sensor to monitor all device available
    the system have no rapl api
    Test if:
      - a PyRAPLCantRecordEnergyConsumption is raise
    """
    with pytest.raises(PyRAPLCantRecordEnergyConsumption):
        Sensor()


def test_no_rapl_api_for_dram(fs_one_socket_no_dram):
    """
    create an instance of Sensor to monitor DRAM
    the system have no rapl api for dram but have one for package
    Test if:
      - a PyRAPLCantRecordEnergyConsumption is raise
    """
    with pytest.raises(PyRAPLCantRecordEnergyConsumption):
        Sensor(devices=[Device.DRAM])

def test_measure_all_no_rapl_api_for_dram(fs_one_socket_no_dram):
    """
    create an instance of Sensor to all available devices
    the system have no rapl api for dram but have one for package
    Test if:
      - the sensor attribute _device_api contains only one entrie. 
      - The entrie key is Device.Pkg and its value is an instance of PkgAPI
    """
    sensor = Sensor()
    assert len(sensor._device_api) == 1
    assert Device.PKG in sensor._device_api
    assert isinstance(sensor._device_api[Device.PKG], PkgAPI)


def test_monitor_socket_1_but_one_socket(fs_one_socket):
    """
    create an instance of Sensor to monitor all device available on socket 1
    the system have no rapl api for socket 1 but have one for socket 0
    Test if:
      - a PyRAPLBadSocketIdException is raise
    """
    with pytest.raises(PyRAPLBadSocketIdException):
        Sensor(socket_ids=[1])


##########
# ENERGY #
##########
class SensorParam:
    def __init__(self, devices, sockets, one_socket_result, two_socket_result):

        def div_if_positive_list(t, n):
            r = []
            for v in t:
                if v > 0:
                    r.append(v / n)
                else:
                    r.append(v)
            return r

        self.devices = devices
        self.sockets = sockets
        self.one_socket_result = one_socket_result
        self.two_socket_result = two_socket_result
        # assert False


@pytest.fixture(params=[
    SensorParam(None, None, [PKG_0_VALUE, DRAM_0_VALUE], [PKG_0_VALUE, DRAM_0_VALUE, PKG_1_VALUE, DRAM_1_VALUE]),
    SensorParam([Device.PKG], None, [PKG_0_VALUE, -1], [PKG_0_VALUE, -1, PKG_1_VALUE, -1]),
    SensorParam([Device.DRAM], None, [-1, DRAM_0_VALUE], [-1, DRAM_0_VALUE, -1, DRAM_1_VALUE]),
    SensorParam([Device.PKG, Device.DRAM], None, [PKG_0_VALUE, DRAM_0_VALUE], [PKG_0_VALUE, DRAM_0_VALUE, PKG_1_VALUE,
                                                                               DRAM_1_VALUE]),

    SensorParam(None, [0], [PKG_0_VALUE, DRAM_0_VALUE], [PKG_0_VALUE, DRAM_0_VALUE]),
    SensorParam([Device.PKG], [0], [PKG_0_VALUE, -1], [PKG_0_VALUE, -1]),
    SensorParam([Device.DRAM], [0], [-1, DRAM_0_VALUE], [-1, DRAM_0_VALUE]),
    SensorParam([Device.PKG, Device.DRAM], [0], [PKG_0_VALUE, DRAM_0_VALUE], [PKG_0_VALUE, DRAM_0_VALUE]),
])
def sensor_param(request):
    """
    parametrize a test with sensor parameters
    """
    parameters = request.param
    print('test parameters')
    print('Device list : ' + str(parameters.devices))
    print('socket list : ' + str(parameters.sockets))
    print('one socket result : ' + str(parameters.one_socket_result))
    print('two socket result : ' + str(parameters.two_socket_result))

    return parameters


@pytest.fixture(params=[
    SensorParam(None, [1], None, [-1, -1, PKG_1_VALUE, DRAM_1_VALUE]),
    SensorParam([Device.PKG], [1], None, [-1, -1, PKG_1_VALUE, -1]),
    SensorParam([Device.DRAM], [1], None, [-1, -1, -1, DRAM_1_VALUE]),
    SensorParam([Device.PKG, Device.DRAM], [1], None, [-1, -1, PKG_1_VALUE, DRAM_1_VALUE]),

    SensorParam(None, [0, 1], [PKG_0_VALUE, DRAM_0_VALUE], [PKG_0_VALUE, DRAM_0_VALUE, PKG_1_VALUE, DRAM_1_VALUE]),
    SensorParam([Device.PKG], [0, 1], [PKG_0_VALUE, -1], [PKG_0_VALUE, -1, PKG_1_VALUE, -1]),
    SensorParam([Device.DRAM], [0, 1], [-1, DRAM_0_VALUE], [-1, DRAM_0_VALUE, -1, DRAM_1_VALUE]),
    SensorParam([Device.PKG, Device.DRAM], [0, 1], [PKG_0_VALUE, DRAM_0_VALUE], [PKG_0_VALUE, DRAM_0_VALUE, PKG_1_VALUE,
                                                                                 DRAM_1_VALUE])
])
def sensor_param_monitor_socket_1(request):
    parameters = request.param
    print('test parameters')
    print('Device list : ' + str(parameters.devices))
    print('socket list : ' + str(parameters.sockets))
    print('one socket result : ' + str(parameters.one_socket_result))
    print('two socket result : ' + str(parameters.two_socket_result))

    return parameters


def test_energy_one_socket(fs_one_socket, sensor_param):
    """
    Create a sensor with given parameters (see printed output) and get energy of monitored devices
    The machine contains only one socket
    Test:
      - return value of the function
    """

    sensor = Sensor(sensor_param.devices, sensor_param.sockets)
    assert sensor.energy() == sensor_param.one_socket_result


def test_energy_two_socket(fs_two_socket, sensor_param):
    """
    Create a sensor with given parameters (see printed output) and get energy of monitored devices
    The machine contains two sockets
    Test:
      - return value of the function
    """
    sensor = Sensor(sensor_param.devices, sensor_param.sockets)
    assert sensor.energy() == sensor_param.two_socket_result


def test_energy_monitor_socket_1_two_socket(fs_two_socket, sensor_param_monitor_socket_1):
    """
    Create a sensor with to monitor package and dram device on socket 1
    use the energy function to get the energy consumption of the monitored devices
    The machine contains two sockets
    Test:
      - return value of the function
    """
    sensor = Sensor(sensor_param_monitor_socket_1.devices, sensor_param_monitor_socket_1.sockets)
    assert sensor.energy() == sensor_param_monitor_socket_1.two_socket_result
