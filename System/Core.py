from threading import Semaphore

class Core:
    def __init__(self,ready_queue,log,core_num,core_semaphore:Semaphore,system_semaphore:Semaphore):
        self.ready_queue = ready_queue
        self.process =None
        self.log = log
        self.core_num = core_num
        self.core_sem = core_semaphore
        self.system_sem = system_semaphore
    
    def do_cycle(self):
        if self.process == None:
            self.process=self.ready_queue.get_process()
        if self.process != None:
            #TODO check for resources
            
            self.process.running()
            end=self.process.do_burst()
            temp = self.process.name
            if end:
                self.process = None
        else:
            #idle
            temp="idle"
        #Logging
        self.log[self.core_num-1] = f"Running task: {temp}"
        
    
    def running(self):
        while True:
            self.core_sem.acquire()
            self.do_cycle()
            self.system_sem.release()
            

