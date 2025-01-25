from classes import ReadyQueue,WaitingQueue,ResourceManager
from threading import Semaphore
class Core4:
    def __init__(self, ready_queue:ReadyQueue.ReadyQueue,
                 waiting_queue:WaitingQueue.WaitingQueue,log:list
                 ,rm:ResourceManager.ResourceManager,
                 core_semaphore:Semaphore,system_semaphore:Semaphore,core_num):
        self.ready_queue = ready_queue
        self.log = log
        self.waiting_queue = waiting_queue
        self.resource_manager = rm
        self.core_sem = core_semaphore
        self.system_sem = system_semaphore
        self.process=None
        self.core_num = core_num
        self.map = {}
    
    def do_cylce(self):
        #Getting a porcess
        if self.process == None:
            self.process = self.ready_queue.get_process()
            if self.process == None:
                self.log[self.core_num-1] = "Running task: idle"
                return
            

        self.process.running()
        #Check dependency
        if not self.process.depend_name in self.map.keys():
            self.waiting_queue.queue.put(self.process)
            self.log[self.core_num-1] = "Running task: idle Depends on something!"
            self.process =None
            return

        isAllocated = self.waiting_queue.put_process(self.process)
        if not isAllocated:
            self.log[self.core_num-1] = "Running task: idle Not enought resource"
            self.process =None
            return
        
        end =self.process.do_burst()
        temp = self.process.name
        self.quantom-=1
        if end:
            self.quantom=0
            need = self.process.get_resources()
            self.resource_manager.reallocate(need[0],need[1])
            self.process.deallocate()
            self.map[temp]=True
            self.process =None
            temp+=" Finished!"
            self.squash_waiting()

        if self.process.check_broke():
            temp+=" Task Broken! Should run again"
        
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
            self.do_cylce()
            self.system_sem.release()