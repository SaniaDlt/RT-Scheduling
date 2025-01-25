from classes.ResourceManager import ResourceManager
from threading import Semaphore,Thread
from classes.ReadyQueue import ReadyQueue
from classes.WaitingQueue import WaitingQueue
from algorithms.FCFS import FCFS
from .Core4 import Core4
from inputs import intrupt_handler

class SubSystem4:
    def __init__(self,timestamp,resources:ResourceManager,
                 log_low,mainsystem_sem:Semaphore,system_sem:Semaphore):
        self.timestamp = timestamp
        self.waiting_queue = WaitingQueue(resources)
        self.ready_queue = ReadyQueue(FCFS)
        self.system_sem = Semaphore(0)
        self.core_sem = [Semaphore(0),Semaphore(0)]
        self.in_sys = Semaphore(0)
        self.in_core = [Semaphore(0),Semaphore(0)]
        self.resources = resources
        self.log_low = log_low
        self.main_system_sem = mainsystem_sem
        self.my_sem = system_sem
        self.log_up = [0 for i in range(2)]
        
        self.cores = [
            Core4(self.ready_queue,self.waiting_queue,self.log_up,resources,self.core_sem[0],
                  self.system_sem,self.in_core[0],self.in_sys,1),
            Core4(self.ready_queue,self.waiting_queue,self.log_up,resources,self.core_sem[1],self.system_sem,
                  self.in_core[1],self.in_sys,2),

        ]
        self.time = 0
    
    def intrupt_hander(self):
        event = intrupt_handler(self.timestamp,self.time)
        if event != None:
            for p in event:
                p.ready()
                self.ready_queue.schedule_process(p)
        self.time+=1
    
    def running(self):
        for c in self.cores:
            Thread(target=c.running).start()

        while True:
            self.my_sem.acquire()
            #Starting new time
            self.intrupt_hander()
            #Sync cores
            self.core_sem[0].release()
            self.core_sem[1].release()
            self.inter_mediate_sync()
            self.system_sem.acquire()
            self.system_sem.acquire()
            #After cores
            self.concat_message()
            self.main_system_sem.release()
    
    def inter_mediate_sync(self):
        #Intermediate step
        self.in_sys.acquire()
        self.in_sys.acquire()
        self.in_core[0].release()
        self.in_core[1].release()
        #Ending work
    
    def concat_message(self):
        result = f"Sub4\n {self.resources}\n{self.waiting_queue}\n{self.ready_queue}\n"
        i=1
        for m in self.log_up:
            result+=f"Core {i}:\n"
            result+=m+"\n"
            i+=1
        self.log_low[3]= result