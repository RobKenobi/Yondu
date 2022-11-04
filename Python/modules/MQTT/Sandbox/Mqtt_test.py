import paho.mqtt.client as mqtt


# =========================================================================

def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("Client is connected")
    else:
        print("Client is not connected")


def on_log(client, userdata, level, buf):
    print("log" + buf)


# =========================================================================

broker = "123a425d9b0748a39d2d27a7c2d4b7eb.s2.eu.hivemq.cloud"
broker_port = 8883

client = mqtt.Client("Client1")

client.on_publish = on_publish
client.on_log = on_log
client.on_connect = on_connect

client.connect(broker, broker_port)

client.publish("Final Exam", "Pierre HOUSSEAUX")


