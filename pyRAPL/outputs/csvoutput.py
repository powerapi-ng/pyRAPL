
import os 
from typing import List 
from .output import * 

@Output.register
class CSVOutput: 

    def __init__(self,filename): 
        self.filename=filename
        self.header= ",".join(list(Result.__annotations__.keys())+["socket"]) +"\n"
        self._data=[]

    
    def add(self,result): 
        x=dict(vars(result))
        x['timestamp']=x['timestamp']
        for i in range(len(result.pkg)) :
            x['socket']=i
            x['pkg']=result.pkg[i]
            x['dram']=result.dram[i]
            self._data.append(x.copy())
        
    
    @property
    def data(self) -> List :
        return self._data
    
    def save(self):
        """"
        Save the curent data in a csv file . If the file exists it will append the results in the end and the file otherwise it will create a new file. 
        After saving. the data will be removed from the RAM memeory 
        """
        cond = os.path.exists(self.filename) 
        with open(self.filename ,"a+") as f : 
            if not  cond : 
                f.writelines(self.header)
            for i in self._data : 
                s=",".join([str(j) for j in i.values()]) +"\n"
                f.writelines(s)
        del(self._data)
        self._data=[]

