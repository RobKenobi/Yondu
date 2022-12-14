import cv2
import mediapipe as mp
import numpy as np


class Visualisation:
    def __init__(self):
        self._mpDraw = mp.solutions.drawing_utils
        self._mpHands = mp.solutions.hands

    def display_handLandmarks(self, image, commands):
        for command in commands:
            HandLandmarks = command.get_hand_landmarks()
            self._mpDraw.draw_landmarks(image, HandLandmarks, self._mpHands.HAND_CONNECTIONS,
                                        self._mpDraw.DrawingSpec(color=(0, 0, 0), thickness=6,
                                                                 circle_radius=2),
                                        self._mpDraw.DrawingSpec(color=(128, 128, 128), thickness=2,
                                                                 circle_radius=0))

    def draw_overlays(self, image, commands, padding=9):
        for hand in commands:
            HandNo, handedness, position, gesture = hand.get_infos()
            # Get all x and y values of the hand
            x_coord = position[:, 0]
            y_coord = position[:, 1]
            # Get bounding boxes coordinates
            x1 = int(np.min(x_coord) - padding)
            y1 = int(np.min(y_coord) - padding)
            x2 = int(np.max(x_coord) + padding)
            y2 = int(np.max(y_coord) + padding)
            cv2.rectangle(image, (x1, y1), (x2, y2), (211, 93, 63), 3)
            cv2.circle(image, (int((x1 + x2) / 2), int((y1 + y2) / 2)), 3, (0, 255, 0), 3)

            cv2.rectangle(image, (x1 - 2, y1 - 20), (x2 + 2, y1), (211, 93, 63), -1)

            cv2.putText(image, handedness + " : " + gesture, (x1, y1 - 4), cv2.FONT_HERSHEY_COMPLEX,
                        0.6, (255, 255, 255), thickness=1)

    def draw_overlays_all(self, image, command):
        self.display_handLandmarks(image, command)
        self.draw_overlays(image, command)
