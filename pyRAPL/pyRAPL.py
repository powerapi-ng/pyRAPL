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
import psutil


class PyRAPLException(Exception):
    """Parent class of all PyRAPL exception
    """


class PyRAPLNoEnergyConsumptionRecordedException(PyRAPLException):
    """Exception raised when a function get_record_*_result is executed without stoping consumption recording before
    """


class PyRAPLNoEnergyConsumptionRecordStartedException(PyRAPLException):
    """Exception raised when a function stop_record_* is executed without starting consumption recording before"""


class PyRAPLCantRecordDRAMEnergyConsumption(PyRAPLException):
    """Exception raised when starting recording DRAM power consumption but no power consumption metric is available for
    the DRAM device
    """


class PyRAPLCantRecordPKGEnergyConsumption(PyRAPLException):
    """Exception raised when starting recording package power consumption but no power consumption metric is available
    for the package device
    """


class PyRAPL:
    """
    singleton that force the execution of the running process on a uniq package and retrieve package power consumption
    """
    instance = None
    already_init = False

    def __init__(self):
        self.dram_file = None
        self.pkg_file = None
        self.package_id = None
        self.siblings_cpu = None

        self.dram_begin_measure = None
        self.dram_end_measure = None

        self.pkg_begin_measure = None
        self.pkg_end_measure = None

        self.pkg_started = False
        self.dram_started = False

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
        return the cpus that are on the same physical package that the cpu0
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
        force the execution of the current process on the cpu given as parameter
        :param cpu_list list: list of cpu id (int) where the current process can be executed
        """
        current_process = psutil.Process()
        current_process.cpu_affinity(cpu_list)

    @staticmethod
    def _get_package_id():
        """
        return physical package id of the cpu0
        :return int:
        """
        f = open('/sys/devices/system/cpu/cpu0/topology/physical_package_id')
        s = f.readline()
        return int(s)

    def _open_rapl_files(self, package_id):
        """
        open the files corresponding to rapl kernel output for the corresponding package id
        :param int package_id: package id corresponding
        """
        pkg_dir_name, pkg_rapl_id = self._get_pkg_directory_name(package_id)
        if pkg_dir_name is None:
            self.pkg_file = None
            self.dram_file = None
            return
        self.pkg_file = open(pkg_dir_name + '/energy_uj', 'r')

        dram_dir_name = self._get_dram_directory_name(pkg_dir_name, pkg_rapl_id)
        if dram_dir_name is None:
            self.dram_file = None
            return

        self.dram_file = open(dram_dir_name + '/energy_uj', 'r')

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

    def get_energy_pkg(self):
        """
        return the amount of consumed energy by the cpu package since last CPU reset
        :return int: the amount of consumed energy since last CPU reset in mJ
        :raise PyRAPLCantRecordPKGEnergyConsumption: if no energy consumtion metric is available for package&
        """
        if self.pkg_file is None:
            raise PyRAPLCantRecordPKGEnergyConsumption

        self.pkg_file.seek(0, 0)
        return int(self.pkg_file.readline())

    def start_record_energy_pkg(self):
        """
        start recording the power consumption of the cpu package
        :raise PyRAPLCantRecordPKGEnergyConsumption: if no energy consumtion metric is available for package
        """
        self.pkg_begin_measure = self.get_energy_pkg()
        self.pkg_started = True

    def stop_record_energy_pkg(self):
        """
        stop recording the power consumption of the cpu package
        :raise PyRAPLNoEnergyConsumptionRecordStartedException: if no energy consumtion metric is available for package
        """
        if not self.pkg_started:
            raise PyRAPLNoEnergyConsumptionRecordStartedException

        self.pkg_end_measure = self.get_energy_pkg()
        self.pkg_started = False

    def get_record_pkg_result(self):
        """
        get the latest energy consumption recorded by PyRAPL for cpu package
        :return: energy consumed between the last start_record_energy_pkg() and stop_record_energy_pkg() in mJ
        :raise PyRAPLNoEnergyConsumptionRecordedException: if no energy consumption was recorded
        """
        if self.pkg_begin_measure is None or self.pkg_end_measure is None:
            raise PyRAPLNoEnergyConsumptionRecordedException
        return self.pkg_end_measure - self.pkg_begin_measure

    def start_record_energy_dram(self):
        """
        start recording the power consumption of the dram
        :raise PyRAPLCantRecordDRAMEnergyConsumption: if no energy consumtion metric is available for dram
        """
        self.dram_begin_measure = self.get_energy_dram()
        self.dram_started = True

    def stop_record_energy_dram(self):
        """
        stop recording the power consumption of the cpu dram
        :raise PyRAPLNoEnergyConsumptionRecordStartedException: if no energy consumtion metric is available for package
        """
        if not self.dram_started:
            raise PyRAPLNoEnergyConsumptionRecordStartedException

        self.dram_end_measure = self.get_energy_dram()
        self.dram_started = False

    def get_record_dram_result(self):
        """
        get the latest energy consumption recorded by PyRAPL for dram
        :return: energy consumed between the last start_record_energy_dram() and stop_record_energy_dram() in mJ
        :raise PyRAPLNoEnergyConsumptionRecordedException: if no energy consumption was recorded
        """
        if self.dram_begin_measure is None or self.dram_end_measure is None:
            raise PyRAPLNoEnergyConsumptionRecordedException
        return self.dram_end_measure - self.dram_begin_measure

    def get_energy_dram(self):
        """
        return the amount of consumed energy by the cpu dram since last CPU reset
        :return int: the amount of consumed energy since last CPU reset in mJ
        :raise PyRAPLCantRecordDRAMEnergyConsumption: if no energy consumtion metric is available for dram
        """
        if self.dram_file is None:
            raise PyRAPLCantRecordDRAMEnergyConsumption

        self.dram_file.seek(0, 0)
        return int(self.dram_file.readline())
