import numpy as np
from enum import Enum

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
        #TODO print the process!
        #Contains ending time
        #Cointains waiting time
        # Contain the core number
        pass

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

#Dependent process
class DependentProcess(Process):
    def __init__(self, name, burst, resources, arrive,depends_on:str):
        super().__init__(name, burst, resources, arrive)
        self.depend_name = depends_on

        