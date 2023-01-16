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
DISTANCE = 40  # cm
ANGLE = 20  # degree

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
    global flying, drone
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

        elif topic == "vx":
            if payload > 0:
                drone.move_forward(DISTANCE)
            elif payload < 0:
                drone.move_back(DISTANCE)
            else:
                pass

        elif topic == "vy":
            if payload > 0:
                drone.move_right(DISTANCE)
            elif payload < 0:
                drone.move_left(DISTANCE)
            else:
                pass
        elif topic == "vz":
            if payload > 0:
                drone.move_up(DISTANCE)
            elif payload < 0:
                drone.move_down(DISTANCE)
            else:
                pass
        elif topic == "v_yaw":
            if payload > 0:
                drone.rotate_counter_clockwise(ANGLE)
            if payload < 0:
                drone.rotate_clockwise(ANGLE)
            else:
                pass


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
        print("\rBattery level : ", drone.get_battery(), " %", end="")
        time.sleep(1)

except KeyboardInterrupt:
    print("Landing drone")
    drone.end()
    client.disconnect()
