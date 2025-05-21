import numpy as np

a = np.array([0,1,2,0,0,4,0,6,9])

nz = np.nonzero(a)

print(nz[0])