from algorithms.Banker import Banker
import numpy as np

max = np.array([[7,5,3],
                [3,2,2],
                [9,0,2],
                [2,2,2],
                [4,3,3]],dtype=np.int32)

banker = Banker(5,3,max)
allocation = np.array([[0,1,0],
                              [2,0,0],
                              [3,0,2],
                              [2,1,1],
                              [0,0,2]],dtype=np.int32)
banker.allocation = allocation
banker.available = np.array([3,3,2],dtype=np.int32)
banker.need = max - allocation

print(banker.check_safty())