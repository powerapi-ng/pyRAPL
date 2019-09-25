import pytest
import pyfakefs
import psutil

from mock import patch, Mock

from pyRAPL import PyRAPL, Device, measure, Measure, PyRAPLCantRecordEnergyConsumption
from pyRAPL import PyRAPLNoEnergyConsumptionRecordedException, PyRAPLNoEnergyConsumptionRecordStartedException

psutil.Process = Mock()

@pytest.fixture
def base_fs(fs):
    """
    create a basic file system containing only processor informations
    """
    fs.create_file('/sys/devices/system/cpu/cpu0/topology/core_siblings_list', contents='0\n')
    fs.create_file('/sys/devices/system/cpu/cpu0/topology/physical_package_id', contents='0\n')
    return fs


@pytest.fixture
def rapl_fs(base_fs):
    """
    create a file system containing energy metric for package 0 and 1
    """
    base_fs.create_file('/sys/class/powercap/intel-rapl/intel-rapl:0/name', contents='package-0\n')
    base_fs.create_file('/sys/class/powercap/intel-rapl/intel-rapl:0/energy_uj', contents='12345\n')

    base_fs.create_file('/sys/class/powercap/intel-rapl/intel-rapl:1/name', contents='package-1\n')
    base_fs.create_file('/sys/class/powercap/intel-rapl/intel-rapl:1/energy_uj', contents='12345\n')
    return base_fs


@pytest.fixture
def rapl_fs_with_core(rapl_fs):
    """
    add to rapl_fs a energy metric for package 0 core
    """
    rapl_fs.create_file('/sys/class/powercap/intel-rapl/intel-rapl:0/intel-rapl:0:0/name', contents='core\n')
    rapl_fs.create_file('/sys/class/powercap/intel-rapl/intel-rapl:0/intel-rapl:0:0/energy_uj', contents='12345\n')
    return rapl_fs


@pytest.fixture
def rapl_fs_with_dram(rapl_fs_with_core):
    """
    add to rapl_fs_with_core a energy metric for package 0 dram
    """
    rapl_fs_with_core.create_file('/sys/class/powercap/intel-rapl/intel-rapl:0/intel-rapl:0:1/name', contents='dram\n')
    rapl_fs_with_core.create_file('/sys/class/powercap/intel-rapl/intel-rapl:0/intel-rapl:0:1/energy_uj',
                                  contents='54321\n')
    return rapl_fs_with_core


@pytest.fixture
def mocked_pyRAPL():
    """
    return a PyRAPL instance with mocked psutils function
    """
    PyRAPL._instance = None
    PyRAPL._aldready_init = False
    pyrapl = PyRAPL()
    yield pyrapl
    PyRAPL._instance = None
    PyRAPL._aldready_init = False

#############
# INIT TEST #
#############
@patch('pyRAPL.pyRAPL.PyRAPL._uniq_init')
@patch('psutil.Process')
def test_uniq_init_executed_once(mock1, mock2):
    """
    Create two instance of PyRAPL

    Test if :
      - the _uniq_init function was only executed once
    """
    i1 = PyRAPL()
    i2 = PyRAPL()

    assert PyRAPL._uniq_init.call_count == 1


def test_get_siblings_cpu_simple_list(fs):
    """
    create a /sys/devices/system/cpu/cpu0/topology/core_siblings_list file that contains the following value :
    1,2,3,20
    use the PyRAPL._get_siblings_cpu to retrieve sibling cpu of cpu0

    Test if :
      - the function return the list [1,2,3,20]
    """
    fs.create_file('/sys/devices/system/cpu/cpu0/topology/core_siblings_list', contents='1,2,3,20\n')
    assert PyRAPL._get_siblings_cpu() == [1, 2, 3, 20]


def test_get_siblings_cpu_interval_id(fs):
    """
    create a /sys/devices/system/cpu/cpu0/topology/core_siblings_list file that contains the following value :
    1-3
    use the PyRAPL._get_siblings_cpu to retrieve sibling cpu of cpu0

    Test if :
      - the function return the list [1,2,3]
    """
    fs.create_file('/sys/devices/system/cpu/cpu0/topology/core_siblings_list', contents='1-3\n')
    assert PyRAPL._get_siblings_cpu() == [1, 2, 3]


def test_get_package_id(fs):
    """
    create a /sys/devices/system/cpu/cpu0/topology/physical_package_id file that contains the following value :
    9
    use the PyRAPL._get_package_id to retrieve the package id of cpu0

    Test if :
      - the function return 9
    """
    fs.create_file('/sys/devices/system/cpu/cpu0/topology/physical_package_id', contents='9\n')
    assert PyRAPL._get_package_id() == 9


def test_open_rapl_files_no_file(base_fs, mocked_pyRAPL):
    """
    create an instance of pyRAPL and run its _open_rapl_files on a fake filesystem with no rapl files

    Test if:
      - no file for package metric was found
      - no file for dram metric was found
    """
    assert mocked_pyRAPL._sys_api[Device.PKG] is None
    assert mocked_pyRAPL._sys_api[Device.DRAM] is None


def test_open_rapl_files_simple(rapl_fs, mocked_pyRAPL):
    """
    create an instance of pyRAPL and run its _open_rapl_files on the fake filesystem rapl_fs to open files containing
    energy consumption metric about package 0

    Test if:
      - the file /sys/class/powercap/intel-rapl/intel-rapl:0/energy_uj was open by the PyRAPL instance
      - no file for dram metric was found
    """
    assert mocked_pyRAPL._sys_api[Device.PKG] is not None

    assert mocked_pyRAPL._sys_api[Device.DRAM] is None
    assert mocked_pyRAPL._sys_api[Device.PKG].name == '/sys/class/powercap/intel-rapl/intel-rapl:0/energy_uj'


def test_open_rapl_files_simple_pkg1(rapl_fs, mocked_pyRAPL):
    """
    create an instance of pyRAPL and run its _open_rapl_files on the fake filesystem rapl_fs to open files containing
    energy consumption metric about package 1

    Test if:
      - the file /sys/class/powercap/intel-rapl/intel-rapl:1/energy_uj was open by the PyRAPL instance
      - no file for dram metric was found
    """
    mocked_pyRAPL._open_rapl_files(1)
    assert mocked_pyRAPL._sys_api[Device.PKG] is not None

    assert mocked_pyRAPL._sys_api[Device.DRAM] is None
    assert mocked_pyRAPL._sys_api[Device.PKG].name == '/sys/class/powercap/intel-rapl/intel-rapl:1/energy_uj'


def test_open_rapl_files_with_core(rapl_fs_with_core, mocked_pyRAPL):
    """
    create an instance of pyRAPL and run its _open_rapl_files on the fake filesystem rapl_fs_with_core to open files
    containing energy consumption metric about package 0

    Test if:
      - the file /sys/class/powercap/intel-rapl/intel-rapl:0/energy_uj was open by the PyRAPL instance
      - no file for dram metric was found
    """
    assert mocked_pyRAPL._sys_api[Device.PKG] is not None

    assert mocked_pyRAPL._sys_api[Device.DRAM] is None
    assert mocked_pyRAPL._sys_api[Device.PKG].name == '/sys/class/powercap/intel-rapl/intel-rapl:0/energy_uj'


def test_open_rapl_files_with_dram(rapl_fs_with_dram, mocked_pyRAPL):
    """
    create an instance of pyRAPL and run its _open_rapl_files on the fake filesystem rapl_fs_with_core to open files
    containing energy consumption metric about package 0

    Test if:
      - the file /sys/class/powercap/intel-rapl/intel-rapl:0/energy_uj was open by the PyRAPL instance
      - the file /sys/class/powercap/intel-rapl/intel-rapl:0/intel-rapl:0:1/energy_uj was open by the PyRAPL instance
    """
    assert mocked_pyRAPL._sys_api[Device.DRAM] is not None
    assert mocked_pyRAPL._sys_api[Device.PKG] is not None

    assert mocked_pyRAPL._sys_api[Device.DRAM].name == '/sys/class/powercap/intel-rapl/intel-rapl:0/intel-rapl:0:1/energy_uj'
    assert mocked_pyRAPL._sys_api[Device.PKG].name == '/sys/class/powercap/intel-rapl/intel-rapl:0/energy_uj'


#######################
# GET PACKAGE ENERGY  #
#######################
def test_get_energy_pkg_no_file(base_fs, mocked_pyRAPL):
    """
    try to get a the amount of energy consumed by the cpu package in a machine with no rapl sensor

    create an instance of PyRAPL with the filesystem base_fs and run the energy function

    Test if:
      - a PyRAPLCantRecordEnergyConsumption is raise
    """
    with pytest.raises(PyRAPLCantRecordEnergyConsumption):
        mocked_pyRAPL.energy(Device.PKG)


def test_get_energy_bad_type_device_device(rapl_fs, mocked_pyRAPL):
    """
    call the PyRAPL.energy function with a non Device argument

    Test if:
      - A TypeError is raise
    """
    with pytest.raises(TypeError):
        mocked_pyRAPL.energy(5)

def test_energy(rapl_fs, mocked_pyRAPL):
    """
    try to get a the amount of energy consumed by the cpu package

    create an instance of PyRAPL with the filesystem rapl_fs and run the energy function

    Test if:
      - the returned value is an int and is greater than 0
    """
    val = mocked_pyRAPL.energy(Device.PKG)
    assert isinstance(val, float)
    assert val > 0


###########################
# START RECORDING ENERGY  #
###########################
def test_start_record_energy_pkg_without_rapl(base_fs, mocked_pyRAPL):
    """
    try to start cpu package energy consumtpion recording in a machine with no rapl sensor

    create an instance of PyRAPL with the file system base_fs and run the start_record_energy_pkg function

    Test if:
      - a PyRAPLCantRecordEnergyConsumption is raise
    """
    with pytest.raises(PyRAPLCantRecordEnergyConsumption):
        mocked_pyRAPL.record(Device.PKG)



def test_record_bad_type_device(rapl_fs, mocked_pyRAPL):
    """
    call the PyRAPL.record function with non Device parameter

    Test if:
      - A TypeError is raise
    """
    with pytest.raises(TypeError):
        mocked_pyRAPL.record(Device.PKG, 5)


def test_start_record_energy_pkg(rapl_fs, mocked_pyRAPL):
    """
    try to start cpu package energy consumtpion recording

    create an instance of PyRAPL with the file system base_fs and run the start_record_energy_pkg function

    Test if:
      - before runing the function the _measure[Device.PKG][0] attribute is None and is_record_running[Device.PKG] is
        False
      - the _measure[Device.PKG][0] attribute is not None and is_record_running[Device.PKG] is True
    """
    assert mocked_pyRAPL._measure[Device.PKG][0] is None
    assert mocked_pyRAPL._is_record_running[Device.PKG] is False
    mocked_pyRAPL.record(Device.PKG)
    assert mocked_pyRAPL._measure[Device.PKG][0] is not None
    assert mocked_pyRAPL._is_record_running[Device.PKG] is True


def test_start_record_energy_pkg_and_dram(rapl_fs_with_dram, mocked_pyRAPL):
    """
    try to start cpu package and dram energy consumtpion recording

    create an instance of PyRAPL with the file system base_fs and run the record function

    Test if:
      - before runing the function the _measure[Device.PKG][0] attribute is None
      - the _measure[Device.PKG][0] attribute is not None
    """
    assert mocked_pyRAPL._measure[Device.PKG][0] is None
    assert mocked_pyRAPL._measure[Device.DRAM][0] is None
    mocked_pyRAPL.record(Device.PKG, Device.DRAM)
    assert mocked_pyRAPL._measure[Device.PKG][0] is not None
    assert mocked_pyRAPL._measure[Device.DRAM][0] is not None

def test_start_record_energy_all(rapl_fs_with_dram, mocked_pyRAPL):
    """
    try to start all energy consumtpion recording 

    create an instance of PyRAPL with the file system base_fs and run the record function

    Test if:
      - before runing the function the _measure[Device.PKG][0] and _measure[Device.DRAM][0] attribute is None
      - the _measure[Device.PKG][0] and _measure[Device.DRAM][0] attribute is not None
    """
    assert mocked_pyRAPL._measure[Device.PKG][0] is None
    assert mocked_pyRAPL._measure[Device.DRAM][0] is None
    mocked_pyRAPL.record()
    assert mocked_pyRAPL._measure[Device.PKG][0] is not None
    assert mocked_pyRAPL._measure[Device.DRAM][0] is not None


def test_start_record_energy_all(rapl_fs, mocked_pyRAPL):
    """
    try to start all energy consumtpion recording in a file system without dram

    create an instance of PyRAPL with the file system base_fs and run the record function

    Test if:
      - before runing the function the _measure[Device.PKG][0] and _measure[Device.DRAM][0] attribute is None
      - the _measure[Device.PKG][0] attribute is not None
      - the _measure[Device.PKG][0] attribute is None
    """
    assert mocked_pyRAPL._measure[Device.PKG][0] is None
    assert mocked_pyRAPL._measure[Device.DRAM][0] is None
    mocked_pyRAPL.record()
    assert mocked_pyRAPL._measure[Device.PKG][0] is not None
    assert mocked_pyRAPL._measure[Device.DRAM][0] is None

##################################
# STOP RECORDING PACKAGE ENERGY  #
##################################
def test_stop_record_energy_pkg_without_start_recording(rapl_fs, mocked_pyRAPL):
    """
    try to stop cpu package energy consumtpion without starting recordin

    create an instance of PyRAPL with the file system base_fs and run the stop_record_energy_pkg function

    Test if:
      - a PyRAPLNoEnergyConsumptionRecordStartedException is raise
    """
    with pytest.raises(PyRAPLNoEnergyConsumptionRecordStartedException):
        mocked_pyRAPL.stop()


def test_stop_record_energy_pkg(rapl_fs, mocked_pyRAPL):
    """
    try to stop cpu package energy consumtpion recording

    create an instance of PyRAPL with the file system base_fs and run the start_record_energy_pkg and the
    stop_record_energy_pkg functions

    Test if:
      - before runing the function the _measure[Device.PKG][1] attribute is None and is_record_running[Device.PKG] is
        True
      - the _measure[Device.PKG][1] attribute is not None and is_record_running[Device.PKG] is False
    """
    mocked_pyRAPL.record(Device.PKG)

    assert mocked_pyRAPL._measure[Device.PKG][1] is None
    assert mocked_pyRAPL._is_record_running[Device.PKG] is True
    mocked_pyRAPL.stop()
    assert mocked_pyRAPL._measure[Device.PKG][1] is not None
    assert mocked_pyRAPL._is_record_running[Device.PKG] is False

################################
# GET RECORDED PACKAGE ENERGY  #
################################
def test_get_record_pkg_result_without_measure(rapl_fs, mocked_pyRAPL):
    """
    try to get cpu package energy consumtpion without starting recording

    create an instance of PyRAPL with the file system base_fs and run the get_record_pkg_result function

    Test if:
      - a PyRAPLNoEnergyConsumptionRecordedException is raise
    """
    with pytest.raises(PyRAPLNoEnergyConsumptionRecordedException):
        mocked_pyRAPL.recorded_energy(Device.PKG)


def test_get_recorded_energy_bad_type_device(rapl_fs, mocked_pyRAPL):
    """
    call the PyRAPL.recorded_energy function with a non Device argument

    Test if:
      - A TypeError is raise
    """
    with pytest.raises(TypeError):
        mocked_pyRAPL.recorded_energy(5)


def test_get_recorded_energy_bad_type_device_list(rapl_fs, mocked_pyRAPL):
    """
    call the PyRAPL.recorded_energy function with a non Device argument and a Device argument

    Test if:
      - A TypeError is raise
    """
    mocked_pyRAPL.record(Device.PKG)
    mocked_pyRAPL.stop()
    with pytest.raises(TypeError):
        mocked_pyRAPL.recorded_energy(Device.PKG, 5)


def test_get_record_energy_pkg(rapl_fs, mocked_pyRAPL):
    """
    try to get cpu package energy consumtpion recording result

    create an instance of PyRAPL with the file system base_fs and run the record function and the
    stop functions after that, run the recorded_energy function with Device.PKG parameter

    Test if:
      - the returned value is a dictionary
      - the dictionary contains the recorded energy consumption measure for package
    """
    mocked_pyRAPL.record(Device.PKG)
    mocked_pyRAPL.stop()
    correct_value = mocked_pyRAPL._measure[Device.PKG][1] - mocked_pyRAPL._measure[Device.PKG][0]
    val = mocked_pyRAPL.recorded_energy(Device.PKG)
    assert isinstance(val, dict)
    assert Device.PKG in val
    assert val[Device.PKG] == correct_value


def test_get_record_energy_all(rapl_fs_with_dram, mocked_pyRAPL):
    """
    try to get all the recorded energy consumtpion recording result

    create an instance of PyRAPL with the file system base_fs and run the record function and the
    stop functions after that, run the recorded_energy function

    Test if:
      - the returned value is a dictionary
      - the dictionary contains the recorded energy consumption measure for package and dram
    """
    mocked_pyRAPL.record()
    mocked_pyRAPL.stop()
    correct_value = {
        Device.PKG: mocked_pyRAPL._measure[Device.PKG][1] - mocked_pyRAPL._measure[Device.PKG][0],
        Device.DRAM: mocked_pyRAPL._measure[Device.DRAM][1] - mocked_pyRAPL._measure[Device.DRAM][0]
    }
    result = mocked_pyRAPL.recorded_energy()
    assert isinstance(result, dict)
    for device in [Device.PKG, Device.DRAM]:
        assert device in result
        assert result[Device.PKG] == correct_value[device]


def test_get_record_energy_dram_pkg(rapl_fs_with_dram, mocked_pyRAPL):
    """
    try to get dram and package energy consumtpion recording result

    create an instance of PyRAPL with the file system base_fs and run the record function and the
    stop functions after that, run the recorded_energy function

    Test if:
      - the returned value is a dictionary
      - the dictionary contains the recorded energy consumption measure for package and dram
    """
    mocked_pyRAPL.record(Device.PKG, Device.DRAM)
    mocked_pyRAPL.stop()
    correct_value = {
        Device.PKG: mocked_pyRAPL._measure[Device.PKG][1] - mocked_pyRAPL._measure[Device.PKG][0],
        Device.DRAM: mocked_pyRAPL._measure[Device.DRAM][1] - mocked_pyRAPL._measure[Device.DRAM][0]
    }
    result = mocked_pyRAPL.recorded_energy(Device.PKG, Device.DRAM)
    assert isinstance(result, dict)
    for device in [Device.PKG, Device.DRAM]:
        assert device in result
        assert result[Device.PKG] == correct_value[device]


##############
# DECORATEUR #
##############
def test_function_return_value(rapl_fs):
    """
    test if the decorated function return a value
    """
    @measure
    def fun():
        return 1

    assert fun() == 1

def test_use_parameter(rapl_fs):
    """
    decorate a function that take a parameter and return it

    Test if:
      - the given parameter are returned by the decorated function
    """
    @measure
    def fun(a):
        return a

    arg = 3
    assert fun(arg) == arg


def test_use_two_parameter(rapl_fs):
    """
    decorate a function that take two parameter and return them

    Test if:
      - the given parameters are returned by the decorated function
    """
    @measure
    def fun(a, b):
        return (a, b)

    arg1 = 3
    arg2 = 7
    assert fun(arg1, arg2) == (arg1, arg2)


def test_use_positional_parameter(rapl_fs):
    """
    decorate a function that take positional parameter and return them

    Test if:
      - the given parameters are returned by the decorated function
    """
    @measure
    def fun(*a):
        return a

    arg1 = 3
    arg2 = 7
    assert fun(arg1, arg2) == (arg1, arg2)


def test_use_mutable_parameter(rapl_fs):
    """
    decorate a function that take mutable parameter and modify it

    Test if:
      - the given parameter is changed
    """
    class Mutable:
        def __init__(self, val):
            self.val = val

    @measure
    def fun(mut):
        mut.val = 0

    mut = Mutable(5)
    assert mut.val == 5
    fun(mut)
    assert mut.val == 0


def test_param_decorator_monitor_pkg(rapl_fs_with_dram, mocked_pyRAPL):
    """
    decorate a function to monitor package power consumption

    Test if:
      - the result only contains package power consumption the ellipsed time and the functio name
    """
    class Res:
        def __init__(self):
            self.res = None

    result = Res()
    def handler(res):
        result.res = res

    @measure(devices=Device.PKG, handler=handler)
    def fun():
        return None

    fun()
    assert len(result.res.data) == 2
    assert 'PKG' in result.res.data
    assert 'TIME' in result.res.data
    assert result.res.function_name == fun.__name__


def test_param_decorator_monitor_pkg_dram(rapl_fs_with_dram, mocked_pyRAPL):
    """
    decorate a function to monitor package and dram power consumption

    Test if:
      - the result only contains package and dram power consumption, the ellipsed time and the functio name
    """
    class Res:
        def __init__(self):
            self.res = None

    result = Res()
    def handler(res):
        result.res = res

    @measure(devices=[Device.PKG, Device.DRAM], handler=handler)
    def fun():
        return None

    fun()
    assert len(result.res.data) == 3
    assert 'PKG' in result.res.data
    assert 'DRAM' in result.res.data
    assert 'TIME' in result.res.data
    assert result.res.function_name == fun.__name__


def test_param_decorator_monitor_all(rapl_fs_with_dram, mocked_pyRAPL):
    """
    decorate a function to monitor all power consumption

    Test if:
      - the result only contains package and dram power consumption, the ellipsed time and the functio name
    """
    class Res:
        def __init__(self):
            self.res = None

    result = Res()
    def handler(res):
        result.res = res

    @measure(handler=handler)
    def fun():
        return None

    fun()
    assert len(result.res.data) == 3
    assert 'PKG' in result.res.data
    assert 'DRAM' in result.res.data
    assert 'TIME' in result.res.data
    assert result.res.function_name == fun.__name__


def test_handler_call(rapl_fs, mocked_pyRAPL):
    """
    decorate a function an use a mocked handler to handle the measures

    Test if:
      - The mocked handle function is called with a Measure parameter
    """
    mocked_handler = Mock()
    @measure(handler=mocked_handler)
    def fun():
        return None

    assert mocked_handler.call_count == 0

    fun()

    assert mocked_handler.call_count == 1
    assert isinstance(mocked_handler.call_args[0][0], Measure)


@patch('builtins.print')
def test_handler_call(mocked_print, rapl_fs, mocked_pyRAPL):
    """
    decorate a function an use a the default handler

    Test if:
      - the print function was called
    """
    @measure()
    def fun():
        return None

    assert mocked_print.call_count == 0

    fun()

    assert mocked_print.call_count == 3
