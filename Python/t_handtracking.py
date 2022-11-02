from modules.handtracking import HandDetector, HandProcessing
import cv2

# Detect the presence of a hand
detector = HandDetector()

# Translate hand gestures into command
interpreter = HandProcessing(detector)

cap = cv2.VideoCapture(0)

while True:
    success, image = cap.read()
    img = cv2.flip(image, 1)

    success = detector.hands_detection(img)

    if success:
        commands = interpreter.create_hand_commands(img)
        print(len(commands))
    else:
        print(0)