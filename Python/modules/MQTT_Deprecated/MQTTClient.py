import paho.mqtt.client as mqtt

class MQTTClient:
    def __init__(self, broker, broker_port, client_id=""):
        self._broker = broker
        self._broker_port = broker_port
        self._client_id = client_id

        self._MQTT_client = mqtt.Client(client_id=self._client_id, clean_session=None, userdata=None, protocol=mqtt.MQTTv311,
                                        transport="tcp", reconnect_on_failure=True)

    def connect(self):
        ret = self._MQTT_client.connect(host=self._broker, port=self._broker_port, keepalive=60)
        return ret