from classes.ReadyQueue import ReadyQueue
from algorithms.RMS import RMS
from .Core3 import Core3
from threading import Semaphore,Thread
from inputs import intrupt_handler
from classes.ResourceManager import RealTimeRM

class SubSystem3:
    def __init__(self,timestamp,resources:RealTimeRM,log_low,mainsystem_sem:Semaphore,system_sem:Semaphore):
        self.timestamp = timestamp
        self.ready_queue = ReadyQueue(RMS)
        self.system_sem = Semaphore(0)
        self.core_sem = Semaphore(0)
        self.resources = resources
        self.log_low = log_low
        self.main_system_sem = mainsystem_sem
        self.my_sem = system_sem
        self.log_up = [0 for i in range(1)]
        self.core = Core3(self.ready_queue,self.log_up,self.core_sem,self.system_sem,self.resources)
        self.time = 0
    
    def intrupt_hander(self):
        event = intrupt_handler(self.timestamp,self.time)
        if event != None:
            for p in event:   
                p.ready()
                self.ready_queue.schedule_process(p)
        self.time+=1
    
    def running(self):
        core = Thread(target=self.core.running)
        core.start()

        while True:
            self.my_sem.acquire()
            #Starting new time
            self.intrupt_hander()
            #Sync cores
            self.core_sem.release()

            self.system_sem.acquire()
            #After cores
            self.concat_message()
            self.main_system_sem.release()

    def concat_message(self):
        result = f"Sub3\n {self.resources}\n{self.ready_queue}\n"
        i=1
        for m in self.log_up:
            result+=f"Core {i}:\n"
            result+=m+"\n"
            i+=1
        self.log_low[2]= result




