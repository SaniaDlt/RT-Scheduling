import numpy as np

class Process:
    def __init__(self,name:str,burst:int,resources:np.array,arrive:int,processor=1):
        self.name = name
        self.burst = burst
        self.allocation = (0,0)
        self.need = resources
        self.arrive = arrive
        self.processor_num = processor

    def allocate(self,resource:tuple):
        if self.need < resource : raise Exception("A proccess cannot get more that it wanted")
        self.need = self.need - resource
        self.allocation = self.allocate + resource
        #TODO create banker algorithm for each core
        return
#Periodic process
class PeriodicProcess(Process):
    def __init__(self, name:str, burst:int, resources, arrive:int,
                 cycle:int,cylce_count:int):
        super().__init__(name, burst, resources, arrive)
        self.cycle = cycle
        self.c_count = cylce_count

#Dependent process
class DependentProcess(Process):
    def __init__(self, name, burst, resources, arrive,depends_on:str):
        super().__init__(name, burst, resources, arrive)
        self.depend_name = depends_on

        