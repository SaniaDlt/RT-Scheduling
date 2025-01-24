from threading import Lock

class ResourceManager:
    def __init__(self,r1,r2):
        self.r1=r1
        self.r2=r2
        self.lock = Lock()
    
    def request(self,r1,r2):
        with self.lock:
            if self.r1 >= r1 and self.r2 >= r2:
                self.r1-=r1
                self.r2-=r2
                return True
            else:
                return False
    
    def reallocate(self,r1,r2):
        with self.lock:
            self.r1+=r1
            self.r2+=r2
    
    def __str__(self):
        with self.lock:
            return f"Resources R1:{self.r1} R2:{self.r2}"
        