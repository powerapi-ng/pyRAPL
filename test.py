import pyRAPL
# from pyRAPL import measure 
# from pyRAPL import measure_energy
from time import sleep
from sys import argv




@pyRAPL.measure
def fun(n):
    sleep(n)

@pyRAPL.measure(devices=pyRAPL.Device.TIME)
def fun2(n):
    sleep(2*n)



def main1():
    n = int(argv[1]) if len(argv) >1 else 5 
    sensor = pyRAPL.PyRAPL()
    sensor.record([pyRAPL.Device.PKG, pyRAPL.Device.DRAM])
    sleep(n)
    sensor.stop()
    # energy_pkg = sensor.recorded_energy(pyRAPL.Device.PKG)
    # energy_dram = sensor.recorded_energy(pyRAPL.Device.DRAM)
    # print("Energy PKG: %f , Energy DRAM: %f"%(energy_pkg,energy_dram))
    print(sensor.recorded_energy())
    sensor = pyRAPL.PyRAPL()
    sensor.record([pyRAPL.Device.PKG, pyRAPL.Device.DRAM])
    sleep(n)
    sensor.stop()
    # energy_pkg = sensor.recorded_energy(pyRAPL.Device.PKG)
    # energy_dram = sensor.recorded_energy(pyRAPL.Device.DRAM)
    # print("Energy PKG: %f , Energy DRAM: %f"%(energy_pkg,energy_dram))
    print(sensor.recorded_energy())


def main2():
    n = int(argv[1]) if len(argv) >1 else 5 
    fun2(n)
    print("fin f2")
    fun(n)
    print("fin f1")
    _,measures=fun(n)

    print(_)
    print(measures[pyRAPL.Device.DRAM])

if __name__=="__main__":
    main2()
