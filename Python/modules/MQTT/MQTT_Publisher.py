import paho.mqtt.client as mqtt


class MQTT_Publisher:

    def __init__(self, broker, broker_name):
        self.broker = broker
        self.broker_name = broker_name

        self.MQTT_client = mqtt.Client(client_id="", clean_session=None, userdata=None, protocol=mqtt.MQTTv311,
                                       transport="tcp", reconnect_on_failure=True)

    def connect(self):

        pass

    def publish(self,data):
        pass