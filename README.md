# RT-Scheduling

At first i introduce you to each folder and their property:

### Algorithms:

This folder contains all the algorthm that we need in the next folders. Such as Rate monotonic (RMS) ,SRTF,WRR,FCFS...

Also includedd a banker algorithm that needs numpy to run but it does not needed in this project so i'm going to ignore it!

#### FCFS

simple queue that each process come first serve first

#### RMS:

rate monotonic algorithm that uses a priority queue with priority period. also has method to check if with this process we can schedule or not using the formula for utilization

#### SRTF

use priority queue to sort process with priority burst-doneburest

#### WRR

use 1 priority queue that has two priority first one is the round and second one is the burst to do a weighted round robin

#### Scheduling algorithm

Its a interface for the sched algorithm that most of them work with it

### Classes

classes contains Process ,ReadyQueue,WaitingQueue and Resourcemanager

#### Process

this file contains 3 classes periodic class, process class and dependent process class that gets the input has state and also can do burst. simple code you can easly read it!

#### ReadyQueue

a class that gets an algorithm for the ready queue to sort! and can schedule or get a process from it

#### Resource manager

A resource manager is class that manages your resources you can allocate and deallocate in this class easly!

#### Waiting queue:

this class contains a queue that acts like a fifo !

### System:

this is the most important set of classes. we have all the subsystems and their cores. i just breifly tell you about the creative parts for better understanding please read the codes!

#### Resource managment in one burst :

To sync the process resource allocation and de allocations i used semaphore to sync all the cores when doing a burst and when all of them done a burst then they can deallocate the resources. this prevent from a core that realy doesnt have resources but get some resources after the other thread de allocate!

#### Sync the cores

Simply sync the cores and subsystem with semaphore

#### Loadbalance

in subsystem 1 we need to load balance for that i used a threshold (Hyper parameter ) that forces the ready queue to do not have diffrent size more that threshold for example if we have thresh =2 the queue with this sizes are invalid l+3,l,l+1 but this is valid l+2 , l+1 , l.

#### Starvation problem

in subsystem 4 and 1 we have waiting queue to fix the starvation i used merging the waiting queue to ready queue this merge happens in subsystem4 when a process finished and happens in subsystem1 when a round is finished.

#### Deadlock prevention:

when a deadlock happens it uses reverse aging and gives the process lower priority to fix the deadlock! 

If you have any question contact me!
