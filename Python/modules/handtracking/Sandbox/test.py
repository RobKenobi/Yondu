import pickle
import numpy as np


def load_csv(path):
    """
    This function allows to load data and label from a csv file
    :param path: path of the dataset containing the data and the labels
    :return: tuple of numpy arrays (data, label)
    """
    # Load the dataset
    dataset = np.loadtxt(path, delimiter=',')
    # Extract the labels as integers
    label = dataset[:, 0].astype('int')
    # Extract the data
    data = dataset[:, 1:]
    # Reshape the data
    data = data.reshape(len(data), 21, 2)
    return data, label


data, label = load_csv("dataset_left.csv")
data = data.reshape(len(data), 42)

model = pickle.load(open("CART_left.sav", "rb"))

score = model.predict(data)
print(np.mean(score == label))
