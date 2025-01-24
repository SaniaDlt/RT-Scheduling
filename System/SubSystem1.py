from classes.ResourceManager import ResourceManager
from threading import Semaphore,Thread
from classes.ReadyQueue import ReadyQueue
from classes.WaitingQueue import WaitingQueue
from algorithms.WRR import WRR
from .Core1 import Core1
from inputs import intrupt_handler
import heapq

class SubSystem1:
    def __init__(self,timestamp,resources:ResourceManager,
                 log_low,mainsystem_sem:Semaphore,system_sem:Semaphore):
        self.timestamp = timestamp
        self.waiting_queue = WaitingQueue(resources)
        self.ready_queue = [ReadyQueue(WRR),ReadyQueue(WRR),ReadyQueue(WRR)]
        self.system_sem = Semaphore(0)
        self.core_sem = Semaphore(0)
        self.resources = resources
        self.log_low = log_low
        self.main_system_sem = mainsystem_sem
        self.my_sem = system_sem
        self.log_up = [0 for i in range(3)]
        self.tresh=3
        
        self.cores = [
            Core1(self.ready_queue[0],self.waiting_queue,self.log_up,resources,self.core_sem,self.system_sem,1),
            Core1(self.ready_queue[1],self.waiting_queue,self.log_up,resources,self.core_sem,self.system_sem,2),
            Core1(self.ready_queue[2],self.waiting_queue,self.log_up,resources,self.core_sem,self.system_sem,3)
        ]
        self.time = 0
    
    def intrupt_hander(self):
        event = intrupt_handler(self.timestamp,self.time)
        if event != None:
            for p in event:
                p.ready()
                self._push(p.process_num-1,p)
        self.time+=1
    
    def running(self):
        for c in self.cores:
            Thread(target=c.do_cylce).start()

        while True:
            self.my_sem.acquire()
            #Starting new time
            self.intrupt_hander()
            self.load_balance()
            #Sync cores
            self.core_sem.release(3)

            self.system_sem.acquire()
            self.system_sem.acquire()
            self.system_sem.acquire()
            #After cores
            self.concat_message()
            self.main_system_sem.release()
    
    def load_balance(self):
        len1 = len(self.ready_queue[0].queue)
        len2 = len(self.ready_queue[1].queue)
        len3 = len(self.ready_queue[2].queue)
        if abs(len1-len2) <=self.tresh and abs(len2-len3) <= self.tresh and abs(len1-len3) <=self.tresh:
            return # It means everything is done! 
        
        if abs(len1 - len2) > self.tresh:
            diffrence = abs(len1-len2)//2
            max_queue = 0 if len1>len2 else 1
            min_queue = 1 if max_queue==0 else 0
        elif abs(len2-len3) > self.tresh:
            diffrence = abs(len2-len3)//2
            max_queue = 1 if len1>len2 else 2
            min_queue = 1 if max_queue==2 else 2
        else:
            diffrence = abs(len1-len3)//2
            max_queue = 0 if len1>len3 else 2
            min_queue = 2 if max_queue==0 else 0
        #pop and push
        for i in range(diffrence):
            least_priority_process =self._pop(max_queue)
            self._push(min_queue,least_priority_process)
        return self.load_balance()

    def _push(self,process_num,p):
        priority = self.cores[process_num].first_priority +1
        self.ready_queue[process_num].algorithm.schedule(self,priority,p)

    def _pop(self,process_num):
        heap = self.ready_queue[process_num].queue
        _,_,least_process = max(heap)
        heap.remove(least_process)
        heapq.heapify(heap)
        return least_process

    
    def concat_message(self):
        result = f"Sub1\n {self.resources}\n{self.waiting_queue}\n"
        i=1
        for m in self.log_up:
            result+=f"Core {i}:\n"
            result+=f"{self.ready_queue[i-1]}"+"\n"
            result+=m+"\n"
            i+=1
        self.log_low[0]= result