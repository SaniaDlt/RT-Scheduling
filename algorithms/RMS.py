from .SchedulingAlgorithm import SchedulingAlgorithm
from classes.ReadyQueue import ReadyQueue
import heapq
from classes.Process import PeriodicProcess

class RMS(SchedulingAlgorithm):
    def __init__(self, ready_queue: ReadyQueue):
        self.queue = []
        ready_queue.queue = self.queue
           
    def choose(self):
        _, process = heapq.heappop(self.queue)
        return process
    
    def schedule(self, p: PeriodicProcess):
        priority = 1 / p.cycle
        heapq.heappush(self.queue,(priority, p))
    
    def check_scheduling(self):
        pass
    