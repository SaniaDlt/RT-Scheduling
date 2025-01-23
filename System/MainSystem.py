from inputs import read_file,generate_timestamp
from SubSystem2 import SubSystem2
from threading import Semaphore,Thread
class MainSystem:
    def __init__(self,input_path):
        self.resources , sub_systems = read_file(input_path)
        self.log = ["" for i in range(4)]
        self.mainsystem_sem = Semaphore(0)
        self.systems_sem = Semaphore(0)

        self.sub_system2 = SubSystem2(generate_timestamp(sub_systems[1]),
                                      self.resources[1],self.log,self.mainsystem_sem,self.systems_sem)

        self.t =None
    
    def start(self):
        #Create thread for each thread
        Thread(target=self.sub_system2.running).start()
        self.t = 0
        while True:
            self.systems_sem.release(4)
            for i in range(4):
                self.mainsystem_sem.acquire()
            self.t+=1
            self.print_()
            

    
    def print_(self):
        print(self.t)
        for i in self.log:
            print(i)
        

        

