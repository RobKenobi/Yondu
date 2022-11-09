import sys
import os

PYTHON_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
sys.path.insert(1, PYTHON_DIR)

import cv2
import numpy as np
from modules.handtracking import HandDetector, HandProcessing, Visualisation
from modules.handtracking.utils import normalized_landmarks

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
path_data = "data.npy"
path_label = "label.npy"

# Try loading matrix
try:
    data = np.load(path_data)
    label = np.load(path_label)
# Except create matrix
except:
    data = None
    label = None

while True:
    # Getting the key pressed
    key = cv2.waitKey(1000)

    # If <ESC> is pressed, exit the loop
    if key == 27:
        # Closing all cv2 windows
        cv2.destroyAllWindows()

        # Closing camera
        cap.release()

        # Update dataset ?
        print("#" * 20)
        choice = input("Save data ? (y/n) : ")
        if choice.lower() == "y":
            np.save(path_data, data)
            np.save(path_label, label)

        break

    # Reading image
    _, img = cap.read()
    # Flipping image
    img = cv2.flip(img, 1)

    # Detecting hands
    hand_detected = detector.hands_detection(img)

    if hand_detected:
        commands = interpreter.create_hand_commands(img)
        landmarks = commands[0].get_numpy_hand_landmarks(False)
        norm_landmarks = normalized_landmarks(landmarks)

        if key != -1:
            if data is None:
                data = np.array([norm_landmarks])
                label = np.array([chr(key)])
            else:
                data = np.append(data, norm_landmarks[np.newaxis], axis=0)
                label = np.append(label, chr(key))
            print(data.shape)

        visu.draw_overlays_all(img, commands)

    cv2.imshow("Visualization", img)
