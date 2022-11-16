"""
DANGER - This program deletes data from the dataset
"""
import numpy as np

path = "dataset_left.csv"
label_to_delete = [1]

print("You are about to delete the data with the following label : ", label_to_delete, "in the file ",path)
data = np.loadtxt(path, delimiter=',')

for label in label_to_delete:
    data = data[np.where(data[:, 0] != label)]

choice = input("Confirm ? (y/n) ")
if choice == "y":
    np.savetxt(path, data, delimiter=',')
else:
    print("Aborted")