import random
import time

from paho.mqtt.client import Client

# Communication initialisation
BROKER = "mqtt.eclipseprojects.io"
BROKER_PORT = 1883

client = Client()
client.connect(BROKER, BROKER_PORT)

last_time = time.time()
Time_period = 0.5

choices = ["takeoff", "landing", "vx", "vy", "vz", "v_yaw"]

while True:
    try:
        if time.time() - last_time > 0.5:
            client.publish("YONDU/DroneCommand/" + random.choice(choices), random.randint(-1, 1))
            client.publish("YONDU/DroneCommand/" + random.choice(choices), random.randint(-1, 1))
            last_time = time.time()

    except KeyboardInterrupt:
        print("End")
        break
