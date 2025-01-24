from queue import Queue
from .ResourceManager import ResourceManager
from .Process import Process

class WaitingQueue:
    def __init__(self, resource: ResourceManager): 
        self.queue = Queue()
        self.queue.pop
        self.resource = resource

        
    # def get_process(self):
    #     if not self.queue.empty():
    #         resource_available = self.resource.request(self.resource1, self.resource2)
    #         if resource_available:
    #             return self.queue.get()
    #     return None
    
    def put_process(self, process: Process):
        if process.ready():
            resource_available = self.resource.request(process.resources[0], process.resources[1])
            if not resource_available:
                process.waiting()
                self.queue.put(process)
                return False
            process.allocate()
            return True