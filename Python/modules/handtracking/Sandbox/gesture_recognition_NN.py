import sys
import os

PYTHON_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
sys.path.insert(1, PYTHON_DIR)

import cv2
import numpy as np
from modules.handtracking import HandDetector, HandProcessing, Visualisation
from modules.handtracking.utils import normalized_landmarks

# Hand signs dictionary
signs = {
    "o": 0,  # Open hand
    "c": 1,  # Closed hand
    "i": 2,  # index up
    "f": 3,  # middle finger up
    "v": 4,  # index and middle finger up
    "e": 5,  # thumb and pinky up
    "s": 6,  # thumb, index and pinky up
    "u": 7,  # index and pinky up
    "k": 8,  # index and thumb joined
    "t": 9  # italian sign
}

# Hand signs description dictionary
signs_description = {
    "o": "Open hand",
    "c": "Closed hand",
    "i": "index up",
    "f": "middle finger up",
    "v": "index and middle finger up",
    "e": "thumb and pinky up",
    "s": "thumb, index and pinky up",
    "u": "index and pinky up",
    "k": "index and thumb joined",
    "t": "italian sign"
}


def add_to_dataset(data, label, landmark, key):
    if chr(key) not in signs.keys():
        print("Unknown key")
        for sign in signs_description:
            print(sign, " : ", signs_description[sign])
        return data, label

    if data is None:
        data = np.array([landmark])
        label = np.array([signs[chr(key)]])
    else:
        data = np.append(data, landmark[np.newaxis], axis=0)
        label = np.append(label, signs[chr(key)])
    print(f"Added sign : {signs_description[chr(key)]}")
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

# Path to data and label files
path_data_left = "data_left.npy"
path_label_left = "label_left.npy"

path_data_right = "data_right.npy"
path_label_right = "label_right.npy"

# Checking if data and label files exist for left hand
if os.path.exists(path_data_left):
    data_left = np.load(path_data_left)
    label_left = np.load(path_label_left)
# Else creating data and label variables for left hand
else:
    data_left = None
    label_left = None

# Checking if data and label files exist for right hand
if os.path.exists(path_data_right):
    data_right = np.load(path_data_right)
    label_right = np.load(path_label_right)
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
                # Saving data
                np.save(path_data_left, data_left)
                # Saving label
                np.save(path_label_left, label_left)
            # If data from right hand have been collected
            if data_right is not None:
                # Saving data
                np.save(path_data_right, data_right)
                # Saving label
                np.save(path_label_right, label_right)

        break

    # Reading image
    _, img = cap.read()
    # Flipping image
    img = cv2.flip(img, 1)

    # Detecting hands
    hand_detected = detector.hands_detection(img)

    # If a hand is detected
    if hand_detected:
        # Generating the command objects
        commands = interpreter.create_hand_commands(img)
        # Retrieving hand landmarks
        landmarks = commands[0].get_numpy_hand_landmarks(False)
        # Retrieving handedness
        handedness = commands[0].get_infos()[1]
        # Normalizing the hand landmarks
        norm_landmarks = normalized_landmarks(landmarks)

        # If a key is pressed
        if key != -1:
            # If the left hand has been detected
            if handedness == "Left":
                data_left, label_left = add_to_dataset(data_left, label_left, norm_landmarks, key)
            # If the right hand has been detected
            else:
                data_right, label_right = add_to_dataset(data_right, label_right, norm_landmarks, key)

        visu.draw_overlays_all(img, commands)

    cv2.imshow("Visualization", img)
