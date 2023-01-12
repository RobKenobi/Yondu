import time

from djitellopy import Tello
from paho.mqtt.client import Client

"""
    Global variables
"""

# MQTT communication
BROKER = "broker.hivemq.com"
PORT = 1883

connected_to_broker = False
MAIN_TOPIC = "YONDU/DroneCommand/"

# Drone
drone = Tello()
flying = False
SPEED = 20  # cm/s
ANGLE = 10  # degree/s

vx = 0
vy = 0
vz = 0
v_yaw = 0

"""
    Defining communication callbacks
"""


def callback_on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("\nConnected to the broker")
        global connected_to_broker
        connected_to_broker = True
        subscription = MAIN_TOPIC + "#"
        client.subscribe(subscription)
        print(f"\nSubscribed to {subscription}")
    else:
        print("Connection failed")
        exit(1)


def callback_on_message(client, userdata, msg):
    global flying, drone, vx, vy, vz, v_yaw
    topic = msg.topic.split("/")[-1]
    payload = int(str(msg.payload.decode("utf-8")))

    if not flying:
        if topic == "takeoff" and payload == 1:
            drone.takeoff()
            flying = True

    else:
        if topic == "landing":
            drone.land()
            flying = False

        if topic == "stop":
            vx = 0
            vy = 0
            vz = 0
            v_yaw = 0

        elif topic == "vx":
            if payload > 0:
                vx = SPEED
            elif payload < 0:
                vx = - SPEED
            else:
                vx = 0

        elif topic == "vy":
            if payload > 0:
                vy = SPEED
            elif payload < 0:
                vy = -SPEED
            else:
                vy = 0
        elif topic == "vz":
            if payload > 0:
                vz = SPEED
            elif payload < 0:
                vz = - SPEED
            else:
                vz = 0
        elif topic == "v_yaw":
            if payload > 0:
                v_yaw = ANGLE
            if payload < 0:
                v_yaw = - ANGLE
            else:
                v_yaw = 0


def callback_on_disconnect(client, userdata, rc):
    print("Disconnected from the broker")
    global connected_to_broker
    connected_to_broker = False


"""
    Communication initialization
"""

print(44 * "*")
print("***     Communication initialization     ***")
print(44 * "*")

client = Client()
client.on_connect = callback_on_connect
client.on_message = callback_on_message
client.on_disconnect = callback_on_disconnect

client.connect(BROKER, PORT)
client.loop_start()

i = 0
while not connected_to_broker:
    print("\rConnecting to broker" + i * ".", end="")
    time.sleep(0.5)
    i += 1
    i %= 4

print("Connecting to the drone")
drone.connect()

try:
    while True:
        drone.send_rc_control(vy, vx, vz, v_yaw)
        print("\rBattery level : ", drone.get_battery(), " %", end="")
        time.sleep(0.5)

except KeyboardInterrupt:
    print("Landing drone")
    drone.end()
    client.disconnect()
