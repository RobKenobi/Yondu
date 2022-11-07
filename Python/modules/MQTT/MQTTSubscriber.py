from .MQTTClient import MQTTClient

class MQTTSubscriber(MQTTClient):
    def __init__(self, broker, broker_port, client_id):
        super().__init__(broker, broker_port, client_id)

    def subscribe(self, topic, on_message_callback):
        # TODO implement the subscribe method
        pass

