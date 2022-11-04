import time
import paho.mqtt.client as mqtt
import random


broker = "mqtt.eclipseprojects.io"
broker_port = 8883

client = mqtt.Client("Client_pub")

client.connect(broker, broker_port)

while True:
    number = random.randint(0, 10)
    client.publish("Rand", number)
    print("I pub", number)
    time.sleep(1)
