import pickle

import numpy as np
from sklearn import tree


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


def generate_model(path_dataset, model_path, validation_split=0.2):
    # Printing message
    message = f"GENERATING {model_path}"
    print("\n" + "*" * len(message))
    print(message)
    print("*" * len(message))

    # Loading dataset
    data, label = load_csv(path_dataset)

    # Reshaping the data
    data = data.reshape(len(data), 42)

    # Computing the number of training data
    dataset_size = len(label)
    training_split = int((1 - validation_split) * dataset_size)

    # Shuffling the index of the dataset
    selection = np.random.permutation(dataset_size)

    # Selecting random elements for the training set
    training_data = data[selection[:training_split]]
    training_label = label[selection[:training_split]]

    # Selecting random elements for the validation set
    test_data = data[selection[training_split:]]
    test_label = label[selection[training_split:]]

    print(f"Training data shape : {training_data.shape}\nTest data shape : {test_data.shape}")

    # Creating model
    model = tree.DecisionTreeClassifier()
    # Training model on training data
    model.fit(training_data, training_label)
    # Evaluating the model on test data
    score = model.score(test_data, test_label)

    print(f"Obtained score on validation data : {score}")

    save_model = input("Save model ? (y/n) ")
    if save_model == "y":
        # Saving model
        pickle.dump(model, open(model_path, "wb"))


if __name__ == "__main__":
    path_dataset_left = "dataset_left.csv"
    path_dataset_right = "dataset_right.csv"

    path_model_left = "../GestureRecognition/CART_left.sav"
    path_model_right = "../GestureRecognition/CART_right.sav"

    generate_model(path_dataset_left, path_model_left)
    generate_model(path_dataset_right, path_model_right)
