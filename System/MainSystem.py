from inputs import read_file,generate_timestamp,generate_timestamp_periodic
from .SubSystem2 import SubSystem2
from .SubSystem1 import SubSystem1
from .SubSystem3 import SubSystem3
from .SubSystem4 import SubSystem4
from threading import Semaphore,Thread
from classes.ResourceManager import RealTimeRM
class MainSystem:
    def __init__(self,input_path):
        self.resources , sub_systems = read_file(input_path)
        self.log = ["a" for i in range(4)]
        self.mainsystem_sem = Semaphore(0)
        self.systems_sem = [Semaphore(0),Semaphore(0),Semaphore(0),Semaphore(0)]
        self.rt_rm = RealTimeRM(self.resources[2].r1,self.resources[2].r2,
                                self.resources[0],self.resources[1],self.resources[3])
        self.sub_system1 = SubSystem1(generate_timestamp(sub_systems[0]),self.resources[0],self.log,
                                      self.mainsystem_sem,self.systems_sem[0])
        self.sub_system2 = SubSystem2(generate_timestamp(sub_systems[1]),
                                      self.resources[1],self.log,self.mainsystem_sem,self.systems_sem[1])
        self.sub_system3 = SubSystem3(generate_timestamp_periodic(sub_systems[2]),
                                      self.rt_rm,self.log,self.mainsystem_sem,self.systems_sem[2])
        self.sub_system4 = SubSystem4(generate_timestamp(sub_systems[3]),
                                      self.resources[3],self.log,self.mainsystem_sem,self.systems_sem[3])

        self.t =None
    
    def start(self):
        #Create thread for each thread
        Thread(target=self.sub_system2.running).start()
        Thread(target=self.sub_system1.running).start()
        Thread(target=self.sub_system3.running).start()
        Thread(target=self.sub_system4.running).start()
        self.t = 0
        while True:
            for i in range(4):
                self.systems_sem[i].release()
            for i in range(4):
                self.mainsystem_sem.acquire()
            self.t+=1
            if self.print_():
                break
        
        print("Finished!")
            

    
    def print_(self):
        count_process = 8
        print(f"Time : {self.t}")
        for i in self.log:
            print(i)
        
        n=sum(i.lower().count("idle") for i in self.log)    
        if n==count_process and self.t > 10:
            return True
        return False

        

