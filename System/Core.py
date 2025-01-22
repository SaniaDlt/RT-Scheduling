from threading import Semaphore
from classes.ResourceManager import ResourceManager
class Core:
    def __init__(self,ready_queue,log,core_num,core_semaphore:Semaphore,system_semaphore:Semaphore,resource_manager:ResourceManager):
        self.ready_queue = ready_queue
        self.process =None
        self.log = log
        self.core_num = core_num
        self.core_sem = core_semaphore
        self.system_sem = system_semaphore
        self.resource_manager = resource_manager
        self.priority =None
    
    def do_cycle(self):
        self.check_preempt()
        if self.process == None:
            self.priority,self.process=self.ready_queue.get_process()
            if self.process !=None:
                need=self.process.get_resources()
                isAllocated=self.resource_manager.request(need[0],need[1])
                if isAllocated:
                    self.process.allocate()
            else:
                self.log[self.core_num-1] = "Running task: idle"
                return
        
        
        self.process.running()
        try:
            end=self.process.do_burst()
        except Exception as e:
            # Case that we dont not allocate resource to the process
            #Using invert againg!
            self.priority+=1
            self.ready_queue.algorithm.schedule_deadlock_case(self.priority,self.process)
            self.process =None
            self.priority =None
            #----
            self.log[self.core_num-1] = f"Running task: DeadLock! No resource for the process!"
            return
        temp = self.process.name
        if end:
            need=self.process.get_resources()
            self.resource_manager.reallocate(need[0],need[1]) 
            self.process.deallocate()
            self.process = None
                
        #Logging
        self.log[self.core_num-1] = f"Running task: {temp}"
        
    def check_preempt(self):
        p = self.process.burst - self.process.done_bursts 
        if p > self.ready_queue.queue[0][0]:
            #switch out:
            need=self.process.get_resources()
            self.resource_manager.reallocate(need[0],need[1]) 
            self.process.deallocate()
            self.ready_queue.schedule_process(self.process)
            #switch in:
            self.priority,self.process = self.ready_queue.get_process()
            need=self.process.get_resources()
            isAllocated=self.resource_manager.request(need[0],need[1])
            if isAllocated:
                self.process.allocate()


    def running(self):
        while True:
            self.core_sem.acquire()
            self.do_cycle()
            self.system_sem.release()
            

