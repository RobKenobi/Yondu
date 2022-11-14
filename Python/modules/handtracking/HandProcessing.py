from .HandCommand import HandCommand
from .utils import landmarks_to_numpy, normalized_landmarks, load_CART_model
import pickle

path_model_right = "CART_right.sav"
path_model_left = "CART_left.sav"

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


class HandProcessing:
    def __init__(self, HandDetector):
        self._HandDetector = HandDetector

        self._gesture_classifier_right = None
        self._gesture_classifier_left = None

    def set_model_left(self, model):
        self._gesture_classifier_left = model

    def set_model_right(self, model):
        self._gesture_classifier_right = model

    def find_handedness(self, HandNo=0):
        handedness = self._HandDetector.get_result(
        ).multi_handedness[HandNo].classification[0].label
        return handedness

    def find_position_on_image(self, image, HandNo=0):
        h, w, c = image.shape
        pose_array = landmarks_to_numpy(self._HandDetector.get_result().multi_hand_landmarks[HandNo].landmark,
                                        get_z=False)
        pose_array[:, 0] *= w
        pose_array[:, 1] *= h

        return pose_array.astype('int')

    def find_gesture(self, landmarks, handedness="left"):
        if self._gesture_classifier_left is None or self._gesture_classifier_right is None:
            print("No model set")
            raise NotImplementedError

        pose = landmarks_to_numpy(landmarks.landmark, get_z=False)
        norm = normalized_landmarks(pose).reshape(1, 42)
        if handedness == "left":
            prediction = self._gesture_classifier_left.predict(norm)
        else:
            prediction = self._gesture_classifier_right.predict(norm)
        return list(signs_description.values())[int(prediction)]

    def create_hand_commands(self, image, find_gesture=True):
        list_HandCommand = list()
        for HandNo, HandLandmarks in enumerate(self._HandDetector.get_result().multi_hand_landmarks):
            handedness = self.find_handedness(HandNo)
            position = self.find_position_on_image(image, HandNo)
            if find_gesture:
                gesture = self.find_gesture(HandLandmarks)
            else:
                gesture = ""
            list_HandCommand.append(HandCommand(
                HandNo, handedness, position, gesture, HandLandmarks))
        return list_HandCommand
