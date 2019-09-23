import pyRAPL
from time import sleep
from sys import argv
def fun (n):
    sleep(n)

if __name__=="__main__":
    n = int(argv[1]) if len(argv) >1 else 5 
    sensor = pyRAPL.PyRAPL()
    sensor.record([pyRAPL.Device.PKG, pyRAPL.Device.DRAM])
    fun(n)
    sensor.stop()
    energy_pkg = sensor.recorded_energy(pyRAPL.Device.PKG)
    energy_dram = sensor.recorded_energy(pyRAPL.Device.DRAM)
    print("Energy PKG: %f , Energy DRAM: %f"%(energy_pkg,energy_dram))
