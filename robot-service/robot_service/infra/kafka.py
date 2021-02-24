import logging

from kafka import KafkaProducer, KafkaConsumer
from lazy_object_proxy.simple import Proxy


from robot_service.utils.serializer import dumps, loads


logger = logging.getLogger(__name__)


class RobotKafkaProducer(KafkaProducer):
    def __init__(self):
        super().__init__(
            value_serializer=lambda m: dumps(m).encode('utf-8'),
            bootstrap_servers='robot-championship-kafka:9092'
        )
       
    def send(self, value):
        return super().send('robot-championship.robots', value)


class ChampionshipKafkaProducer(KafkaProducer):
    def __init__(self):
        super().__init__(
            value_serializer=lambda m: dumps(m).encode('utf-8'),
            bootstrap_servers='robot-championship-kafka:9092',
        )

    def send(self, value):
        return super().send('robot-championship.championships', value)


robot_message_sender = Proxy(RobotKafkaProducer)


championship_message_sender = Proxy(ChampionshipKafkaProducer)


def init_message_listening(app):
    from robot_service.messaging.championship import ChampionshipKafkaConsumer
    logger.info('Initializing message listening')
    championship_event_consumer = ChampionshipKafkaConsumer(KafkaConsumer(
        'robot-championship.championships',
        value_deserializer=lambda m: loads(m.decode('utf-8')),
        bootstrap_servers='robot-championship-kafka:9092',
        group_id='robot-service'
    ), app)
    championship_event_consumer.start()
