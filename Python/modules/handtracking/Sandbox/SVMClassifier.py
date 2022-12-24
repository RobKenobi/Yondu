from sklearn import svm
import numpy as np
import pickle


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


# Selecting which model to build {True, False}
right_hand = False

# Path definition
dataset_path = "dataset_right.csv" if right_hand else "dataset_left.csv"
model_path = "SVM_right.sav" if right_hand else "SVM_left.sav"

# Loading dataset
data, label = load_csv(dataset_path)

# Reshaping the data
data = data.reshape(len(data), 42)

# Splitting the dataset
TEST_SPLIT = 0.1

dataset_size = len(label)
training_split = int((1 - TEST_SPLIT) * dataset_size)

selection = np.random.permutation(dataset_size)

training_data = data[selection[:training_split]]
training_label = label[selection[:training_split]]

test_data = data[selection[training_split:]]
test_label = label[selection[training_split:]]

print(f"Training data shape : {training_data.shape}\nTest data shape : {test_data.shape}")

model = svm.SVR()
model.fit(training_data, training_label)
score = model.score(test_data, test_label)

print(score)
