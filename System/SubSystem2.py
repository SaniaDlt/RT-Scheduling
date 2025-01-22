from classes.ReadyQueue import ReadyQueue
from algorithms.SRTF import SRTF
from Core import Core
from threading import Semaphore,Thread
from inputs import intrupt_handler
from classes.ResourceManager import ResourceManager

class SubSystem2:
    def __init__(self,timestamp,resources:ResourceManager,log_low,mainsystem_sem:Semaphore,system_sem:Semaphore):
        self.timestamp = timestamp
        self.ready_queue = ReadyQueue(SRTF)
        self.system_sem = Semaphore(0)
        self.core_sem = Semaphore(0)
        self.resources = resources
        self.log_low = log_low
        self.main_system_sem = mainsystem_sem
        self.my_sem = system_sem
        self.log_up = [0 for i in range(2)]
        self.core1 = Core(self.ready_queue,self.log_up,1,self.core_sem,self.system_sem)
        self.core2 = Core(self.ready_queue,self.log_up,2,self.core_sem,self.system_sem)
        self.time = 0
    
    def intrupt_hander(self):
        event = intrupt_handler(self.timestamp,self.time)
        if event != None:
            for p in event:
                priority = p.burst
                p.ready()
                self.ready_queue.put((priority,p))
        self.time+=1
    
    def running(self):
        # TODO log to upper system
        core1 = Thread(self.core1.running)
        core2 = Thread(self.core2.running)
        core1.start()
        core2.start()
        while True:
            self.my_sem.acquire()
            #Starting new time
            self.intrupt_hander()
            #Sync cores
            self.core_sem.release(2)

            self.system_sem.acquire()
            self.system_sem.acquire()
            self.main_system_sem.release()




