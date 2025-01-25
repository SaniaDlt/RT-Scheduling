from .SchedulingAlgorithm import SchedulingAlgorithm
from classes.ReadyQueue import ReadyQueue
from queue import Queue
from classes.Process import Process

class FCFS(SchedulingAlgorithm):
    def __init__(self, ready_queue: ReadyQueue):
        self.queue = []
        ready_queue.queue = self.queue
        
    def choose(self):
        if 0<len(self.queue):
            process = self.queue.pop(0)
            return process
        return None
    
    def schedule(self, p: Process):
        self.queue.append(p)