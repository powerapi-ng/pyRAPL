import pandas 
import time 


from .output import * 

@Output.register
class DataFrameOutput: 

    def __init__(self): 
        self._data =None 
        self._data =  pandas.DataFrame(columns=list(Result.__annotations__.keys())+["socket"])

    
    def add(self,result): 
        x=dict(vars(result))
        x['timestamp']=time.ctime(x['timestamp'])
        for i in range(len(result.pkg)) :
            x['socket']=i
            x['pkg']=result.pkg[i]
            x['dram']=result.dram[i]
            self._data=self._data.append(x,ignore_index=True)
    
    @property
    def data(self) -> pandas.DataFrame:
        return self._data