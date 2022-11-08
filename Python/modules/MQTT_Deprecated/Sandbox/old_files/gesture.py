import paho.mqtt.client as mqtt
import os
import cv2
import time
import os
import mediapipe as mp  # https://mediapipe.dev
import paho.mqtt.client

# =========================================================================

NETPIE_HOST = "broker.netpie.io"
CLIENT_ID = "9f7bb790-de04-405c-b315-e6a4bbdebb9d"
DEVICE_TOKEN = "qKvczqN9k816orMioQeDcM8Cm7MJHdKA"


# =========== functions ====================================================
# ----------- NETPIE -----------------------------------------------------

# MQTT_Deprecated functions
def on_connect(client, userdata, flags, rc):
    print("Result from connect: {}".format(mqtt.connack_string(rc)))
    client.subscribe("@shadow/data/updated")


def on_subscribe(client, userdata, mid, granted_qos):
    print("I've subscribed")

def on_message(client, userdata, msg):
    print(msg.payload)
    data_ = str(msg.payload).split(",")
    data_led = data_[1].split("{")
    data_led1 = data_led[1].split(":")
    data_led2 = data_led1[1].split("}")
    data_led3 = data_led2[0]
    print(data_led3)


def publish(topic, msg):  # (String,String)
    client = mqtt.Client(protocol=mqtt.MQTTv311, client_id=CLIENT_ID, clean_session=True)
    client.publish(topic, msg)
    print('PUBLISHED :', msg)


# ========= FingerImage ====================================================

# Camera Setup
wCam, hCam = 480, 640

cap = cv2.VideoCapture(0)
cap.set(3, wCam)
cap.set(4, hCam)

print('Camera SETUP: OK')  # Logitech C270 3 MP Webcam

# Mediapipe Setup
mpHands = mp.solutions.hands
hands = mpHands.Hands(max_num_hands=2, min_tracking_confidence=0.8)
mpDraw = mp.solutions.drawing_utils
print("MEDIAPIPE: OK")

# Using the mediapipe landmarks, we select the landmarks we want to work with
# More information on https://google.github.io/mediapipe/solutions/hands.html

tipsIds = [4, 8, 12, 16, 20]
mcpIds = [2, 6, 10, 14, 18]
Fingers = ['Thumb', 'Index', 'Middle Finger', 'Ring Finger', 'Pinky Finger']
FingerState = [0, 0, 0, 0, 0]

## Gesture are determined with a array of 5 representing each fingers
## If a finger is raised we will set its value to 1

# Gesture List
Gesture_R = [[0, 0, 0, 0, 0], [0, 1, 0, 0, 0], [0, 1, 1, 0, 0], [0, 1, 1, 1, 0], [0, 1, 1, 1, 1], [1, 1, 1, 1, 1],
             [1, 1, 0, 0, 1], [0, 0, 1, 0, 0], [1, 0, 0, 0, 1]]
Gesture_L = [[1, 0, 0, 0, 0], [1, 1, 0, 0, 0], [1, 1, 1, 0, 0], [1, 1, 1, 1, 0], [1, 1, 1, 1, 1], [0, 1, 1, 1, 1],
             [0, 1, 0, 0, 1], [1, 0, 1, 0, 0], [0, 0, 0, 0, 1]]

Gesture_name = ['Zero/CloseHand', 'One', 'Two/Peace', 'Tree', 'Four', 'Five/OpenHand', 'RockAndRoll', '****', 'Surfer']
# Gesture number, each number correspond to a gesture
Gesture_index = [0, 1, 2, 3, 4, 5, 6, 7, 8]

topic = '@msg/thomasthetrain'

# ==================================================================================================
# MQTT_Deprecated SETUP
client = mqtt.Client(protocol=mqtt.MQTTv311, client_id=CLIENT_ID, clean_session=True)
client.username_pw_set(DEVICE_TOKEN)
client.on_connect = on_connect
client.on_subscribe = on_subscribe
client.on_message = on_message
client.connect(NETPIE_HOST, 1883)
client.loop_start()

# ==================================================================================================
time1 = time.time()

while True:
    success, img = cap.read()

    if success:
        img = cv2.flip(img, 1)

        # Find Hands and add lm to a list
        imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        results = hands.process(imgRGB)
        lm_list = []
        if results.multi_hand_landmarks:
            for HandLandmarks in results.multi_hand_landmarks:
                for id, lm in enumerate(HandLandmarks.landmark):
                    h, w, c = img.shape
                    cx, cy = int(lm.x * w), int(lm.y * w)
                    lm_list.append([id, cx, cy])
                # Drawn Land_marks of the hand
                mpDraw.draw_landmarks(img, HandLandmarks, mpHands.HAND_CONNECTIONS)

        if len(lm_list) != 0:
            # https: // google.github.io / mediapipe / solutions / hands

            # Determine if it's the right or left hand ?
            if lm_list[1][1] < lm_list[17][1]:
                Gesture = Gesture_R
            if lm_list[1][1] > lm_list[17][1]:
                Gesture = Gesture_L

            ## Determine if a finger is raised or not

            # The thumb is a special case
            if lm_list[tipsIds[1]][1] < lm_list[tipsIds[0] - 1][1]:
                FingerState[0] = 1
            if lm_list[tipsIds[0]][1] >= lm_list[tipsIds[0] - 1][1]:
                FingerState[0] = 0

            # The 4 other fingers
            for i in range(1, len(Fingers)):
                if lm_list[tipsIds[i]][2] < lm_list[mcpIds[i]][2]:
                    FingerState[i] = 1
                if lm_list[tipsIds[i]][2] >= lm_list[mcpIds[i]][2]:
                    FingerState[i] = 0

            # If a gesture is found, publish it's related value via MQTT_Deprecated
            for i in range(len(Gesture_index)):
                if FingerState == Gesture[i]:
                    if time.time() - 2.0 >= time1:
                        Gesture_index_string = str(Gesture_index[i])
                        client.publish(topic, Gesture_index_string, retain=True)
                        print("Publish.....", Gesture_index_string)
                        time1 = time.time()

        # Display our camera, img
        cv2.imshow("Image", img)
        if cv2.waitKey(1) == ord('e'):  # Press e to exit loop
            break
# =============================================================================================
client.loop_stop
