from .SchedulingAlgorithm import SchedulingAlgorithm
from classes.ReadyQueue import ReadyQueue
from queue import PriorityQueue
from classes.Process import PeriodicProcess

class RMS(SchedulingAlgorithm):
    def __init__(self, ready_queue: ReadyQueue):
        self.queue = PriorityQueue()
        ready_queue.queue = self.queue
           
    def choose(self):
        _, process = self.queue.get()
        return process
    
    def schedule(self, p: PeriodicProcess):
        priority = 1 / p.cycle
        self.queue.put((priority, p))