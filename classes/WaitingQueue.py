from queue import Queue
from .ResourceManager import ResourceManager
from .Process import Process
from threading import Lock
class WaitingQueue:
    def __init__(self, resource: ResourceManager): 
        self.queue = Queue()
        self.resource = resource
        self.lock = Lock()

        
    # def get_process(self):
    #     if not self.queue.empty():
    #         resource_available = self.resource.request(self.resource1, self.resource2)
    #         if resource_available:
    #             return self.queue.get()
    #     return None
    
    def put_process(self, process: Process):
        with self.lock:
            resource_available = self.resource.request(process.need[0], process.need[1])
            if not resource_available:
                process.waiting()
                self.queue.put(process)
                return False
            process.allocate()
            return True
    def __str__(self):
        return f"Waiting Queue {list(self.queue.queue)}"