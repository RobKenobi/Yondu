import cv2
from paho.mqtt.client import Client

from modules.handtracking import HandDetector, HandProcessing, Visualisation

# TODO association between gesture and parameters to change

# Detect the presence of a hand
detector = HandDetector(max_num_hands=2)

# Translate hand gestures into command
interpreter = HandProcessing(detector)

# Object for visualisation
visu = Visualisation()

# Video feed
cap = cv2.VideoCapture(0)

# Communication initialisation
BROKER = "mqtt.eclipseprojects.io"
BROKER_PORT = 1883

client = Client()
client.connect(BROKER, BROKER_PORT)

while True:

    # Press <ESC> to quit
    if cv2.WaitKey(0) == 27:
        print("Voilà bon... Ok ! Hmmmm bye bye !")
        # Closing all windows
        cv2.destroyAllWindows()
        # Turning off the camera
        cap.close()
        break

    read_image, img = cap.read()
    if read_image:
        img = cv2.flip(img, 1)

        # Finding whether at least one hand is present on the picture
        hand_detected = detector.hands_detection(img)

        # If at least one hand has been detected
        if hand_detected:
            # Compute the list of commands associated to each hand
            commands = interpreter.create_hand_commands(img)

            # Visualisation
            visu.draw_overlays_all(img, commands)

            # TODO get hands positions and compute command to send


