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
    def __repr__(self):
        return self.__str__() 

class RealTimeRM(ResourceManager):
    def __init__(self, r1, r2,rm1:ResourceManager,rm2:ResourceManager,rm4:ResourceManager):
        super().__init__(r1, r2)
        self.rm = [rm1,rm4,rm2]
        self.got_sources = [(0,0),(0,0),(0,0)]
    
    def hard_request(self,r1,r2):
        with self.rm[0].lock,self.rm[1].lock,self.rm[2].lock:
            
            for i in range(len(self.rm)):
                if r1==0 and r2==0:
                    return
                r1,r2 = self.check_and_get(r1,r2,i)
            
            raise Exception(f"No resource!!!!!!! Need {r1} {r2}")
    
    def hard_release(self):
        with self.rm[0].lock,self.rm[1].lock,self.rm[2].lock:
            for i in range(len(self.rm)):
                rm = self.rm[i]
                r1,r2 = self.got_sources[i]
                rm.r1+=r1
                rm.r2+=r2
                self.got_sources[i] = (0,0)
    
    def check_and_get(self,r1,r2,indx):
        if self.rm[indx].r1 >= r1:
            self.rm[indx].r1-=r1
            result1=r1
            r1=0
        else:
            r1-=self.rm[indx].r1
            result1 = self.rm[indx].r1
            self.rm[indx].r1=0

        if self.rm[indx].r2 >= r2:
            self.rm[indx].r2-=r2
            result2=r2
            r2=0
        else:
            r2-=self.rm[indx].r2
            result2 = self.rm[indx].r2
            self.rm[indx].r2=0
        self.got_sources[indx] = (result1,result2)
        return r1,r2
    
    def __str__(self):
        with self.lock:
            return f"Resources R1:{self.r1} R2:{self.r2} HardAllocation: { self.got_sources}"

            
        