from .SchedulingAlgorithm import SchedulingAlgorithm
from classes.ReadyQueue import ReadyQueue
from queue import PriorityQueue
from classes.Process import Process

class WRR(SchedulingAlgorithm):
    def __init__(self, ready_queue: ReadyQueue):
        self.queue = PriorityQueue()
        ready_queue.queue = self.queue
           
    def choose(self):
        if not self.queue.empty():
            _,_, process = self.queue.get()
            return process
        return None
    
    def schedule(self, p: Process):
        self.queue.put((p.first_priority, p.burst, p))