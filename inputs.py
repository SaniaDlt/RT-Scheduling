from classes.Process import Process,PeriodicProcess,DependentProcess
from classes.ResourceManager import ResourceManager

def read_file(path):
    resources = [0 for i in range(4)]
    sub_systems = [[] for i in range(4)]

    with open(path,'r') as file:
        i=0
        j=0
        for line in file:
            # Getting resources from file
            if i<=3:
                res = line.strip().split(" ")
                resources[i] = ResourceManager(int(res[0]),int(res[1]))
                i+=1
            elif "$" in line:
                #Changing input of the subsystem
                j+=1
                continue
            else:
                process = line.strip().split(" ")
                if j==0:
                    sub_systems[j].append(
                        Process(process[0],int(process[1]),int(process[2]),int(process[3]),int(process[4])))
                elif j==1:
                    sub_systems[j].append(
                        Process(process[0],int(process[1]),int(process[2]),int(process[3])))
                elif j==2:
                    sub_systems[j].append(
                        PeriodicProcess(process[0],int(process[1])
                                        ,int(process[2]),int(process[3]),int(process[4]),int(process[5])))
                elif j==3:
                    sub_systems[j].append(
                        DependentProcess(process[0],int(process[1])
                                     ,int(process[2]),int(process[3]),process[4]))

    return resources,sub_systems

def intrupt_handler(timestamp:list,t):
    if len(timestamp) <t or timestamp[t]==0: return None
    return timestamp[t]
                
def generate_timestamp(subsystem_list):
    temp = 0
    for p in subsystem_list:
        temp = max(temp,p.arrive)
    
    timestamp = [0 for i in range(temp)]
    
    for p in subsystem_list:
        i = p.arrive
        if timestamp[i] == 0:
            timestamp[i] = []
        timestamp[i].append(p)

    return timestamp
                
