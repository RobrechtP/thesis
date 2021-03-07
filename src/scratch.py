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

path = "../transitions/rain2.txt"
gen = RainGenerator()
data = gen.generate_data()
print(data)
gen.save_data(data, path)
data = gen.load_data(path)
print(data)