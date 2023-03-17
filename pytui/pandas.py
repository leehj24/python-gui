import matplotlib.pyplot as plt
from pandas import *
import pandas as pd
import numpy as np

x= np.arange(-50,50,1)
y = 1*x**3 + 0*x**2 + 1*x +1
plt.plot(x,y)
plt.show()