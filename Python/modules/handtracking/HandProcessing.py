from .HandCommand import HandCommand
from .utils import landmarks_to_numpy, normalized_landmarks
import tensorflow as tf
import numpy as np


class HandProcessing:
    def __init__(self, HandDetector):
        self._HandDetector = HandDetector
        self._gesture_classifier = tf.keras.models.load_model("model_right.hdf5")

    def find_handedness(self, HandNo=0):
        handedness = self._HandDetector.get_result().multi_handedness[HandNo].classification[0].label
        return handedness

    def find_position_on_image(self, image, HandNo=0):
        h, w, c = image.shape
        pose_array = landmarks_to_numpy(self._HandDetector.get_result().multi_hand_landmarks[HandNo].landmark,
                                        get_z=False)
        pose_array[:, 0] *= w
        pose_array[:, 1] *= h

        return pose_array.astype('int')

    def find_gesture(self, landmarks, handedness="left"):
        # TODO select model depending on handedness
        pose = landmarks_to_numpy(landmarks.landmark, get_z=False)
        norm = normalized_landmarks(pose)
        prediction = self._gesture_classifier.predict(norm[np.newaxis])
        return str(np.argmax(np.squeeze(prediction)))

    def create_hand_commands(self, image):
        list_HandCommand = list()
        for HandNo, HandLandmarks in enumerate(self._HandDetector.get_result().multi_hand_landmarks):
            handedness = self.find_handedness(HandNo)
            position = self.find_position_on_image(image, HandNo)
            gesture = self.find_gesture(HandLandmarks)
            #gesture = ""
            list_HandCommand.append(HandCommand(HandNo, handedness, position, gesture, HandLandmarks))
        return list_HandCommand
