# MIT License

# Copyright (c) 2018, INRIA
# Copyright (c) 2018, University of Lille
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
import logging
try:
    import psutil
except ImportError:
    logging.getLogger().info("psutil is not installed.")


from enum import Enum

class Device(Enum):
    PKG = 1
    DRAM = 2
    GPU = 3


class PyRAPLException(Exception):
    """Parent class of all PyRAPL exception
    """


class PyRAPLNoEnergyConsumptionRecordedException(PyRAPLException):
    """Exception raised when a function recorded_energy() is executed without stoping consumption recording before
    """


class PyRAPLNoEnergyConsumptionRecordStartedException(PyRAPLException):
    """Exception raised when a function stop() is executed without starting consumption recording before"""


class PyRAPLCantRecordEnergyConsumption(PyRAPLException):
    """Exception raised when starting recording power consumption for a device but no power consumption metric is
    available for this device
    """
    def __init__(self, device):
        PyRAPLException.__init__(self)
        self.device = device


class PyRAPL:
    """
    singleton that force the execution of the running process on a unique package and retrieve package power consumption
    """
    instance = None
    already_init = False

    def __init__(self):
        self.sys_api = {
            Device.PKG: None,
            Device.DRAM: None,
            Device.GPU: None
        }
        self.is_record_running = {
            Device.PKG: False,
            Device.DRAM: False,
            Device.GPU: False
        }
        self.measure = {
            Device.PKG: [None, None],
            Device.DRAM: [None, None],
            Device.GPU: [None, None]
        }
        self.package_id = None
        self.siblings_cpu = None

        if self.already_init is False:
            self.already_init = True
            self._uniq_init()

    def _uniq_init(self):
        """
        Initialize the PyRAPL tool
        """
        self.siblings_cpu = PyRAPL._get_siblings_cpu()
        self.package_id = PyRAPL._get_package_id()
        PyRAPL._force_cpu_execution_on(self.siblings_cpu)
        self._open_rapl_files(self.package_id)

    @staticmethod
    def _get_siblings_cpu():
        """
        return the CPUs that are on the same physical package that the CPU0
        :return list:
        """
        f = open('/sys/devices/system/cpu/cpu0/topology/core_siblings_list')
        s = f.readline()

        if '-' in s:
            [first, last] = list(map(int, s.split('-')))
            return list(range(first, last + 1))
        else:
            return list(map(int, s.split(',')))

    @staticmethod
    def _force_cpu_execution_on(cpu_list):
        """
        force the execution of the current process on the CPU given as parameter
        :param cpu_list list: list of CPU id (int) where the current process can be executed
        """
        current_process = psutil.Process()
        current_process.cpu_affinity(cpu_list)

    @staticmethod
    def _get_package_id():
        """
        return physical package id of the CPU0
        :return int:
        """
        f = open('/sys/devices/system/cpu/cpu0/topology/physical_package_id')
        s = f.readline()
        return int(s)

    def _open_rapl_files(self, package_id):
        """
        open the files corresponding to rapl kernel output for the corresponding package id
        :param int package_id: corresponding package id
        """
        pkg_dir_name, pkg_rapl_id = self._get_pkg_directory_name(package_id)
        if pkg_dir_name is None:
            self.sys_api[Device.PKG] = None
            self.sys_api[Device.DRAM] = None
            return
        self.sys_api[Device.PKG] = open(pkg_dir_name + '/energy_uj', 'r')

        dram_dir_name = self._get_dram_directory_name(pkg_dir_name, pkg_rapl_id)
        if dram_dir_name is None:
            self.sys_api[Device.DRAM] = None
            return

        self.sys_api[Device.DRAM] = open(dram_dir_name + '/energy_uj', 'r')

    def _get_pkg_directory_name(self, package_id):
        """
        :return (str, int): directory name, rapl_id
        """
        rapl_id = 0
        while os.path.exists('/sys/class/powercap/intel-rapl/intel-rapl:' + str(rapl_id)):
            dirname = '/sys/class/powercap/intel-rapl/intel-rapl:' + str(rapl_id)
            f = open(dirname + '/name', 'r')
            if f.readline() == 'package-' + str(package_id) + '\n':
                return dirname, rapl_id
            else:
                rapl_id += 1
        return None, None

    def _get_dram_directory_name(self, pkg_directory_name, rapl_id):
        sub_id = 0
        while os.path.exists(pkg_directory_name + '/intel-rapl:' + str(rapl_id) + ':' + str(sub_id)):
            dirname = pkg_directory_name + '/intel-rapl:' + str(rapl_id) + ':' + str(sub_id)
            f = open(dirname + '/name', 'r')
            if f.readline() == 'dram\n':
                return dirname
            else:
                sub_id += 1
        return None

    def __new__(cls):
        """use only one instance of PyRAPL"""
        if cls.instance is None:
            cls.instance = object.__new__(cls)
        return cls.instance

    def energy(self, device):
        """
        return the amount of consumed energy by the device given in parameter since last CPU reset
        :param Device device: the device to get the power consumption
        :return int: the amount of consumed energy of the device since last CPU reset in mJ
        :raise PyRAPLCantRecordEnergyConsumption: if no energy consumtion metric is available for the given device
        :raise TypeError: if device is not a Device parameter
        """
        if not isinstance(device, Device):
            raise TypeError()
        if self.sys_api[device] is None:
            raise PyRAPLCantRecordEnergyConsumption(device)

        api_file = self.sys_api[device]
        api_file.seek(0, 0)
        return int(api_file.readline())

    def record(self, devices):
        """
        start recording the power consumption of the given devices
        :param [Device] devices: list of device to record the power consumption
        :raise PyRAPLCantRecordEnergyConsumption: if no energy consumtion metric is available for the given device
        :raise TypeError: if a device in devices list is not a Device parameter
        """
        for device in devices:
            energy = self.energy(device)
            self.measure[device][0] = energy
            self.is_record_running[device] = True

    def stop(self):
        """
        stop recording the power consumption
        :raise PyRAPLNoEnergyConsumptionRecordStartedException: if no power consumption recording was started
        """
        energy_recorded = False

        for device, is_running in self.is_record_running.items():
            if is_running:
                energy_recorded = True
                self.is_record_running[device] = False
                self.measure[device][1] = self.energy(device)

        if not energy_recorded:
            raise PyRAPLNoEnergyConsumptionRecordStartedException()


    def recorded_energy(self, device):
        """
        get the latest energy consumption recorded by PyRAPL for the given device
        :return: energy (in mJ) consumed between the last record() and stop() function call
        :raise PyRAPLNoEnergyConsumptionRecordedException: if no energy consumption was recorded
        :raise TypeError: if device is not a Device parameter
        """
        if not isinstance(device, Device):
            raise TypeError()

        if self.measure[device][0] is None or self.measure[device][1] is None:
            raise PyRAPLNoEnergyConsumptionRecordedException

        measure = self.measure[device][1] - self.measure[device][0]
        self.measure[device][0] = None
        self.measure[device][1] = None

        return measure
