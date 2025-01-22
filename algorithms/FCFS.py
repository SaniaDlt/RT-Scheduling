from SchedulingAlgorithm import SchedulingAlgorithm
from classes.ReadyQueue import ReadyQueue
from queue import PriorityQueue
from classes.Process import Process

class FCFS(SchedulingAlgorithm):
    def __init__(self, ready_queue: ReadyQueue):
        self.queue = PriorityQueue()
        ready_queue.queue = self.queue
        
    def choose(self):
        return self.queue.get()
    
    def schedule(self, process: Process):
        self.queue.put(process)