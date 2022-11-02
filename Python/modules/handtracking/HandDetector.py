import cv2
import mediapipe as mp
import numpy as np


class HandDetector():
    def __init__(self, static_image_mode=False, max_num_hands=2, min_detection_confidence=0.5,
                 min_tracking_confidence=0.5):

        # Initialisation of mp.Hands
        self.static_image_mode = static_image_mode  # indicates whether the image is static or not
        self.max_num_hands = max_num_hands          # maximum number of hands detected
        self.min_detection_confidence = min_detection_confidence    # probability threshold that there is a hand
        self.min_tracking_confidence = min_tracking_confidence      # probability threshold of the position of the hand

        # MediaPipe
        self.mpHands = mp.solutions.hands
        self.hands = self.mpHands.Hands(static_image_mode=self.static_image_mode, max_num_hands=self.max_num_hands,
                                        min_detection_confidence=self.min_detection_confidence,
                                        min_tracking_confidence=self.min_tracking_confidence)
        # Mediapipe drawing class
        self.mpDraw = mp.solutions.drawing_utils

    def find_hands_2D(self, image, display_hands=False, gesture_recognition=False):
        image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

        # Perform the hand landmarks detection
        self.results = self.hands.process(image_rgb)
        success = False
        # If landmarks is detected
        if self.results.multi_hand_landmarks:  # Use multi_hand_world_landmarks to get 3d pose
            success = True
            self.hands_info = []

            for HandNo, HandLandmarks in enumerate(self.results.multi_hand_landmarks):

                handedness = self.find_handeness(HandNo=HandNo)
                position = self.find_position(image=image, HandNo=HandNo)
                gesture = "None"
                self.hands_info.append([HandNo, handedness, position, gesture])
                # print(HandLandmarks)
                if display_hands:
                    self.mpDraw.draw_landmarks(image, HandLandmarks, self.mpHands.HAND_CONNECTIONS,
                                               self.mpDraw.DrawingSpec(color=(0, 0, 0), thickness=6,
                                                                       circle_radius=2),
                                               self.mpDraw.DrawingSpec(color=(128, 128, 128), thickness=2,
                                                                       circle_radius=0))

        return success, image

    def find_handeness(self, HandNo=0):
        if self.results.multi_hand_landmarks:
            handedness = self.results.multi_handedness[HandNo].classification[0].label
        return handedness

    def find_position(self, image, HandNo=0):
        h, w, c = image.shape
        if self.results.multi_hand_landmarks:
            pos_list = np.zeros((21, 2))
            for id, pos in enumerate(self.results.multi_hand_landmarks[HandNo].landmark):
                x, y = int(pos.x * w), int(pos.y * h)
                pos_list[id, 0] = x
                pos_list[id, 1] = y

        return pos_list

    def draw_overlays(self, image, padding=9):

        for hand in self.hands_info:
            HandNo, handedness, position, gesture = hand
            # Get all x and y values of the hand
            x_coord = position[:, 0]
            y_coord = position[:, 1]
            # Get bounding boxes coordinates
            x1 = int(np.min(x_coord) - padding)
            y1 = int(np.min(y_coord) - padding)
            x2 = int(np.max(x_coord) + padding)
            y2 = int(np.max(y_coord) + padding)
            cv2.rectangle(image, (x1, y1), (x2, y2), (211, 93, 63), 3)

            cv2.rectangle(image, (x1 - 2, y1 - 20), (x2 + 2, y1), (211, 93, 63), -1)
            cv2.putText(image, handedness + ": " + gesture, (x1, y1 - 4), cv2.FONT_HERSHEY_COMPLEX,
                        0.6, (255, 255, 255), thickness=1)

        return
