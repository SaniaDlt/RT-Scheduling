# from algorithms.SchedulingAlgorithm import SchedulingAlgorithm

class ReadyQueue:
    def __init__(self,algorithm_class):
        self.queue=None
        self.algorithm = algorithm_class(self)
    
    def get_process(self):
        process = self.algorithm.choose()
        return process
        
    
    def schedule_process(self,p):
        p.ready()
        self.algorithm.schedule(p)
    
    def __str__(self):
        return f"Ready Queue: {self.queue}"