import numpy as np
import os
import pickle

# Path to model files
DIR = os.path.dirname(os.path.abspath(__file__))
path_model_right = DIR + "\CART_right.sav"
path_model_left = DIR + "\CART_left.sav"

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


def landmarks_to_numpy(landmarks, get_z=True):
    """
    This function converts a set of landmarks into a numpy array with each line corresponding to a landmark
    This matrix has 3 columns if the parameter get_z is True, otherwise 2.
    :param landmarks: set of landmarks
    :param get_z: bool
    :return: numpy array
    """

    # Initializing the numpy array
    if get_z:
        np_landmarks = np.empty((21, 3))
    else:
        np_landmarks = np.empty((21, 2))

    # Filling the numpy array with the landmarks positions
    for index, landmark in enumerate(landmarks):
        if get_z:
            np_landmarks[index, :] = np.array([landmark.x, landmark.y, landmark.z])
        else:
            np_landmarks[index, :] = np.array([landmark.x, landmark.y])

    return np_landmarks


def normalized_landmarks(landmarks):
    """
    This functions converts a numpy array of the hand landmarks into
    a numpy array of the normalized hand landmarks. Hence, the hand sign
    is independent of the hand size and position.
    :param landmarks: numpy array of the hand landmarks positions
    :return: numpy array of the normalized hand landmarks positions.
    """

    # Setting the wrist landmark position as the reference point
    base_x, base_y = landmarks[0, 0], landmarks[0, 1]
    # Positioning the other landmarks in the wrist frame
    landmarks_norm = landmarks - np.array([base_x, base_y])
    # Normalizing the positions
    landmarks_norm /= np.linalg.norm(landmarks_norm)
    return landmarks_norm


def load_CART_model(path):
    """
    Allows to load a trained CART model
    :param path: path to the model file
    :return: model
    """
    model = pickle.load(open(path, "rb"))
    return model


class HandCommand:
    def __init__(self, HandNo, handedness, position, gesture, HandLandmarks):
        # Hand number
        self._HandNo = HandNo
        # Handedness
        self._handedness = handedness
        # Position of the landmarks in the image
        self._position = position
        # Hand gesture
        self._gesture = gesture
        # Hand landmarks
        self._handLandmarks = HandLandmarks

    def get_hand_landmarks(self):
        """
        This methods returns the hand landmarks
        :return:
        """
        return self._handLandmarks

    def get_numpy_hand_landmarks(self, get_z=True):
        return landmarks_to_numpy(self._handLandmarks, get_z)

    def get_infos(self):
        return self._HandNo, self._handedness, self._position, self._gesture


class HandProcessing:
    def __init__(self, HandDetector):
        self._gesture_classifier_right = None
        self._gesture_classifier_left = None
        self._HandDetector = HandDetector

        self._gesture_classifier_right = load_CART_model(path_model_right)
        self._gesture_classifier_left = load_CART_model(path_model_left)

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
        pose = landmarks_to_numpy(landmarks, get_z=False)
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
                gesture = self.find_gesture(HandLandmarks.landmark)
            else:
                gesture = ""
            list_HandCommand.append(HandCommand(
                HandNo, handedness, position, gesture, HandLandmarks))
        return list_HandCommand
