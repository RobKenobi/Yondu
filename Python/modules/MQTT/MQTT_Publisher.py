import paho.mqtt.client as mqtt


class MQTT_Publisher:

    def __init__(self, broker, broker_port):
        self.broker = broker
        self.broker_port = broker_port

        self.MQTT_client = mqtt.Client(client_id="", clean_session=None, userdata=None, protocol=mqtt.MQTTv311,
                                       transport="tcp", reconnect_on_failure=True)

    def connect(self):
        self.MQTT_client.connect(host=self.broker, port=self.broker_port, keepalive=60)
        pass

    def publish(self, data):
    
        pass
