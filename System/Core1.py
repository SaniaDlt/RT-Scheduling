from classes import ReadyQueue,WaitingQueue,ResourceManager
from threading import Semaphore
class Core1:
    def __init__(self, ready_queue:ReadyQueue.ReadyQueue,
                 waiting_queue:WaitingQueue.WaitingQueue,log:list
                 ,rm:ResourceManager.ResourceManager,
                 core_semaphore:Semaphore,system_semaphore:Semaphore,core_num):
        self.ready_queue = ready_queue
        self.log = log
        self.first_priority = -1
        self.waiting_queue = waiting_queue
        self.resource_manager = rm
        self.core_sem = core_semaphore
        self.system_sem = system_semaphore
        self.quantom = None
        self.process=None
        self.priority=None
        self.core_num = core_num
        self.min_burst=None
    
    def do_cylce(self):
        #Getting a porcess
        if self.process == None:
            self.priority,self.process = self.ready_queue.get_process()
            if self.priority == None:
                self.log[self.core_num-1] = "Running task: idle"
                return
            elif self.priority == self.first_priority:
                self.quantom = self.process.burst // self.min_burst
            else:
                #Changing a round
                self.squash_waiting()
                self.min_burst = self.process.burst
                self.quantom=1
                self.first_priority = self.priority

        self.process.running()
        isAllocated = self.waiting_queue.put_process(self.process)
        if not isAllocated:
            self.log[self.core_num-1] = "Running task: idle Not enought resource"
            return
        end =self.process.do_burst()
        temp = self.process.name
        self.quantom-=1
        if end:
            self.quantom=0
            need = self.process.get_resources()
            self.resource_manager.reallocate(need[0],need[1])
            self.process.deallocate()
            self.process =None
            temp+=" Finished!"
        if self.quantom==0 and not end:
            #Deallocate
            need = self.process.get_resources()
            self.resource_manager.reallocate(need[0],need[1])
            self.process.deallocate()
            #Schedule it
            self.ready_queue.algorithm.schedule(self.first_priority+1,self.process)
            self.process =None
        
        self.log[self.core_num-1] = f"Running task: {temp}"
    #For load balance    
    def squash_waiting(self):
        queue=self.waiting_queue.queue
        while not queue.empty():
            p = queue.get()
            self.ready_queue.algorithm.schedule(self.first_priority+1,p)

    def running(self):
        while True:
            self.core_sem.acquire()
            self.do_cycle()
            self.system_sem.release()
    