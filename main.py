from threading import Semaphore
from Tests.input_test import test_read_file,test_generate_time_stamp
from Tests.subsystems_test import test_sub_system1
from System.MainSystem import MainSystem
#Test input : 
#test_read_file('input.txt') #Pass!
#test_generate_time_stamp('input.txt') # Pass!

#Test Subsystem
## Test Subsystem1:
#test_sub_system1('input.txt',10) #Simple test pass #LoadBalanceTest  Pass #WaitingQueue test Pass
#test_sub_system1('input.txt',20) #Simple Test pass! #Deadlock pass #Preempt pass
#test_sub_system1('input.txt',20) #Simple test Done! # BeforeAfter Done!

#Running the main system!
#Simple test pass
#Hard test ? 
MainSystem('test1.txt').start()