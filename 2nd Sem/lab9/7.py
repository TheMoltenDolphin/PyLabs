import numpy as np

url = 'https://archive.ics.uci.edu/ml/machine-learning-databases/iris/iris.data'
iris = np.genfromtxt(url, delimiter=',', dtype='object')

column = iris[:, -1]

unique_species, counts = np.unique(column, return_counts=True)

print(unique_species)
print(counts)