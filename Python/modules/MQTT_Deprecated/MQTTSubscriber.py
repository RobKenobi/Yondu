from .MQTTClient import MQTTClient


class MQTTSubscriber(MQTTClient):
    def __init__(self, broker, broker_port, client_id, on_message):
        super().__init__(broker, broker_port, client_id)
        self._on_message = on_message
        self._subscribed_topic = list()

    def subscribe(self, topic):
        self._MQTT_client.subscribe(topic)
        self._subscribed_topic.append(topic)
