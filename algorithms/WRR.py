from .SchedulingAlgorithm import SchedulingAlgorithm
from classes.ReadyQueue import ReadyQueue
import heapq
from classes.Process import Process

class WRR:
    def __init__(self, ready_queue: ReadyQueue):
        self.queue = []
        ready_queue.queue = self.queue
           
    def choose(self):
        if 0<len(self.queue):
            p1,_, process = heapq.heappop(self.queue)
            return p1,process
        return None,None
    
    def schedule(self,first_priority ,p: Process):
        heapq.heappush(self.queue,(first_priority, p.burst, p))