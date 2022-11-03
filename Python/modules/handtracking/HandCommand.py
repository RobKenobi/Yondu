import numpy as np


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

    def get_numpy_hand_landmarks(self):
        for i, landmark in enumerate(self._handLandmarks.landmark):
            self._numpy_hand_landmarks[i, :] = np.array([landmark.x, landmark.y, landmark.z])
        return self._numpy_hand_landmarks

    def get_infos(self):
        return self._HandNo, self._handedness, self._position, self._gesture
