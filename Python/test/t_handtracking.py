import os
import sys

# Add the Python directory to the path
PYTHON_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(1, PYTHON_DIR)

from modules.handtracking import HandDetector, HandProcessing, Visualisation
import cv2

# Detect the presence of a hand
detector = HandDetector(max_num_hands=2)

# Translate hand gestures into command
interpreter = HandProcessing(detector)

# Object for visualisation
visu = Visualisation()

# Image feed
cap = cv2.VideoCapture(0)

while True:
    # Getting image from camera
    _, image = cap.read()

    # Flipping image
    img = cv2.flip(image, 1)

    # Finding whether at least one hand is present on the picture
    hand_detected = detector.hands_detection(img)

    # If at least one hand has been detected
    if hand_detected:
        # Compute the list of commands associated to each hand
        commands = interpreter.create_hand_commands(img)

        # Visualisation
        visu.draw_overlays_all(img, commands)

    cv2.imshow("Image", img)
    # Press "e" to exit
    if cv2.waitKey(1) == ord("e"):
        # Closing windows
        cv2.destroyAllWindows()

        # Turning off camera
        cap.release()
        break
