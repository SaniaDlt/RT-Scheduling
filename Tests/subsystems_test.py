from inputs import read_file,generate_timestamp
from System.SubSystem1 import SubSystem1
from System.SubSystem2 import SubSystem2
from System.SubSystem4 import SubSystem4
from threading import Semaphore,Thread
def test_sub_system1(path,step):
    
    log = ["" for i in range(4)]
    mainsystem_sem = Semaphore(0)
    systems_sem = Semaphore(0)
    sub_system = create_subsystem4(path,log,systems_sem,mainsystem_sem)
    Thread(target=sub_system.running).start()
    t=0
    def print_():
        print(f"Time : {t}")
        for i in log:
            print(i)
    
    for i in range(step):
        t+=1
        systems_sem.release()
        mainsystem_sem.acquire()
        print_()

def create_subsystem1(path,log,systems_sem,mainsystem_sem):
    resource,subsystems=read_file(path)
    return SubSystem1(generate_timestamp(subsystems[0]),resource[0],log,
                                      mainsystem_sem,systems_sem)
def create_subsystem2(path,log,systems_sem,mainsystem_sem):
    resource,subsystems=read_file(path)
    return SubSystem2(generate_timestamp(subsystems[1]),resource[1],log,
                                      mainsystem_sem,systems_sem)

def create_subsystem4(path,log,systems_sem,mainsystem_sem):
    resource,subsystems=read_file(path)
    return SubSystem4(generate_timestamp(subsystems[3]),resource[3],log,
                                      mainsystem_sem,systems_sem)