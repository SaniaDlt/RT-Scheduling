# from algorithms.SchedulingAlgorithm import SchedulingAlgorithm

class ReadyQueue:
    def __init__(self,algorithm_class):
        self.queue=None
        self.algorithm = algorithm_class(self)
    
    def get_process(self):
        if not self.queue.empty():
            process = self.algorithm.choose()
            return process
        return None
    
    def schedule_process(self,p):
        p.ready()
        self.algorithm.schedule(p)
    
    def __str__(self):
        return f"Ready Queue: {self.queue}"