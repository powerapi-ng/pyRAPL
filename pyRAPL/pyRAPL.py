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
import logging
import time
import functools

from enum import Enum

try:
    import psutil
except ImportError:
    logging.getLogger().info("psutil is not installed.")


class Device(Enum):
    PKG = 1
    DRAM = 2
    GPU = 3


class PyRAPL:
    """
    singleton that force the execution of the running process on a unique package and retrieve package power consumption
    """
    _instance = None
    _already_init = False

    def __new__(cls):
        """use only one instance of PyRAPL"""
        if cls._instance is None:
            cls._instance = object.__new__(cls)
        return cls._instance

    def __init__(self, pin_process=False):

        self._is_record_running = {
            Device.PKG: False,
            Device.DRAM: False,
            Device.GPU: False
        }
        self._measure = {
            Device.PKG: [None, None],
            Device.DRAM: [None, None],
            Device.GPU: [None, None]
        }
        self._package_id = None
        self._siblings_cpu = None
        self.pin_process = pin_process

        if self._already_init is False:
            self._already_init = True
            self._uniq_init()

    def _uniq_init(self):
        """
        Initialize the PyRAPL tool
        """
        self._sys_api = {
            Device.PKG: None,
            Device.DRAM: None,
            Device.GPU: None
        }

        if self.pin_process:
            self._siblings_cpu = PyRAPL._get_siblings_cpu()
            self._package_id = PyRAPL._get_package_id()
            PyRAPL._force_cpu_execution_on(self._siblings_cpu)

        self._open_rapl_files(self._package_id)



    def _open_rapl_files(self, package_id):
        """
        open the files corresponding to rapl kernel output for the corresponding package id
        :param int package_id: corresponding package id
        """
        pkg_dir_name, pkg_rapl_id = self._get_pkg_directory_name(package_id)
        if pkg_dir_name is None:
            self._sys_api[Device.PKG] = None
            self._sys_api[Device.DRAM] = None
            return
        self._sys_api[Device.PKG] = open(pkg_dir_name + '/energy_uj', 'r')

        dram_dir_name = self._get_dram_directory_name(pkg_dir_name, pkg_rapl_id)
        if dram_dir_name is None:
            self._sys_api[Device.DRAM] = None
            return

        self._sys_api[Device.DRAM] = open(dram_dir_name + '/energy_uj', 'r')

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

    def energy(self, device):
        """
        return the amount of consumed energy by the device given in parameter since last CPU reset
        :param Device device: the device to get the power consumption
        :return float: the amount of consumed energy of the device since last CPU reset in J
        :raise PyRAPLCantRecordEnergyConsumption: if no energy consumtion metric is available for the given device
        :raise TypeError: if device is not a Device instance
        """

        if not isinstance(device, Device):
            raise TypeError()

        if self._sys_api[device] is None:
            raise PyRAPLCantRecordEnergyConsumption(device)

        api_file = self._sys_api[device]
        api_file.seek(0, 0)
        return int(api_file.readline())/1000000

    def _begin_record(self, device):
        energy = self.energy(device)
        self._measure[device][0] = energy
        self._is_record_running[device] = True

    def record(self, *devices):
        """
        start recording the power consumption of the given devices
        :param [Device] devices: list of device to record the power consumption
        :raise PyRAPLCantRecordEnergyConsumption: if no energy consumtion metric is available for the given device
        :raise TypeError: if a device in devices list is not a Device instance
        """
        if devices:
            for device in devices:
                self._begin_record(device)
        else:
            for device, api_file in self._sys_api.items():
                if api_file:
                    self._begin_record(device)

    def stop(self):
        """
        stop recording the power consumption
        :raise PyRAPLNoEnergyConsumptionRecordStartedException: if no power consumption recording was started
        """
        energy_recorded = False

        for device, is_running in self._is_record_running.items():
            if is_running:
                energy_recorded = True
                self._is_record_running[device] = False
                self._measure[device][1] = self.energy(device)

        if not energy_recorded:
            raise PyRAPLNoEnergyConsumptionRecordStartedException()

    def _compute_recorded_energy(self, device):

        recorded_energy =  (self._measure[device][1] - self._measure[device][0])
        # print("yolo")
        self._measure[device][0] = None
        self._measure[device][1] = None
        return recorded_energy

    def recorded_energy(self, *devices):
        """
        get the latest energy consumption recorded by PyRAPL for the given device
        :return: energy (in J) consumed between the last record() and stop() function call
        :raise PyRAPLNoEnergyConsumptionRecordedException: if no energy consumption was recorded
        :raise TypeError: if device is not a Device instance
        """
        measures = {}
        if devices:
            for device in devices:
                if not isinstance(device, Device):
                    raise TypeError()

                if self._measure[device][0] is None or self._measure[device][1] is None:
                    raise PyRAPLNoEnergyConsumptionRecordedException

                measures[device] = self._compute_recorded_energy(device)

            return measures
        else:
            for device in self._measure:
                # print("dev {}, dev[0] {} ,dev[1] {}".format(dev,self.measure[dev][0],self.measure[dev][1]) )
                if self._measure[device][0] and self._measure[device][1]:
                    measures[device] = self._compute_recorded_energy(device)
            if measures:
                return measures
            else:
                raise PyRAPLNoEnergyConsumptionRecordedException


class Measure:
    def __init__(self, function_name, data):
        self.function_name = function_name
        self.data = data


def measure(_func=None, *, devices=None, handler=None):
    """ a decorator to measure the energy consumption of a function recorded by PyRAPL
    :param [Device] devices: the list of devices to monitor by pyrapl
    :param function(measure) handler: traitement of the results recorded from pyrapl
    """

    def default_handler(measures):
        print(f"measures got from the function {measures.function_name } :")
        for mes, val in measures.data.items():
            print(f"{mes } : {val:.4}")

    def decorator_measure_energy(func):
        @functools.wraps(func)
        def wrapper_measure(*args, **kwargs):
            sensor = PyRAPL()
            sensor.record(*devices)
            t1 = time.perf_counter()
            val = func(*args, **kwargs)
            t2 = time.perf_counter()
            sensor.stop()

            data = {
                device._name_: mes for device, mes in sensor.recorded_energy(*devices).items()
            }
            data['TIME'] = t2 - t1

            handle(Measure(func.__name__, data))
            return val
        return wrapper_measure

    # measure.sensor=PyRAPL() # to make an instance only one time
    if not isinstance(devices, list):
        devices = [devices] if devices else []

    handle = default_handler if handler is None else handler

    if _func is None:
        # to ensure the working system when you call it with parameters or without parameters
        return decorator_measure_energy
    else:
        return decorator_measure_energy(_func)
