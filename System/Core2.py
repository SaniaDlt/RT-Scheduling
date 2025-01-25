from threading import Semaphore
from classes.ResourceManager import ResourceManager
class Core2:
    def __init__(self,ready_queue,log,core_num,core_semaphore:Semaphore,
                 system_semaphore:Semaphore,intermediate_core_sem:Semaphore,intermediate_sys_sem:Semaphore
                 ,resource_manager:ResourceManager):
        self.ready_queue = ready_queue
        self.process =None
        self.log = log
        self.core_num = core_num
        self.core_sem = core_semaphore
        self.system_sem = system_semaphore
        self.resource_manager = resource_manager
        self.priority =None
        self.in_core =intermediate_core_sem
        self.in_sys = intermediate_sys_sem
    
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
                self.pulse_sync()
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
            self.log[self.core_num-1] = f"Running task:Idle DeadLock! No resource for the process!"
            self.pulse_sync()
            return
        self.pulse_sync()
        temp = self.process.name
        if end:
            need=self.process.get_resources()
            self.resource_manager.reallocate(need[0],need[1]) 
            self.process.deallocate()
            temp+=" Finished!"
            self.process = None
                
        #Logging
        self.log[self.core_num-1] = f"Running task: {temp}"
        
    def check_preempt(self):
        if self.process == None : return
        p = self.process.burst - self.process.done_bursts 
        if 0 < len(self.ready_queue.queue) and p > self.ready_queue.queue[0][0]:
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

    def pulse_sync(self):
        # Do intermediate step!
        self.in_sys.release()
        self.in_core.acquire()       

