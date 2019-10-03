
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


from typing import List,Tupe
from time import time
from pyRAPL import sensor,result 


class Measurement : 
    """
    An object used to record the energy measurement between two instances 
    """
    def __init__(self, label : str ) : 
        self.label = label
        self.a = ()
        self.b = ()
        self.sensor = sensor.Sensor()

    def begin(self): 
        """
        To start recording 
        """
        self.a=[time()] 
        self.a = self.a +  self.sensor.energy()

    def end(self):
        self.b=[time()]
        x=self.sensor.energy() 
        self.d=[j-i for i,j in zip(self.a,self.b)]
        self.b=self.b+x 
        self._results =Result()
        self._results.label = self.label 
        self._results.timestamp=self.a[0]
        self._results.duration=self.d[0]
        self._pkg = self.d[::2] # get odd numbers 
        self._dram = self.d[1::2] # get even numbers 

    def export(self, output): 
        output.add(self._results)

    @property
    def result() -> Result:
        return self._results