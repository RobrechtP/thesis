import fnmatch
import numpy as np
import math
import time
from src.pomdp import *
from src.solverAdapter import *
import numpy as np
from src.simulator import *
from src.controller import *
from src.logger import *
from src.slipGenerator import *
import time



test = [([[1],[1]]), ([1,2,3])]
test = np.random.random((50,50,750))


np.save("testdata.npy", test)
test2 = np.load("testdata.npy", allow_pickle=True)

print(test2[0][0][0])
print(test2.size)