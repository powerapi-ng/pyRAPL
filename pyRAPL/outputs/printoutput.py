
from ..outputs import * 

@Output.register
class PrintOutput: 
    """
        Implementation of the Abstract class Output that print the results 
    """

    def add (self,result:Result): 
        def print_energy(energy): 
            s=""
            for i in range(len(energy)):
                s=s+f"\n\tsocket {i} : {energy[i]: 10.4}"
            return s 

        s=f"""
        Lable : {result.label} 
        Begin : {time.ctime(result.timestamp)} 
        Duration : {result.duration} s
        -------------------------------
        PKG : {print_energy(result.pkg)}
        -------------------------------
        DRAM : {print_energy(result.dram)}
        -------------------------------
        """ 
        print(s)

