import numpy as np
from .utils import landmarks_to_numpy


class HandCommand:
    def __init__(self, HandNo, handedness, position, gesture, HandLandmarks):
        self._HandNo = HandNo
        self._handedness = handedness
        self._position = position
        self._gesture = gesture
        self._handLandmarks = HandLandmarks
        self._numpy_hand_landmarks = np.zeros((21, 3))

    def get_hand_landmarks(self):
        return self._handLandmarks

    def get_numpy_hand_landmarks(self, get_z=True):
        return landmarks_to_numpy(self._handLandmarks.landmark, get_z)

    def get_infos(self):
        return self._HandNo, self._handedness, self._position, self._gesture
