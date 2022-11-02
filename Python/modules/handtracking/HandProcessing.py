from .HandCommand import HandCommand
import numpy as np


class HandProcessing:
    def __init__(self, HandDetector):
        self._HandDetector = HandDetector

    def find_handedness(self, HandNo=0):
        handedness = self._HandDetector.get_result().multi_handedness[HandNo].classification[0].label
        return handedness

    def find_position(self, image, HandNo=0):
        h, w, c = image.shape
        pos_list = np.zeros((21, 2))
        for id, pos in enumerate(self._HandDetector.get_result().multi_hand_landmarks[HandNo].landmark):
            x, y = int(pos.x * w), int(pos.y * h)
            pos_list[id, 0] = x
            pos_list[id, 1] = y

        return pos_list

    def create_hand_commands(self, image):
        list_HandCommand = list()
        for HandNo, HandLandmarks in enumerate(self._HandDetector.get_result().multi_hand_landmarks):
            handedness = self.find_handedness(HandNo)
            position = self.find_position(image, HandNo)
            gesture = ""
            list_HandCommand.append(HandCommand(HandNo, handedness, position, gesture, HandLandmarks))
        return list_HandCommand
