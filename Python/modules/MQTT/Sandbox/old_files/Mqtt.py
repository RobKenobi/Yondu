import RPi.GPIO as GPIO
import time
import paho.mqtt.client as mqtt


# MQTT SETUP

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


broker = "161.200.199.2"
broker_port = 1883
client = mqtt.Client("Client1")

client.on_log = on_log
client.on_connect = on_connect
client.on_message = on_message

client.connect(broker, broker_port)
client.subscribe("Final Exam")

# RP4 GPIO SETUP
LED_PIN = 17
BUTTON_PIN = 2

GPIO.setmode(GPIO.BCM)
GPIO.setup(LED_PIN, GPIO.OUT)
GPIO.setup(BUTTON_PIN, GPIO.IN)

state = "off"
received_msg = ""
while True:
    client.loop_start()
    time.sleep(0.1)

    # Toggle led upon receiving a "TOGGLE" message from the broker
    print(received_msg)
    if received_msg == "TOGGLE":
        if state == "off":
            GPIO.output(LED_PIN, GPIO.HIGH)
        if state == "on":
            GPIO.output(LED_PIN, GPIO.LOW)
    else:
        GPIO.output(LED_PIN, GPIO.LOW)
        # if Button is pressed
        if GPIO.input(BUTTON_PIN) == GPIO.HIGH:
            # Publish Pierre HOUSSEAUX to Final Exam
            client.publish("Final Exam", "Pierre HOUSSEAUX")
            # Led Blinking
            GPIO.output(LED_PIN, GPIO.HIGH)
            state = "on"
            time.sleep(0.1)
        else:
            state = "off"

client.loop_stop()
client.disconnect()
GPIO.cleanup()
