

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



import abc

from pyRAPL import Result


class Output(abc.ABC):
    """
    Abstract class that represent an output handler for the Measurement class 
    """ 

    @abc.abstractmethod
    def add(self,result:Result):
        """
            Handle the object Results 
        """
        pass
    #

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
        Begin : {result.timestamp} 
        Duration : {result.duration} s
        -------------------------------
        PKG : {print_energy(result.pkg)}
        -------------------------------
        DRAM : {print_energy(result.dram)}
        -------------------------------
        """ 
        print(s)

