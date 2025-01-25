from .SchedulingAlgorithm import SchedulingAlgorithm
from classes.ReadyQueue import ReadyQueue
import heapq
from classes.Process import PeriodicProcess

class RMS(SchedulingAlgorithm):
    def __init__(self, ready_queue: ReadyQueue):
        self.queue = []
        ready_queue.queue = self.queue
        self.utility =0
           
    def choose(self):
        if 0<len(self.queue):
            _, process = heapq.heappop(self.queue)
            return _,process
        return None,None
    
    def schedule(self, p: PeriodicProcess):
        if p.done_bursts ==0:
            self.utility+=p.burst/p.cycle *100
        priority =  p.cycle
        heapq.heappush(self.queue,(priority, p))
    
    def update_utility(self,process):
        self.utility-=process.burst/process.cycle *100

    def check_scheduling(self):
        n = len(self.queue)
        bound = n*(2**(1/n)-1)*100 if n>0 else 100
        if self.utility >=bound:
            return True
        elif self.utility >= bound:
            raise Exception("Cannot do anything for this one!")
        return False
    