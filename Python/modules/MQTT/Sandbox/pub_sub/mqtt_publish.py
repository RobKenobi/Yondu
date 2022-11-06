import time
import paho.mqtt.client as mqtt
import random



#broker = "123a425d9b0748a39d2d27a7c2d4b7eb.s2.eu.hivemq.cloud"
#broker_port = 8883

broker = "broker.hivemq.com"
#broker = "mqtt.eclipseprojects.io"
broker_port = 1883


client = mqtt.Client("Client_pub")

client.connect(broker, broker_port)

while True:
    number = random.randint(0, 10)
    client.publish("Rand", number)
    print("I pub", number)
    time.sleep(1)
