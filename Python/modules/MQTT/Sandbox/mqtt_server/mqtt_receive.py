import time
import paho.mqtt.client as mqtt

broker = "mqtt.eclipseprojects.io"
broker_port = 1883


def on_message(client, userdata, msg):
    global received_msg
    topic = msg.topic
    msg_decode = str(msg.payload.decode("utf-8"))
    print("Message received:", msg_decode, "on topic", topic)
    received_msg = msg_decode


client = mqtt.Client("Client_receiv")
client.connect(broker, broker_port)


while True:
    client.loop_start()
    client.subscribe("Rand")
    client.on_message = on_message

client.loop_stop()