import time

import cv2
import numpy as np
from paho.mqtt.client import Client

from modules.handtracking import HandDetector, HandProcessing, Visualisation

# Hand signs associations dictionary
# Parameters to play with:
# - Vx
# - Vy
# - Vz
# - V_yaw
# - Takeoff
# - Landing

signs_association_left = {
    "Open hand": "takeoff",
    "Closed hand": "stop",
    "index up": "vx",
    "thumb up": "landing",
    "index and middle finger up": "vz",
    "index and thumb joined": "flip_left"
}

signs_association_right = {
    "Open hand": "takeoff",
    "Closed hand": "stop",
    "index up": "vy",
    "thumb up": "landing",
    "index and middle finger up": "v_yaw",
    "index and thumb joined": "flip_right"
}

# Detect the presence of a hand
detector = HandDetector(max_num_hands=2)

# Translate hand gestures into command
interpreter = HandProcessing(detector)

# Object for visualisation
visu = Visualisation()

# Video feed
cap = cv2.VideoCapture(0)

# Communication initialisation
BROKER = "broker.hivemq.com"
BROKER_PORT = 1883
MAIN_TOPIC = "YONDU/DroneCommand/"
connected_to_broker = False


def callback_on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("\nConnected to the broker")
        global connected_to_broker
        connected_to_broker = True
    else:
        print("\nConnection failed")
        exit(1)


client = Client("Camera", clean_session=False)
client.on_connect = callback_on_connect
client.connect(BROKER, BROKER_PORT)
client.loop_start()

i = 0
while not connected_to_broker:
    print("\rConnecting to the broker", i * ".", end="")
    time.sleep(0.01)
    i = (i + 1) % 4

last_time = time.time()
Time_period = 2

while True:

    # Press <ESC> to quit
    if cv2.waitKey(1) == 27:
        print("Voilà bon... Ok ! Hmmmm bye bye !")
        # Closing all windows
        cv2.destroyAllWindows()
        # Turning off the camera
        cap.release()

        # Asking the drone to land
        client.publish("YONDU/DroneCommand/landing", 1)

        # Disconnecting from the broker
        client.disconnect()
        break

    read_image, img = cap.read()
    if read_image:
        img = cv2.flip(img, 1)
        height = img.shape[0]
        copy_img = img.copy()

        # Commands zone
        cv2.rectangle(copy_img, (0, 0), (img.shape[1], int(img.shape[0] * 0.3)), (0, 0, 255), -1)
        cv2.rectangle(copy_img, (0, int(img.shape[0] * 0.6)), (img.shape[1], img.shape[0]), (255, 0, 0), -1)
        img = cv2.addWeighted(img, 0.7, copy_img, 0.3, gamma=0)

        # Finding whether at least one hand is present on the picture
        hand_detected = detector.hands_detection(img)

        # If at least one hand has been detected
        if hand_detected:
            # Compute the list of commands associated to each hand
            commands = interpreter.create_hand_commands(img)

            # Visualisation
            visu.draw_overlays_all(img, commands)

            # Computing new commands every <Time_period> seconds
            if time.time() - last_time > Time_period:
                commands_to_send = list()
                for command in commands:
                    _, _, position, gesture = command.get_infos()

                    position = (np.min(position[:, 1]) + np.max(position[:, 1])) / 2
                    action = 1 if position < height * 0.3 else -1 if position > height * 0.6 else 0

                    commands_to_send.append((gesture, action))

                    # Publishing commands
                    client.publish("YONDU/DroneCommand/" + gesture, action, qos=2)
                last_time = time.time()

        cv2.imshow("Image", img)
