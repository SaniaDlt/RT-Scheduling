from .SchedulingAlgorithm import SchedulingAlgorithm as interface
from classes.ReadyQueue import ReadyQueue
from queue import PriorityQueue
from classes.Process import Process

class SRTF(interface):
    def __init__(self,rqueue:ReadyQueue):
        self.queue = PriorityQueue()
        rqueue.queue = self.queue
        
    def choose(self):
        _,process = self.queue.get()
        return process

    def schedule(self,p : Process):
        priority = p.burst - p.done_bursts
        self.queue.put((priority,p))
