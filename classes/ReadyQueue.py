from algorithms.SchedulingAlgorithm import SchedulingAlgorithm

class ReadyQueue:
    def __init__(self,algorithm:SchedulingAlgorithm):
        self.queue=None
        self.algorithm = algorithm(self)
    
    def get_process(self):
        if not self.queue.empty():
            process = self.algorithm.choose()
            process.running()
    
    def schedule_process(self,p):
        p.ready()
        self.algorithm.schedule(p)