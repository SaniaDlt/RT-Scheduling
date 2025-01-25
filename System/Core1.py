from classes import ReadyQueue,WaitingQueue,ResourceManager
from threading import Semaphore
class Core1:
    def __init__(self, ready_queue:ReadyQueue.ReadyQueue,
                 waiting_queue:WaitingQueue.WaitingQueue,log:list
                 ,rm:ResourceManager.ResourceManager,
                 core_semaphore:Semaphore,system_semaphore:Semaphore,intermediate_core:Semaphore,intermediate_system:Semaphore,core_num):
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
        self.in_core = intermediate_core
        self.in_sys = intermediate_system
        self.t=1

    
    def do_cylce(self):
        #Getting a porcess
        self.log[self.core_num-1]=""
        if self.process == None:
            self.priority,self.process = self.ready_queue.get_process()
            
            if self.priority == None:
                self.log[self.core_num-1] = "Running task: idle"
                self.pulse_sync()
                return
            elif self.priority == self.first_priority:
                self.quantom = self.process.burst // self.min_burst
            else:
                #Changing a round
                self.squash_waiting()
                self.min_burst = self.process.burst
                self.quantom=1
                self.first_priority = self.priority      
        self.process.ready()
        if not self.process.isAllocated:
            isAllocated = self.waiting_queue.put_process(self.process)
            if not isAllocated:
                self.process =None
                self.priority =None
                self.log[self.core_num-1] = "Running task: idle Not enought resource"
                self.pulse_sync()
                return
            self.process.allocate()
        self.process.running()
        end =self.process.do_burst(self.t)
        self.pulse_sync()
        #To sync the running pulse
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
            self.do_cylce()
            self.t+=1
            self.system_sem.release()

    def pulse_sync(self):
        # Do intermediate step!
        self.in_sys.release()
        self.in_core.acquire()
            