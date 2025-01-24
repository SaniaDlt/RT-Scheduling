from .SchedulingAlgorithm import SchedulingAlgorithm as interface
from classes.ReadyQueue import ReadyQueue
import heapq
from classes.Process import Process

class SRTF(interface):
    def __init__(self,rqueue:ReadyQueue):
        self.queue = []
        rqueue.queue = self.queue
        
    def choose(self):
        _,process = heapq.heappop(self.queue)
        return _,process

    def schedule(self,p : Process):
        priority = p.burst - p.done_bursts
        heapq.heappush(self.queue, (priority, p))
    
    def schedule_deadlock_case(self,priority,p:Process):
        priority = priority
        heapq.heappush(self.queue,(priority,p))
