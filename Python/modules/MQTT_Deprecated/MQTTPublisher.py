from .MQTTClient import MQTTClient

class MQTTPublisher(MQTTClient):

    def __init__(self, broker, broker_port):
        super().__init__(broker, broker_port)
        self._published_topics = list()

    def publish(self, topic, data):
        message_info = self._MQTT_client.publish(topic, data)
        success = message_info.is_published()
        if success:
            self._published_topics.append(topic)
        return success, message_info
