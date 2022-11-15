import mediapipe as mp
import cv2


class HandDetector:
    def __init__(self, static_image_mode=False, max_num_hands=2, min_detection_confidence=0.5,
                 min_tracking_confidence=0.5):
        # Initialisation of mp.Hands
        self._static_image_mode = static_image_mode  # indicates whether the image is static or not
        self._max_num_hands = max_num_hands  # maximum number of hands detected
        self._min_detection_confidence = min_detection_confidence  # probability threshold that there is a hand
        self._min_tracking_confidence = min_tracking_confidence  # probability threshold of the position of the hand

        # MediaPipe
        self._mpHands = mp.solutions.hands
        self._hands = self._mpHands.Hands(static_image_mode=self._static_image_mode, max_num_hands=self._max_num_hands,
                                          min_detection_confidence=self._min_detection_confidence,
                                          min_tracking_confidence=self._min_tracking_confidence)

        # Others
        self._result = None

    def get_result(self):
        return self._results

    def hands_detection(self, image):
        image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

        # Perform the hand landmarks detection
        self._results = self._hands.process(image_rgb)
        # Success is True if at least one hand has been detected
        success = True if self._results.multi_hand_landmarks else False
        return success
