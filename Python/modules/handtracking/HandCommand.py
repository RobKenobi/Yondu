class HandCommand:
    def __init__(self, HandNo, handedness, position, gesture, HandLandmarks):
        self._HandNo = HandNo
        self._handedness = handedness
        self._position = position
        self._gesture = gesture
        self._handLandmarks = HandLandmarks

    def get_handLandmarks(self):
        return self._handLandmarks

    def get_infos(self):
        return self._HandNo, self._handedness, self._position, self._gesture
