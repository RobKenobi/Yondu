import numpy as np

data_path = "data_left.npy"
label_path = "label_left.npy"

saving_path = "dataset.csv"

data = np.load(data_path)
label = np.load(label_path)

csv_data = data.reshape(len(data), 42)

dataset = np.concatenate([label[np.newaxis].T, csv_data], axis=1)

np.savetxt(saving_path, dataset, delimiter=',')

dataset = np.loadtxt(saving_path, delimiter=',')

load_label = dataset[:, 0]
load_data = dataset[:, 1:]

load_data = load_data.reshape(len(load_data), 21, 2)
