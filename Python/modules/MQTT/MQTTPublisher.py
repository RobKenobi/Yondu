from .MQTTClient import MQTTClient

class MQTTPublisher(MQTTClient):

    def __init__(self, broker, broker_port):
        super().__init__(broker, broker_port)

    def publish(self, topic, data):
        message_info = self._MQTT_client.publish(topic, data)
        return message_info.is_published(), message_info
