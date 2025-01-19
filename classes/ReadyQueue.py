from algorithms.SchedulingAlgorithm import SchedulingAlgorithm

class ReadyQueue:
    def __init__(self,algorithm:SchedulingAlgorithm):
        self.algorithm = algorithm(self)