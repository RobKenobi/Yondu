from modules.handtracking import HandDetector, HandProcessing, Visualisation
import cv2

# Detect the presence of a hand
detector = HandDetector()

# Translate hand gestures into command
interpreter = HandProcessing(detector)

# Object for visualisation
visu = Visualisation()

cap = cv2.VideoCapture(0)

while True:
    success, image = cap.read()
    img = cv2.flip(image, 1)

    success = detector.hands_detection(img)

    if success:
        commands = interpreter.create_hand_commands(img)
        visu.draw_overlays_all(img, commands)

    cv2.imshow("Image", img)
    # Press "e" to exit
    if cv2.waitKey(1) == ord("e"):
        break
