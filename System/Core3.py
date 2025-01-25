from threading import Semaphore
from classes.ReadyQueue import ReadyQueue
from classes.ResourceManager import RealTimeRM
class Core3:
    def __init__(self,ready_queue:ReadyQueue,log,core_sem:Semaphore,system_sem:Semaphore,rm:RealTimeRM):
        self.ready_queue = ready_queue
        self.process =None
        self.log = log
        self.core_sem = core_sem
        self.system_sem = system_sem
        self.resource_manager = rm
        self.priority =None
        self.hard_time =False
        self.hard_allocate =False
        self.second = False
    def do_cycle(self):
        self.check_preempt()
        #Checking for realtime!
        if self.ready_queue.algorithm.check_scheduling():
            self.hard_time=True
        else:
            self.hard_time=False
            if self.hard_allocate:
                self.resource_manager.hard_release()
        #---
        if self.process == None:
            self.priority,self.process=self.ready_queue.get_process()
            if self.process !=None:
                need=self.process.get_resources()
                isAllocated=self.resource_manager.request(need[0],need[1])
                if not isAllocated:
                    raise Exception("Not enough")
                self.process.allocate()
            else:
                self.log[0] = "Running task: idle"
                return
        #Getting resource for two cycles
        if self.hard_time and not self.hard_allocate:
            need = self.process.get_resources()
            self.resource_manager.hard_request(need[0],need[1])
            self.hard_allocate =True
        
        self.process.running()
        end = self.process.do_burst()
        temp = self.process.name
        if end:
            need = self.process.get_resources()
            self.resource_manager.reallocate(need[0],need[1]) 
            self.process.deallocate()
            self.ready_queue.algorithm.update_utility(self.process)
            self.process = None
            
        if self.hard_time and self.hard_allocate and not self.second:
            #Do a cycle again
            self.second=True
            return self.do_cycle()
            
        self.second = False
        self.log[0] = f"Running task: {temp}"

    def check_preempt(self):
        if self.process == None: return
        p = self.priority
        if 0 < len(self.ready_queue.queue) and p > self.ready_queue.queue[0][0]:
            #switch out:
            need=self.process.get_resources()
            self.resource_manager.reallocate(need[0],need[1]) 
            self.process.deallocate()
            self.ready_queue.schedule_process(self.process)
            #switch in:
            self.priority,self.process = self.ready_queue.get_process()
            need=self.process.get_resources()
            self.resource_manager.request(need[0],need[1])
    
    def running(self):
        while True:
            self.core_sem.acquire()
            self.do_cycle()
            self.system_sem.release()