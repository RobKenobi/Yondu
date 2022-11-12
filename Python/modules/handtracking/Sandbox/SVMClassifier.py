from sklearn import svm
import numpy as np

# Selecting which model to build {True, False}
right_hand = True

# Path definition
data_path = "data_right.npy" if right_hand else "data_left.npy"
label_path = "label_right.npy" if right_hand else "label_left.npy"
model_save_path = "model_right.hdf5" if right_hand else "model_left.hdf5"

# Loading data and label
data = np.load(data_path)
label = np.load(label_path)

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