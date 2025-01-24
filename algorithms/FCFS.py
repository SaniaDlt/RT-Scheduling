from .SchedulingAlgorithm import SchedulingAlgorithm
from classes.ReadyQueue import ReadyQueue
from queue import Queue
from classes.Process import Process

class FCFS(SchedulingAlgorithm):
    def __init__(self, ready_queue: ReadyQueue):
        self.queue = Queue()
        ready_queue.queue = self.queue
        
    def choose(self):
        process = self.queue.get()
        return process
    
    def schedule(self, p: Process):
        self.queue.put(p)