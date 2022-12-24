import sys
import os

# Updating path
PYTHON_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
sys.path.insert(1, PYTHON_DIR)

import cv2
import numpy as np

from modules.handtracking import HandDetector, HandProcessing, Visualisation


def normalized_landmarks(landmarks):
    """
    This functions converts a numpy array of the hand landmarks into
    a numpy array of the normalized hand landmarks. Hence, the hand sign
    is independent of the hand size and position.
    :param landmarks: numpy array of the hand landmarks positions
    :return: numpy array of the normalized hand landmarks positions.
    """

    # Setting the wrist landmark position as the reference point
    base_x, base_y = landmarks[0, 0], landmarks[0, 1]
    # Positioning the other landmarks in the wrist frame
    landmarks_norm = landmarks - np.array([base_x, base_y])
    # Normalizing the positions
    landmarks_norm /= np.linalg.norm(landmarks_norm)
    return landmarks_norm


def save_to_csv(data, label, path):
    """
    This function allows to save the landmarks data and their corresponding label
    into a csv file.
    :param data: numpy array of the landmarks
    :param label: numpy array of the labels
    :param path: path with the name of the file
    :return: None
    """
    # Reshaping the data array
    csv_data = data.reshape(len(data), 42)
    # Reshaping the label array
    csv_label = label.reshape(len(label), 1)
    # Concatenating the label and data
    dataset = np.concatenate([csv_label, csv_data], axis=1)
    # Saving the dataset
    np.savetxt(path, dataset, delimiter=',')


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


# Hand signs dictionary
signs = {
    "o": 0,  # Open hand
    "c": 1,  # Closed hand
    "i": 2,  # index up
    "p": 3,  # thumb up
    "v": 4,  # index and middle finger up
    "k": 5,  # index and thumb joined
}

# Hand signs description dictionary
signs_description = {
    "o": "Open hand",
    "c": "Closed hand",
    "i": "index up",
    "p": "thumb up",
    "v": "index and middle finger up",
    "k": "index and thumb joined"
}


def show_keys():
    for sign in signs_description:
        print(sign, " : ", signs_description[sign])


def add_to_dataset(data, label, landmark, key):
    if chr(key) not in signs.keys():
        print("Unknown key")
        show_keys()
        return data, label

    if data is None:
        data = np.array([landmark])
        label = np.array([signs[chr(key)]])
    else:
        data = np.append(data, landmark[np.newaxis], axis=0)
        label = np.append(label, signs[chr(key)])
    print(f"{signs_description[chr(key)]}")
    return data, label


# Detect the presence of a hand
detector = HandDetector(max_num_hands=2)

# Translate hand gestures into command
interpreter = HandProcessing(detector)

# Object for visualisation
visu = Visualisation()

# Image feed
cap = cv2.VideoCapture(0)

cv2.namedWindow("Visualization")

path_dataset_left = "dataset_left.csv"
path_dataset_right = "dataset_right.csv"

# Checking if dataset exists for left hand
if os.path.exists(path_dataset_left):
    print("Loading left dataset")
    data_left, label_left = load_csv(path_dataset_left)
# Else creating data and label variables for left hand
else:
    data_left = None
    label_left = None

# Checking if dataset exists for right hand
if os.path.exists(path_dataset_right):
    print("Loading right dataset")
    data_right, label_right = load_csv(path_dataset_right)
# Else creating data and label variables for right hand
else:
    data_right = None
    label_right = None

# Printing sentence
print("This program goal is to build the training and testing datasets.\n"
      "To do so, you will have to do hand sign and press the corresponding key on your keyboard.\n"
      "These are the signs we are going to recognize with the key you have to press :\n\n")
for sign in signs_description:
    print(sign, " : ", signs_description[sign])

print("\nIf you don't remember which key to press, just press <h> or <enter>")
print("To exit the program, press <ESC>")

# Starting the infinite loop
while True:
    # Getting the key pressed
    key = cv2.waitKey(1)

    # If <ESC> is pressed, exit the loop
    if key == 27:
        # Closing all cv2 windows
        cv2.destroyAllWindows()

        # Closing camera
        cap.release()

        # Update dataset ?
        print("\n If you have made a mistake, don't save the data !\n")
        print("#" * 20)
        choice = input("Save data ? (y/n) : ")
        if choice.lower() == "y":
            # If data from left hand have been collected
            if data_left is not None:
                save_to_csv(data_left, label_left, path_dataset_left)
            # If data from right hand have been collected
            if data_right is not None:
                save_to_csv(data_right, label_right, path_dataset_right)

        break

    # If <h> is pressed
    if key == ord("h"):
        # Show help
        show_keys()

    # Reading image
    _, img = cap.read()
    # Flipping image
    img = cv2.flip(img, 1)

    # Detecting hands
    hand_detected = detector.hands_detection(img)

    # If a hand is detected
    if hand_detected:
        # Generating the command objects
        commands = interpreter.create_hand_commands(img, find_gesture=False)
        # Retrieving normalized hand landmarks
        norm_landmarks = commands[0].get_normalized_landmarks(False)
        # Retrieving handedness
        handedness = commands[0].get_infos()[1]

        # If a key is pressed
        if key != -1:
            # If the left hand has been detected
            if handedness == "Left":
                print("Left hand \t:\t ", end="")
                data_left, label_left = add_to_dataset(data_left, label_left, norm_landmarks, key)
            # If the right hand has been detected
            else:
                print("Right hand \t:\t ", end="")
                data_right, label_right = add_to_dataset(data_right, label_right, norm_landmarks, key)

        visu.draw_overlays_all(img, commands)

    cv2.imshow("Visualization", img)
