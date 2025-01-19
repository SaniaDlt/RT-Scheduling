import numpy as np

class Banker:
    def __init__(self,process_num:int,resource_num:int,max:np.array):
        self.allocation = np.zeros((process_num,resource_num),dtype=np.int32)
        self.need = np.zeros((process_num,resource_num),dtype=np.int32)
        self.max = max
        self.available = np.sum(max,axis=0,dtype=np.int32)
        self.process_num = process_num
        self.resource_num = resource_num
    
    def check_safty(self):
        need = self.need
        allocation = self.allocation
        work = self.available.copy()
        finish =np.array([False for i in range(self.process_num)])
        
        sequence = []
        free_resource = np.zeros(self.resource_num,dtype=np.int32)

        i=0
        while i< self.process_num:
            multi_porcess = []
            free_resource *=0
            j=0
            while j < self.process_num:
                if not finish[j] and np.all(need[j]<=work):
                    finish[j]=True
                    free_resource+=allocation[j]
                    multi_porcess.append(j)
                    j=0
                    continue
                j+=1
            
            if len(multi_porcess) == 0:
                # Terminal state
                if finish.sum() != self.process_num:
                    return False,[]
                else:
                    return True,sequence
            if len(multi_porcess) == 1:
                sequence.extend(multi_porcess)
            
            else : sequence.append(multi_porcess)
            work+=free_resource
            i+=1
        
        return True,sequence
        

    
    def allocate(self,resource,process_num):
        if np.all(self.need[process_num] < resource): 
            raise Exception("Process cannot request more than what it said at the first")
        if self.available < resource : return False,[]
        self.available -= resource
        self.need[process_num] -= resource
        self.allocation[process_num] +=resource
        safe = self.check_safty()
        if not safe[0]:
            #Undo the changes
            self.available += resource
            self.need[process_num] +=resource
            self.allocation[process_num] -=resource
            return False,[]
        else:
            return True,safe

