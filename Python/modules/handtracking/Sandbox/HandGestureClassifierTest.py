import sys
import os

import numpy as np

PYTHON_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
sys.path.insert(1, PYTHON_DIR)

import cv2
import tensorflow as tf
from modules.handtracking import HandDetector, HandProcessing, Visualisation
from modules.handtracking.utils import normalized_landmarks

model_path = "model_right.hdf5"

model = tf.keras.models.load_model(model_path)

# Detect the presence of a hand
detector = HandDetector(max_num_hands=2)

# Translate hand gestures into command
interpreter = HandProcessing(detector)

# Object for visualisation
visu = Visualisation()

# Image feed
cap = cv2.VideoCapture(0)

cv2.namedWindow("Visualization")

while True:
    # Getting the key pressed
    key = cv2.waitKey(1)

    # If <ESC> is pressed, exit the loop
    if key == 27:
        # Closing all cv2 windows
        cv2.destroyAllWindows()

        # Closing camera
        cap.release()

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

        visu.draw_overlays_all(img, commands)

    cv2.imshow("Visualization", img)
