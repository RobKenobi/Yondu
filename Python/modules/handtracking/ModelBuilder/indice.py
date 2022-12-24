import numpy as np

path = "dataset_left.csv"

data = np.loadtxt(path, delimiter=',')
label = data[:, 0]

label = np.where(label > 0, label - 1, label)

data[:, 0] = label

np.savetxt(path, data, delimiter=',')
