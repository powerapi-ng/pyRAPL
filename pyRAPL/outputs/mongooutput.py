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




from typing import List
import asyncio



import pymongo 

from pyRAPL import Result
from pyRAPL.outputs import Output

@Output.register
class MongoOutput:
        
    def __init__(self,serveraddr, serverport,database,collection):
        """
        export the results to a collection in a mongo database 

        """
        self._client = pymongo.MongoClient(serveraddr, serverport)
        self._db=self._client[database]
        self._collection = self._db[collection]
        # self.header = ",".join(list(Result.__annotations__.keys()) + ["socket"]) + "\n"
        self._data = []

    def add(self,result):
        x = dict(vars(result))
        x['timestamp'] = x['timestamp']
        for i in range(len(result.pkg)):
            x['socket'] = i
            x['pkg'] = result.pkg[i]
            x['dram'] = result.dram[i]
            self._data.append(x.copy())

    @property
    def data(self) -> List:
        return self._data
    
    def save(self):
        """"
        save data into a mongo database 
        After saving. the data will be removed from the RAM memeory
        """
        self._collection.insert_many(self.data)
        del self._data
        self._data = []
