import numpy as np
from enum import Enum
import random
class Process:
    def __init__(self,name:str,burst:int,resources:np.array,arrive:int,processor=1):
        self.name = name
        self.burst = burst
        self.isAllocated =False
        self.need = resources
        self.arrive = arrive
        self.processor_num = processor
        self.done_bursts=0
        self.state = None
        self.count = 0

    def __lt__(self, other):
        return self.burst < other.burst

    def allocate(self):
        self.isAllocated = True
        
    def deallocate(self):
        self.isAllocated = False

    def running(self):
        self.state = State.RUNNING

    def waiting(self):
        self.state = State.WAIT
    
    def ready(self):
        self.state = State.READY
    
    def get_resources(self):
        return self.need
    
    def do_burst(self):
        if self.isAllocated  and self.state== State.RUNNING:
            self.done_bursts+=1
            if self.done_bursts == self.burst:
                return True
            else: return False
        else:
            raise Exception("A process should  be allocated and be in running state")
    
    def __str__(self):
        return f"Name {self.name} needed resource {self.get_resources()} arrive at {self.arrive}"
    def __repr__(self):
        return self.__str__()     

class State(Enum):
    RUNNING=0
    WAIT=2
    READY=1


#Periodic process
class PeriodicProcess(Process):
    def __init__(self, name:str, burst:int, resources, arrive:int,
                 cycle:int,cylce_count:int):
        super().__init__(name, burst, resources, arrive)
        self.cycle = cycle
        self.c_count = cylce_count
    
    def do_burst(self):
        r = super().do_burst()
        if r :
            self.done_bursts =0
        return r
    def __str__(self):
        return f"Name {self.name} needed resource {self.get_resources()} arrive at {self.arrive} cycle {self.cycle}"
    def __repr__(self):
        return self.__str__()   

    

#Dependent process
class DependentProcess(Process):
    def __init__(self, name, burst, resources, arrive,depends_on:str):
        super().__init__(name, burst, resources, arrive)
        self.depend_name = depends_on if depends_on != '-' else None
        self.broke = False

    def do_burst(self):
        self.broke=False
        r = super().do_burst()
        if r:
            rnd = random.random()
            if rnd<=0.3:
                self.done_bursts=0
                self.broke =True
                return False
            return True

    def check_broke(self):
        return self.broke
