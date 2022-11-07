import sys
import os

# Add Python directory to the path variable
PYTHON_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(1, PYTHON_DIR)

from modules.MQTT import MQTTPublisher
import numpy as np
import time

broker = "mqtt.eclipseprojects.io"
broker_port = 1883

publisher = MQTTPublisher(broker, broker_port)
print(publisher.connect())


while True:
    message = np.random.choice(10)
    topic = "RAND"
    success, _ = publisher.publish(topic, message)
    if success:
        print(f"Send <{message}> on <{topic}>")
    time.sleep(1)