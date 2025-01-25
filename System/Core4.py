from classes import ReadyQueue,WaitingQueue,ResourceManager
from threading import Semaphore
class Core4:
    def __init__(self, ready_queue:ReadyQueue.ReadyQueue,
                 waiting_queue:WaitingQueue.WaitingQueue,log:list
                 ,rm:ResourceManager.ResourceManager,
                 core_semaphore:Semaphore,system_semaphore:Semaphore,
                 intermediate_core_sem:Semaphore,intermediate_sys_sem:Semaphore,core_num,dones):
        self.ready_queue = ready_queue
        self.log = log
        self.waiting_queue = waiting_queue
        self.resource_manager = rm
        self.core_sem = core_semaphore
        self.system_sem = system_semaphore
        self.process=None
        self.core_num = core_num
        self.dones =dones
        self.in_core =intermediate_core_sem
        self.in_sys = intermediate_sys_sem
        self.t=1
    def do_cylce(self):
        #Getting a porcess
        if self.process == None:
            self.process = self.ready_queue.get_process()
            if self.process == None:
                self.log[self.core_num-1] = "Running task: idle"
                self.pulse_sync()
                return
            

        self.process.running()
        #Check dependency
        if self.process.depend_name != None and not self.process.depend_name in self.dones :
            self.waiting_queue.queue.put(self.process)
            self.log[self.core_num-1] = "Running task: idle Depends on something!"
            self.process =None
            self.pulse_sync()
            return
        if not self.process.isAllocated:
            isAllocated = self.waiting_queue.put_process(self.process)
            if not isAllocated:
                self.log[self.core_num-1] = "Running task: idle Not enought resource"
                self.process =None
                self.pulse_sync()
                return
            self.process.allocate()
            
        end =self.process.do_burst(self.t)
        self.pulse_sync()
        temp = self.process.name
        if end:
            need = self.process.get_resources()
            self.resource_manager.reallocate(need[0],need[1])
            self.process.deallocate()
            self.dones.append(temp)
            self.process =None
            temp+=" Finished!"
            self.squash_waiting()
            self.log[self.core_num-1] = f"Running task: {temp}"
            return

        if self.process.check_broke():
            temp+=" Task Broken! Should run again"
        
        self.log[self.core_num-1] = f"Running task: {temp}"
    #For load balance    
    def squash_waiting(self):
        queue=self.waiting_queue.queue
        while not queue.empty():
            p = queue.get()
            self.ready_queue.schedule_process(p)

    def running(self):
        while True:
            self.core_sem.acquire()
            self.do_cylce()
            self.t+=1
            self.system_sem.release()
    
    def pulse_sync(self):
        # Do intermediate step!
        self.in_sys.release()
        self.in_core.acquire()     