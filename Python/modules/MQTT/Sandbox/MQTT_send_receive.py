# MQTT SETUP
import time
import paho.mqtt.client as mqtt


def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("Client is connected")
    else:
        print("Client is not connected")

def on_log(client, userdata, level, buf):
    print("log" + buf)

def on_message(client, userdata, msg):
    global received_msg
    topic = msg.topic
    msg_decode = str(msg.payload.decode("utf-8"))
    print("Message received:", msg_decode, "on topic", topic)
    received_msg = msg_decode


broker = "123a425d9b0748a39d2d27a7c2d4b7eb.s2.eu.hivemq.cloud"
broker_port = 8883
client = mqtt.Client("Client1")

client.on_log = on_log
client.on_connect = on_connect
client.on_message = on_message

client.connect(broker, broker_port)

client.publish("Final Exam", "Pierre HOUSSEAUX")
client.subscribe("Final Exam")

state = "off"

received_msg=""
while True:
    client.loop_start()
    time.sleep(0.1)

    # Toggle led upon receiving a "TOGGLE" message from the broker
    print(received_msg)
    if received_msg == "TOGGLE":
        if state == "off":
            print("on")
        if state == "on":
            print("off")

client.loop_stop()
client.disconnect()
