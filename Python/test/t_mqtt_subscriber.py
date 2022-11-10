import sys
import os

PYTHON_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(1, PYTHON_DIR)

from modules.MQTT import MQTTSubscriber

broker = "mqtt.eclipseprojects.io"
broker_port = 1883
client_id = 1


def on_message(client, userdata, msg):
    global received_msg
    topic = msg.topic
    msg_decode = str(msg.payload.decode("utf-8"))
    print("Message received:", msg_decode, "on topic", topic)
    received_msg = msg_decode


client = MQTTSubscriber(broker, broker_port, client_id, on_message)

client.connect()
client.subscribe("Rand")

while True:
    client.loop_start()
