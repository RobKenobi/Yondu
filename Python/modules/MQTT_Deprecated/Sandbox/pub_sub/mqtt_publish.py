import time
import paho.mqtt.client as mqtt
import random
import numpy as np

# broker = "123a425d9b0748a39d2d27a7c2d4b7eb.s2.eu.hivemq.cloud"
# broker_port = 8883

# broker = "broker.hivemq.com"
broker = "mqtt.eclipseprojects.io"

userName = "HyUKLhwYGxslPTYuIBgyJQY"
clientID = "HyUKLhwYGxslPTYuIBgyJQY"
password = "DBc10E6UGVFNoc/lTpbLmyjG"

# broker = "mqtt3.thingspeak.com"
broker_port = 1883

client = mqtt.Client(client_id=clientID, )

client.connect(broker, broker_port)

# while True:
    # number = random.randint(0, 10)

for i in range(100):
    number=0
    if i == 10:
        number=1

    client.publish("takeoff", number)
    # client.publish("Test_mqtt/string", "Pierre")
    print("I pub", number)
    time.sleep(1)
