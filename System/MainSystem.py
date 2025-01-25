from inputs import read_file,generate_timestamp,generate_timestamp_periodic
from .SubSystem2 import SubSystem2
from .SubSystem1 import SubSystem1
from .SubSystem3 import SubSystem3
from .SubSystem4 import SubSystem4
from threading import Semaphore,Thread
from classes.ResourceManager import RealTimeRM
import tkinter as tk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np

class MainSystem:
    def __init__(self,input_path):
        self.resources , sub_systems = read_file(input_path)
        self.log = ["a" for i in range(4)]
        self.mainsystem_sem = Semaphore(0)
        self.systems_sem = [Semaphore(0),Semaphore(0),Semaphore(0),Semaphore(0)]
        self.in_min = Semaphore(0)
        self.in_sys = [Semaphore(0),Semaphore(0),Semaphore(0),Semaphore(0)]
        self.rt_rm = RealTimeRM(self.resources[2].r1,self.resources[2].r2,
                                self.resources[0],self.resources[1],self.resources[3])
        self.sub_system1 = SubSystem1(generate_timestamp(sub_systems[0]),self.resources[0],self.log,
                                      self.mainsystem_sem,self.systems_sem[0],self.in_min,self.in_sys[0])
        self.sub_system2 = SubSystem2(generate_timestamp(sub_systems[1]),
                                      self.resources[1],self.log,self.mainsystem_sem,self.systems_sem[1],
                                      self.in_min,self.in_sys[1])
        self.sub_system3 = SubSystem3(generate_timestamp_periodic(sub_systems[2]),
                                      self.rt_rm,self.log,self.mainsystem_sem,self.systems_sem[2],self.in_min,self.in_sys[2])
        self.sub_system4 = SubSystem4(generate_timestamp(sub_systems[3]),
                                      self.resources[3],self.log,self.mainsystem_sem,self.systems_sem[3],self.in_min,self.in_sys[3])
        self.sub_sytems = sub_systems
        self.t =None
        self.cores = [3,2,1,2]
        self.utilization = [[[] for j in range(self.cores[i])] for i in range(len(self.sub_sytems))]
        self.root = tk.Tk()

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
                self.in_min.acquire()
            for i in range(4):
                self.in_sys[i].release()
            for i in range(4):
                self.mainsystem_sem.acquire()
            self.t+=1
            if self.print_():
                break
        print("Summery:")
        
        for i in range(len(self.sub_sytems)):
            for p in self.sub_sytems[i]:
                print(p)
        print("Finished!")
        self.update_plot()
        self.root.mainloop()

    def update_plot(self):
        fig, axes = plt.subplots(2, 6, figsize=(15, 8))
        x= [i for i in range( len(self.utilization[0][0]))]
        print(self.utilization)
        axes = axes.flatten()
        k=0
        for i in range(4):
            aggregate=np.zeros(len(x))
            for j in range(self.cores[i]):
                ax = axes[k]
                k+=1
                aggregate+=np.array(self.utilization[i][j])
                ax.plot(x,self.utilization[i][j],color='r')
                ax.set_title(f"Core {j+1} in subsystem {i+1}")
            aggregate/=self.cores[i]
            ax = axes[k]
            k+=1
            
            ax.plot(x,list(aggregate),marker='^',color='g',linestyle='--')
            ax.set_title(f"SubSystem {i+1}")
    

        # Display the plot in Tkinter
        canvas = FigureCanvasTkAgg(fig, master=self.root)
        canvas.draw()
        # Clear previous plot and update with new canvas
        canvas.get_tk_widget().pack()
            

    
    def print_(self):
        count_process = 8
        print(f"Time : {self.t}")
        for i in self.log:
            print(i)
        for i in range(len(self.log)):
            lines = self.log[i].split("\n")
            k=0
            for line in lines:
                if "Running task: idle" in line:
                    self.utilization[i][k].append(0)
                    k+=1
                elif "Running task:" in line:
                    self.utilization[i][k].append(100)
                    k+=1
            

        
        n=sum(i.lower().count("idle") for i in self.log)    
        if n==count_process and self.t > 10:
            return True
        return False

        

